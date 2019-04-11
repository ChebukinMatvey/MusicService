#!/usr/bin/python3
from sqlalchemy import String,ForeignKey, create_engine,Integer, SmallInteger, Column, Table 
from sqlalchemy.orm import backref,relationship,Session
from sqlalchemy.ext.declarative import declarative_base 
Base = declarative_base()




artists_songs_table = Table(
        'artists_songs_table',
        Base.metadata, 
        Column('artist_id',String(23),ForeignKey('artists.id')),
        Column('song_id',String(23),ForeignKey('songs.id'))
) 


songs_tags_table = Table(
    'songs_tags_table',
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
    songs = relationship('Song',secondary=artists_songs_table)
    album = relationship("Album")

    def __init__(self,id,name,followers, popularity):
        self.id = id
        self.name = name
        self.followers = followers
        self.popularity = popularity


#######################################################
class Album(Base):
    __tablename__ = 'albums'

    id = Column(String(23),primary_key=True)
    name = Column(String(60))
    img = Column(String(80))
    type = Column(String(15))
    total_tracks = Column(SmallInteger)
    artists_id = Column(String(23),ForeignKey('artists.id'))
    artist = relationship("Artist",uselist=False)
    songs = relationship('Song',uselist=False,backref="albums")


    def __init__(self,id,name,img,type,total_tracks,artist):
        self.id = id
        self.name = name 
        self.img = img 
        self.type = type
        self.total_tracks = total_tracks
        self.artist = artist


#########################################################
class Tag(Base):
    __tablename__= 'tags'
    id = Column(Integer, primary_key=True,autoincrement=True)
    description = Column(String(70))
    songs = relationship('Song',secondary=songs_tags_table)
    def __init__(self,d):
        self.description = d


#########################################################
class Song(Base):
    __tablename__ = 'songs'
    id = Column(String(23),primary_key = True)
    name = Column(String(250))
    popularity = Column(SmallInteger)
    track_number = Column(SmallInteger)
    genere = Column(String(30))
 
    tags = relationship('Tag',secondary=songs_tags_table)
    artist = relationship('Artist',secondary=artists_songs_table)
    album_id = Column(String(23),ForeignKey('albums.id'))

    def __init__(self,id,name,popularity,track_number,genre,tag):
        self.id = id
        self.name = name
        self.popularity = popularity 
        self.track_number = track_number 
        self.genere = genre,
        self.tag_id =  tag
        # self.artist_id = artist_id
        # self.album_id = "we"




def init_schema():
    engine = create_engine('mysql://nokinobi:xxxtera@localhost:3306/music?charset=utf8mb4',
    echo=True)
    Base.metadata.create_all(bind=engine)   
    session = Session(bind=engine,autocommit=True)
    res =    session.query(Album).join(Artist).all()
    