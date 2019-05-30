#!/usr/bin/python3
import pprint as pp 
import pandas as pd 
import os 
import threading
import copy 
import math
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import requests

tracks_file = open('tracks.csv','a')
artists_file = open('artists.csv','a')
albums_file = open('albums.csv','a')
features_file = open('features.csv','a')


artist_df = pd.DataFrame(columns=['id','name','track_id'])
tracks_df = pd.DataFrame(columns=['id','name','artist_id','popularity','album_id','feature_id','track_number'])
albums_df = pd.DataFrame(columns=['id','name','artist_id','img','type','total_tracks'])
features_df = pd.DataFrame(columns=['duration','danceability','energy','instrumentalness','liveness','loudness','valence',
                                'tempo','id','track_id'])

features_df.to_csv(features_file,sep=';',index=False)
albums_df.to_csv(albums_file,sep=';',index=False)
artist_df.to_csv(artists_file,sep=';',index=False)
tracks_df.to_csv(tracks_file,sep=';',index=False)



creds =  SpotifyClientCredentials(
client_id ="3777d2616b8945af8d6cf30dbea45517",
client_secret = "d3829f43311340e48cf1907bdaffda54")
sp = Spotify(client_credentials_manager=creds)





def process_tracks(tracks,features):
    for i,track in enumerate(tracks['tracks']):
        # artist
        for i,artist in enumerate(track['artists']):
            try:
                artist_df.loc[i] = [artist['id'],artist['name'],track['id']] 
            except Exception as exc:
                print( f"Exception while artist processed {artist['id']}  {exc}" )
        artist_df.to_csv(artists_file,sep=';',index=False,header=False)
        artist_df.drop(artist_df.index,inplace=True)
 
        # album 
        album =track['album']
        try:
            albums_df.loc[0] = [album['id'],album['name'],album['artists'][0]['id'],album['images'][1]['url'],
                            album['album_type'],album['total_tracks']]
        except Exception as exc:
            albums_df.loc[0] = [album['id'],album['name'],album['artists'][0]['id'],"No image",
                            album['album_type'],album['total_tracks']]
            print( f"Exception while album processed {album['id']}  {exc}" )
 
        albums_df.to_csv(albums_file,header=False,sep=';',index=False)
        albums_df.drop(albums_df.index,inplace=True)
        # feature
        try:     
            feature = features[i]
            features_df.loc[0] = [feature['duration_ms'],feature['danceability'],feature['energy'],feature['instrumentalness'],feature['liveness'],
                               feature['loudness'],feature['valence'],feature['tempo'],feature['id'],track['id']]       
        except Exception as exc:
            features_df.loc[0] = ['-','-','-','-','-','-','-','-','-',track['id']]
            print(f"Noe feature for {track['id']}")
        features_df.to_csv(features_file,sep=';',index=False,header=False)
        features_df.drop(features_df.index,inplace=True)
 
        # track
        try:
            tracks_df.loc[i] = [ track['id'] , track['name'] , track['artists'][0]['id'] , track['popularity'] , track['album']['id'], feature['id'] , track['track_number'] ]
        except Exception as exc:
            tracks_df.loc[0] = [track['id'],'-','-','-','-','-','-']
            print( f"Exception while track processed {track['id']}  {exc}" )
        tracks_df.to_csv(tracks_file,sep=';',header=False,index=False)
        tracks_df.drop(tracks_df.index,inplace=True)

total_songs_processed = 0

def main1():
    songs  = pd.read_csv('./data/csv/songs.csv',delimiter=';',error_bad_lines=False)
    # genres = pd.read_csv('./data/csv/tags.csv',delimiter=';',error_bad_lines=False)
    N = len(songs) 
    total_songs_processed += 521000
    songs = songs.truncate(before=521000,after=N) 
    ids = []
    features = []
    for i, row in songs.iterrows():
        if len(row['spotify_id']) != 22:
            continue
        ids.append(row['spotify_id'])
        if len(ids)  == 45 :
            try:
                tracks = sp.tracks(ids)          
                features = sp.audio_features(ids)
            except Exception as exc:
                print("Some exception happened during http request: ")
            process_tracks(tracks,features)
            ids = []
            total_songs_processed += 50
            print(total_songs_processed)


def main2():
    """ Get all data by artist name """
    dataset = pd.read_csv('/home/nokinobi/Workspace/PycharmProjects/Thesis/spotify/au.csv',delimiter=',')
    # print(dataset)
    for _,row in dataset.iterrows():
        _,_,id = row[1].split(':')
        print(id)        
        # query = f"https://zvuk.com/sapi/search?query={(song.artist[0].name + ' ' + song.name) }&include=track"
        # resp = requests.get(query).json()
        # if 'tracks' not in resp['result']: continue
        # id = list(resp["result"]["tracks"].keys())[0]




if __name__ == "__main__":
    main2()