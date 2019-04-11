from sqlalchemy import create_engine, insert
from pprint import pprint
from sqlalchemy.orm import Session
import pandas as pd
from domain.scheme import Tag, Artist,Song,Album


def fill_table_wrapper(df,foo):
    session = get_session()
    buffer = []
    for i in range(len(df)):
        if i%20000 == 0:print(i)
        row = df.loc[i]
        foo(buffer,row)
        if len(buffer) == 20000:
            session.bulk_save_objects(buffer)
            session.commit()
            buffer = []
    session.commit()
    session.close()       


def get_session():
    engine = create_engine('mysql://nokinobi:xxxtera@localhost:3306/music?charset=utf8mb4')
    session = Session(bind=engine)
    return session


def tag(buffer,row):
    tag = row['tag'] if isinstance(row['tag'],str) else str(row['tag'])
    buffer.append(Tag(tag[:70]))


def artist(buffer,row):
    if row['name'] == row['name']: # not NaN
        buffer.append(Artist(row['id'],row['name'][:60],row['followers'],row['popularity']))


def album(buffer,row):
    buffer.append(Album(row['id'],row['name'],row['img'],row['type'],row['total_tracks'],row['artist_id']))



def song(buffer,row):
    tag_id = 1
    genre = '-'
    buffer.append(Song(row['id'],row['name'],row['popularity'],row['track_number'],
    tag_id,row['artist_id'],row['album_id'],genre))