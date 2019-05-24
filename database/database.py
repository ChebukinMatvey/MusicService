#!/usr/bin/python3
import pandas as pd
from database.scheme import Artist, Album,Song
from database.scheme import init_schema
from database.functions import *
import json
from pprint import pprint
import requests

def fill_albums():
    # Fill albums 
    albums = pd.read_csv('./spotify/csv/albums.csv',sep=';',error_bad_lines=False)
    albums = albums.drop_duplicates(subset=['id'],keep='first').reset_index()
    fill_table_wrapper(albums,album)



def fill_data():
    # Fill artists 
    artists = pd.read_csv('./spotify/csv/artists_updated.csv',sep=',',error_bad_lines=False)
    artists = artists.drop_duplicates(subset=['id']).reset_index()
    fill_table_wrapper(artists,artist)

    # fill songs features 
    features = pd.read_csv('./spotify/csv/features.csv',sep=';')
    features.drop_duplicates(subset=['id'],keep='first',inplace=True)
    features = features.reset_index()
    fill_table_wrapper(features,feature)

    # Fill songs 
    songs = pd.read_csv('./spotify/csv/tracks.csv',sep=';')
    fill_table_wrapper(songs.drop_duplicates(subset=['id'],keep='first').reset_index(),song)

    # Fill tags table 
    tags = pd.read_csv('./spotify/csv/tags.csv',sep=';')
    fill_table_wrapper(tags,tag)
    
    # Update genre in song  
    tags = pd.read_csv('./spotify/csv/tags.csv',sep=';')
    update_genre(tags.drop_duplicates(subset=['song_spotify_id'],keep='first').reset_index())

    # Update songs-tag  field 
    update_tags(tags)

    # Fill atists_songs table 
    songs = pd.read_csv('./spotify/csv/tracks.csv',sep=';')
    artist_song(songs.drop_duplicates(subset=['id'],keep='first').reset_index())


def fill_streams():
    session = get_session()
    batch = []
    songs = session.query(Song).all()
    for i in range(150000,len(songs)):
        song = songs[i]
        print("Processing",i)
        try: 
            query = f"https://zvuk.com/sapi/search?query={(song.artist[0].name + ' ' + song.name) }&include=track"
            resp = requests.get(query).json()
            if 'tracks' not in resp['result']: continue
            id = list(resp["result"]["tracks"].keys())[0]
            song.stream = id 
            batch.append(song)
            if len(batch) == 100:
                session.bulk_save_objects(batch)
                session.commit()
                batch = []
                print("Batch saved")
        except Exception as e:
            print("Exception on ",i,query,e)
            continue

def insert():
    # init_schema()
    # fill_data()

    session = get_session()
    song = session.query(Song).get('3JEzGRDUsozrehZTq3dKE8')
    pprint(song.__dict__)