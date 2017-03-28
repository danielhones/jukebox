import itertools
import logging
import os

from peewee import *

from jukebox import settings


db = SqliteDatabase(settings.DATABASE_FILE)


class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def all(cls):
        return cls.select().where(True)

    def attributes(self, exclude=None):
        if exclude is None:
            exclude = []
        return {k: v for k, v in self._data.items() if k not in exclude}

    def __repr__(self):
        return "{name}({data})".format(
            name=self.__class__.__name__,
            data=", ".join(['{}={}'.format(k, repr(v)) for k,v in self._data.items()]))


class Artist(BaseModel):
    name = CharField()


class Album(BaseModel):
    title = CharField()
    artist = ForeignKeyField(Artist, related_name='albums', null=True)


class Song(BaseModel):
    """
    Row representing useful info about a song in iTunes library
    """
    title = CharField()
    location = CharField()
    track_id = IntegerField()
    length = IntegerField(null=True)   # in milliseconds
    album = ForeignKeyField(Album, related_name='songs', null=True)
    artist = ForeignKeyField(Artist, related_name='songs', null=True)

    @property
    def formatted_length(self):
        if self.length is None:
            return ""
        seconds = self.length // 1000
        minutes = seconds // 60
        seconds = seconds - (minutes * 60)
        return "{}:{:02d}".format(minutes, seconds)

    @property
    def artist_name(self):
        return self.artist.name if self.artist is not None else ""
    
    @property
    def album_title(self):
        return self.album.title if self.album is not None else ""

    def attributes(self, exclude=None):
        if exclude is None:
            exclude = []
        r = {k: v for k, v in self._data.items() if k not in exclude}
        r.update({
            'formatted_length': self.formatted_length,
            'artist_name': self.artist_name,
            'album_title': self.album_title,
        })
        return r


def create_db():
    db.connect()
    db.create_tables([Album, Artist, Song], safe=True)

