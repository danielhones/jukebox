from peewee import *


DB_FILE = 'itunesdb.sqlite3'
db = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db

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
    length = IntegerField()
    album = ForeignKeyField(Album, related_name='songs', null=True)


def create_db():
    db.connect()
    db.create_tables([Album, Artist, Song])

