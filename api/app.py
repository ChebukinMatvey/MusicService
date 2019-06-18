#!/usr/bin/python3
from api.functions import *
import json
from flask import Flask
from flask import request, make_response
from flask.json import jsonify
app = Flask(__name__)


def process_data(data):
    resp = make_response(jsonify({'result': data}))
    resp.mimetype = 'application/json'
    return resp


@app.route('/track', methods=['POST'])  ## Get songs
def song():
    data = request.get_json(force=True)
    return process_data(get_songs(data['query'],data['username']))


@app.route('/artist', methods=['GET'])  ## Get artist
def artist():
    return process_data(get_artist(request.get_json()['name']))

@app.route('/albums', methods=['GET'])  ## Get all albums of artist by artist name
def albums():
    return process_data(get_albums(request.get_json()['artist']))

@app.route('/album', methods=['GET'])   ## Get album by album id 
def album():
    return process_data(get_album( request.get_json()['id']))


@app.route('/login',methods=['POST'])
def login():
    form = request.form
    user = find_user(form['name'],form['pswd'])
    return process_data(user.name if user else None)


@app.route('/like',methods=['POST'])
def like_post():
    data = request.get_json()
    return process_data(add_like(data['user'],data['song_id']))

@app.route('/like',methods=['DELETE'])
def like_delete():
    data = request.get_json()
    return process_data(delete_like(data['user'],data['song_id']))

@app.route('/user_likes',methods=['POST'])
def user_likes():
    data = request.get_json(force=True)
    res = get_user_likes(data['username'])
    res.reverse()
    return process_data( res )


@app.route('/recommend',methods=['POST'])
def recommend():
    data = request.get_json()
    if 'song_id' in data:
        return process_data(get_recommendations(data['username'],data['song_id']))
    else:
        return process_data(get_recommendations(data['username']))


@app.route('/most_popular',methods=['POST'])
def popular():
    data = request.get_json(force=True)
    return process_data( most_popular(data['username']) )

def main():
    app.run()