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
    return process_data(get_songs(request.get_json(force=True)['name']))


@app.route('/artist', methods=['GET'])  ## Get artist
def artist():
    return process_data(get_artist(request.get_json()['name']))


@app.route('/stream', methods=['POST'])  ## Get song stream
def stream():
    return process_data(get_stream(request.get_json()['id']))


@app.route('/albums', methods=['GET'])  ## Get all albums of artist by artist name
def albums():
    # TODO abums and album edpoints are hell
    return process_data(get_albums(request.get_json()['artist']))


@app.route('/album', methods=['GET'])   ## Get album by album id 
def album():
    return process_data(get_album( request.get_json()['id']))


def main():
    app.run()