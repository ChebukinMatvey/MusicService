from database.scheme import *
from database.database import get_session
from Levenshtein import jaro
import json
import urllib3

session = get_session()

def get_songs(name):
    songs = session.query(Song).filter(Song.stream!=None).all()
    res = []
    for song in songs:
        cof =jaro(song.name,name)
        if cof > 0.7:
            res.append(
                {
                    "id":song.id,
                    "name":song.name,
                    "duration": song.feature.duration,
                    "stream":song.stream,
                    "artists": [ artist.name for artist in song.artist],
                    "img":song.album.img,
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


def get_stream(id):
    song = session.query(Song).get(id)
    return song.stream 



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