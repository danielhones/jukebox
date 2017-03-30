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

from peewee import DoesNotExist
from pyItunes import Library

from jukebox.models import Album, Artist, create_db, Song


ITUNES_FILE = 'itunes_library.xml'
ITUNES_FILE_BAK = 'itunes_library.xml.bak'


class SongDb():
    def __init__(self, lib_file=ITUNES_FILE, echo=True):
        self.library_file = lib_file

    def populate_db(self):
        print('Backing up', ITUNES_FILE)
        shutil.copyfile(ITUNES_FILE, ITUNES_FILE_BAK)

        print('Parsing iTunes file...')
        library = Library(ITUNES_FILE)
        print('Done, library contains %s songs.' % len(library.songs))

        print('Populating db...')
        for key, s in library.songs.items():
            try:
                if not s.location or s.location.endswith('.ipa'):
                    continue  # Don't include apps


                try:
                    artist, _ = Artist.get_or_create(name=s.artist.strip())
                except Exception as e:
                    #print("Error getting artist:", e, "Song:", s.name)
                    artist = None

                try:
                    album, _ = Album.get_or_create(title=s.album.strip(), artist=artist)
                except Exception as e:
                    #print("Error getting album:", e, "Song:", s.name)
                    album = None
                    
                new_song = Song.create(title=s.name,
                                       location=s.location,
                                       track_id=key,
                                       track_number=s.track_number,
                                       length=s.length,
                                       artist=artist,
                                       album=album)

                #print('Adding', new_song.title)
                #new_song.save()
            except Exception as e:
                print("Error saving song:", e)
                # raise
            
        print('Done')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'update':
        database = SongDb()
        database.populate_db()
    elif len(sys.argv) == 2 and sys.argv[1] == 'init':
        create_db()
        database = SongDb()
        database.populate_db()
