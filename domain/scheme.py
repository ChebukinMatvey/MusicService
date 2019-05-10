#!/usr/bin/python3
from sqlalchemy import Float,String,ForeignKey, create_engine,Integer, SmallInteger, Column, Table 
from sqlalchemy.orm import backref,relationship,Session
from sqlalchemy.ext.declarative import declarative_base 


Base = declarative_base()


artists_songs = Table(
        'artists_songs',
        Base.metadata, 
        Column('artist_id',String(23),ForeignKey('artists.id')),
        Column('song_id',String(23),ForeignKey('songs.id'))
) 
songs_tags = Table(
    'songs_tags',
    Base.metadata,
    Column('song_id',String(23),ForeignKey('songs.id')),
    Column('tag_id',Integer,ForeignKey('tags.id'))
)



######################################################
class Artist(Base):
    __tablename__ = 'artists'
    id = Column(String(23), primary_key = True)
    name = Column(String(60))
    followers = Column(Integer)
    popularity = Column(SmallInteger)
    songs = relationship('Song',secondary=artists_songs)
    albums = relationship('Album')

#######################################################
class Album(Base):
    __tablename__ = 'albums'
    id = Column(String(23),primary_key=True)
    name = Column(String(60))
    img = Column(String(80))
    type = Column(String(15))
    total_tracks = Column(SmallInteger)
    songs = relationship('Song',backref="album")
    artists_id = Column(String(23),ForeignKey('artists.id'))
    artist = relationship('Artist')



#########################################################
class Tag(Base):
    __tablename__= 'tags'
    id = Column(Integer, primary_key=True,autoincrement=True)
    description = Column(String(70))
    songs = relationship('Song',secondary=songs_tags)


#########################################################
class Song(Base):
    __tablename__ = 'songs'
    id = Column(String(23),primary_key = True)
    name = Column(String(250))
    popularity = Column(SmallInteger)
    track_number = Column(SmallInteger)
    genere = Column(String(30))
    
    tags = relationship('Tag',secondary=songs_tags)
    artist = relationship('Artist',secondary=artists_songs)
    album_id = Column(String(23),ForeignKey('albums.id'))
 
    features_id = Column(String(23),ForeignKey('features.id'))
    feature = relationship('Feature',uselist=False,foreign_keys=[features_id])



###########################################################
class Feature(Base):
    __tablename__='features'

    id = Column(String(23),primary_key=True)
    duration = Column(Integer)
    danceability = Column(Float(6,4))
    energy= Column(Float(6,4))
    instrumentalness = Column(SmallInteger)
    liveness = Column(Float(6,4))
    loudness = Column(Float(6,4))
    valence = Column(Float(6,4))
    tempo = Column(Float(7,4))

    song_id = Column(String(23),ForeignKey('songs.id'))
    song =  relationship('Song',uselist=False,foreign_keys=[song_id])


def init_schema():
    engine = create_engine(
        'mysql://nokinobi:xxxtera@localhost:3306/music?charset=utf8mb4',
        echo=True
    )
    Base.metadata.create_all(bind=engine)
