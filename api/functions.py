from database.scheme import *
from database.database import get_session
from Levenshtein import jaro
import json
import urllib3
from sqlalchemy import and_
from random import shuffle

session = get_session()

def get_songs(query,username):
    songs = session.query(Song).filter(Song.stream!=None).all()
    user = session.query(User).filter(User.name==username).first()
    res = []
    for song in songs:
        cof =jaro(song.name,query)
        if cof > 0.7:
            res.append(
                {
                    "id":song.id,
                    "name":song.name,
                    "duration": song.feature.duration,
                    "stream":song.stream,
                    "artists": [ artist.name for artist in song.artist],
                    "img":song.album.img,
                    "like":True if song in user.liked_songs else False,
                    "jaro":cof
                }
            )
    res = sorted(res,key=(lambda x:x['jaro']),reverse=True)
    return res


def get_artist(name):
    artists =  session.query(Artist).all()
    result = []
    for artist in artists:
        coeff = jaro(artist.name,name)  
        if  coeff > 0.85:
            songs = []
            for song in artist.songs:
             songs.append(
                 {
                     "id":song.id,
                     "name":song.name,
                     "duration":song.feature.duration,
                     "album":song.album.name,
                     "img":song.album.img
                 }
             )
            result.append({
                "name":artist.name,
                "followers":artist.followers,
                "songs":songs,
                "jaro":coeff
            })
    result = sorted(result,key = lambda x:x['jaro'],reverse=True)
    return result[:10] 


def get_albums(artist_name):
    artists = session.query(Artist).all()
    res = []
    for artist in artists:
        cof = jaro(artist_name,artist.name)
        if cof > 0.85:
            res.append({
                "artist":artist.name,
                "followers":artist.followers,
                "albums":[ { "id":album.id ,"name":album.name , "img":album.img,"songs":album.total_tracks} for album in artist.albums ],
                "jaro":cof
            })
    res = sorted(res, key = lambda x:x['jaro'],reverse=True)
    return res[:25]


def get_album(id):
    album = session.query(Album).get(id)
    if album is None:
        return {}
    else:
        return {
                "id":album.id,
                "name":album.name,
                "songs": [ {
                                "id" : song.id,
                                "name" : song.name,
                                "duration" : song.feature.duration,
                                "img" : song.album.img
                            }
                            for song in album.songs
                         ]
        }


def find_user(name,pswd):
    user = session.query(User).filter(and_(User.name==name,User.pswd==pswd))
    return user


def add_like(username,song_id):
    user = session.query(User).filter(User.name==username).first()
    if user is None: return False
    song = session.query(Song).get(song_id)
    if song not in user.liked_songs:
        user.liked_songs.append(song)
        session.add(user)
        session.commit()
        return True
    else: return False

def delete_like(username,song_id):
    user = session.query(User).filter(User.name==username).first()
    if user is None:
        return False
    song = session.query(Song).get(song_id)
    user = session.query(User).filter(User.name==username).first()
    user.liked_songs.remove(song)
    session.add(user)
    session.commit()
    return True

def get_user_likes(username):
    user = session.query(User).filter(User.name==username).first()
    res = []
    for song in user.liked_songs:
        res.append(
                {
                    "id":song.id,
                    "name":song.name,
                    "duration": song.feature.duration,
                    "stream":song.stream,
                    "artists": [ artist.name for artist in song.artist],
                    "img":song.album.img,
                    "like":True
                }
            )
    return res



def distance(left,right):
    return  (float( (left.feature.danceability - right.feature.danceability)**2 + 
            (left.feature.instrumentalness - right.feature.instrumentalness)**2 + 
            (left.feature.loudness - right.feature.loudness)**2 + 
            (left.feature.liveness - right.feature.liveness)**2 + 
            (left.feature.tempo - right.feature.tempo)**2 + 
            (left.feature.valence - right.feature.valence)**2
            ))**0.5


def get_recommendations(username):
    user = session.query(User).filter(User.name==username).first()
    all_songs = session.query(Song).all()
    res = []
    for song in user.liked_songs:
        for s in all_songs:
            if s == song: continue
            if len(res) == 25: break
            d = distance(s,song)
            if d < 0.5:
                res.append(
                    {
                        "id":s.id,
                        "name":s.name,
                        "duration": s.feature.duration,
                        "stream":s.stream,
                        "artists": [ artist.name for artist in s.artist],
                        "img":s.album.img,
                        "like":False
                    }
                )
    shuffle(res)
    return (res)