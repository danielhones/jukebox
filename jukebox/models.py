from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_FILE = 'itunesdb.sqlite3'
ENGINE_ECHO = False

engine = create_engine('sqlite:///' + DB_FILE, echo=ENGINE_ECHO)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")

    def __repr__(self):
        return "Album(id={id}, title='{}', artist_id={})".format(self.title, self.artist_id)


class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = relationship("Album", back_populates="artist")

    def __repr__(self):
        return "Artist(id={id}, name='{}')".format(self.name)


class Song(Base):
    """
    Row representing useful info about a song in iTunes library
    """
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship("Album", back_populates="songs")
    location = Column(String)

    @property
    def artist(self):
        return self.album.artist
    
    def __repr__(self):
        return "Song(id={id}, title='{title}', album_id='{album_id}', location='{location')".format(**self.__dict__)
