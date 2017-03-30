import json
import os
import time

from flask import Flask, url_for, render_template, request, send_from_directory
from playhouse.shortcuts import model_to_dict

from jukebox.models import Album, Artist, db, Song
from jukebox.settings import ITUNES_MUSIC_DIRECTORY


db.connect()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/songs.json')
def all_songs():
    # check for cached json file first, serve if exists
    #songs = Song.select().join(Album).join(Artist).order_by(Artist.name, Album.title, Song.track_number)
    songs = Song.select().join(Album).join(Artist).order_by(Artist.name, Album.title)
    x = time.time()
    r = json.dumps(
        {i.id: model_to_dict(i, exclude='location', extra_attrs=['formatted_length', 'artist_name', 'album_title']) for i in songs}
    )
    print("TOOK THIS LONG:", time.time() - x)
    return r


@app.route('/songs/<int:song_id>/file')
def song(song_id):
    try:
        song = Song.get(Song.id == song_id)
    except:
        return "song not found", 404

    full_path = os.path.join('/', song.location)
    relative = os.path.relpath(full_path, start=ITUNES_MUSIC_DIRECTORY)
    return send_from_directory(ITUNES_MUSIC_DIRECTORY, relative)


@app.route('/search/<query>')
def search(query):
    return query


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
