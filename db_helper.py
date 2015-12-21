"""
Helper classes to convert iTunes library XML file to SQLite database to use in Flask app

Usage:
db = SongDb('itunes/library/file.xml', echo=False)
db.create_db()
db.populate_db()
"""
import xml.etree.cElementTree as ET
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyItunes import Library
import sys


DB_FILE = 'itunesdb.sqlite3'
ITUNES_FILE = 'itunes_library.xml'
Base = declarative_base()


class Song(Base):
    """
    Row representing useful info about a song in iTunes library
    """
    # TODO: create indexes for title, artist, album
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String)
    location = Column(String)
    # TODO: consider including length of song here

    def __repr__(self):
        return "Song(id=%s, title=%s, artist=%s, album=%s, location=%s)" % (
            self.id, self.title, self.artist, self.album, self.location)


class SongDb():
    def __init__(self, lib_file=ITUNES_FILE, echo=True):
        self.engine = create_engine('sqlite:///' + DB_FILE, echo=echo)
        self.library_file = lib_file
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def populate_db(self):
        print('Parsing iTunes file...')
        library = Library(ITUNES_FILE)
        print('Done, library contains %s songs.' % len(library.songs))

        print('Populating db...')
        for key, s in library.songs.items():
            new_song = Song(id=key, title=s.name, artist=s.artist, album=s.album, location=s.location)
            print('Adding', new_song.title)
            if new_song.location.endswith('.ipa'):
                # Don't include apps
                continue
            else:
                self.session.add(new_song)
        self.session.commit()
        print('Done')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'populate':
        db = SongDb()
        db.populate_db()
