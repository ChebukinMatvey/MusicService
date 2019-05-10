from sqlalchemy import create_engine, insert
from pprint import pprint
from sqlalchemy.orm import Session
import pandas as pd
from domain.scheme import Tag,Feature, Artist,Song,Album,artists_songs as artists_songs_table


def fill_table_wrapper(df,foo):
    session = get_session()
    session.execute('SET FOREIGN_KEY_CHECKS=0;')
    buffer = []
    for i,row in df.iterrows():
        if i%20000 == 0:print(i)
        foo(buffer,row,session)
        if len(buffer) == 20000:
            session.bulk_save_objects(buffer)
            session.commit()
            buffer = []
    else:
        session.bulk_save_objects(buffer)
        session.commit()
    session.close()


def get_session():
    engine = create_engine('mysql://nokinobi:xxxtera@localhost:3306/music?charset=utf8mb4')
    session = Session(bind=engine)
    return session


def tag(buffer,row,session):
    tag = row['tag'] if isinstance(row['tag'],str) else str(row['tag'])
    buffer.append(Tag(description=tag[:70]))


def artist(buffer,row,session):
    if row['name'] == row['name']: # not NaN
        buffer.append(Artist(id=row['id'],name=row['name'][:60],followers=row['followers'],popularity=row['popularity']))


def album(buffer,row,session):
    row['name'] = row['name'] if isinstance(row['name'],str) else str(row['name'])
    row['total_tracks']= row['total_tracks'] if isinstance(row['total_tracks'],int) else 0
    buffer.append(Album(id=row['id'],name=row['name'][:60],img=row['img'],type=row['type'],total_tracks=row['total_tracks'],
                        artists_id=row['artist_id']))


def song(buffer,row,session):
    buffer.append(Song(
                id=row['id'],
                name= str(row['name'])[:250],
                popularity=row['popularity'],
                track_number=row['track_number'],
                artist= [session.query(Artist).get(row['artist_id'])],
                album_id=row['album_id'],
                features_id=row['feature_id']))


def feature(buffer,row,session):
    duration = row['duration'] if isinstance(row['duration'],int) else 0
    danceability = (row['danceability']) if isinstance(row['danceability'],float) else 0
    energy = float(row['energy']) if isinstance(row['energy'],float) else 0
    instrumentalness = float(row['instrumentalness']) if isinstance(row['instrumentalness'],float) else 0
    liveness = float(row['liveness']) if isinstance(row['liveness'],float) else 0
    loudness = float(row['loudness']) if isinstance(row['loudness'],float) else 0
    valence = float(row['valence']) if isinstance(row['valence'],float) else 0
    tempo = float(row['tempo']) if isinstance(row['tempo'],float) else 0

    buffer.append(Feature(
                    id =row['id'],
                    duration = round(duration,4),
                    danceability = round(danceability,4),
                    energy = round(energy,4),
                    instrumentalness = round(instrumentalness,4),
                    liveness = round(liveness,4),
                    loudness = round(loudness,4),
                    valence = round(valence,4),
                    tempo = round(tempo,4),
                    song_id=row['track_id']))    

def update_genre(df):
    session = get_session()
    for i,row in df.iterrows():
        if i % 10000==0:
            print(i)
        song = session.query(Song).get(row['song_spotify_id'])
        if song is None:
            continue
        song.genere = str(row['genre'])
        session.commit()          


def update_tags(df):
    session = get_session()
    for i,row in df.iterrows():
        song = session.query(Song).get(row['song_spotify_id'])
        song.tag = session.query(Tag).filter(Tag.description==row['tag'][:70]).first()
        session.commit()


def artist_song(df):
    session = get_session()
    for i,row in df.iterrows():
        stm = ((artists_songs_table.insert({'artist_id':row['artist_id'],'song_id':row['id']})))
        try:
            session.execute(stm)
            session.commit()
        except Exception as exc:
            print(exc)
        if i % 20000 ==0:
            print(i)