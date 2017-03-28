"""
Helper classes to convert iTunes library XML file to SQLite database to use in Flask app

Usage:
db = SongDb('itunes/library/file.xml', echo=False)
db.create_db()
db.populate_db()
"""
import shutil
import sys
import xml.etree.cElementTree as ET

from pyItunes import Library
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from jukebox.models import Album, Artist, DB_FILE, Song


ITUNES_FILE = 'itunes_library.xml'
ITUNES_FILE_BAK = 'itunes_library.xml.bak'
Base = declarative_base()


class SongDb():
    def __init__(self, lib_file=ITUNES_FILE, echo=True):
        self.engine = create_engine('sqlite:///' + DB_FILE, echo=echo)
        self.library_file = lib_file
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def populate_db(self):
        print('Backing up', ITUNES_FILE)
        shutil.copyfile(ITUNES_FILE, ITUNES_FILE_BAK)
        print('Parsing iTunes file...')
        library = Library(ITUNES_FILE)
        print('Done, library contains %s songs.' % len(library.songs))

        print('Populating db...')
        for key, s in library.songs.items():
            new_song = Song(id=key, title=s.name, location=s.location)
            if new_song.location.endswith('.ipa'):
                continue  # Don't include apps

            print('Adding', new_song.title)
            # make album/artist here
            #q = self.session.query(Artist, name=s.artist)
            
            self.session.add(new_song)
        self.session.commit()
        print('Done')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        db = SongDb()
        db.populate_db()
    elif len(sys.argv) == 2 and sys.argv[1] == 'init':
        db = SongDb()
        db.create_db()
        db.populate_db()
