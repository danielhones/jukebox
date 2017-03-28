import json
import os

from flask import Flask, url_for, render_template, request, send_from_directory

from jukebox.models import Album, Artist, db, Song
from jukebox.settings import ITUNES_MUSIC_DIRECTORY


db.connect()
app = Flask(__name__)


@app.route('/')
def index():
    songs = Song.all()[:100]
    # sort by artist
    return render_template('index.html', songs=songs)


@app.route('/songs.json')
def page_songs():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    if (start is not None and start < 0) or (start is not None and end is not None and end <= start):
        return json.dumps({'error': 'end must be greater than start and start must be >= 0'}), 400

    if start is None:
        start = 0

    if end is None:
        songs = Song.all()[start:]
    else:
        songs = Song.all()[start:end]
    return json.dumps({i.id: i.attributes for i in songs})
    #return json.dumps([i.attributes for i in songs])


@app.route('/songs/<int:song_id>/file')
def song(song_id):
    try:
        song = Song.get(Song.id == song_id)
    except:
        return "Song not found", 404

    # relative = os.path.relpath(song.location, start=ITUNES_MUSIC_DIRECTORY)
    # return send_from_directory(ITUNES_MUSIC_DIRECTORY, relative)
    return send_from_directory('static', 'untitled.mp3')


@app.route('/search/<query>')
def search(query):
    return query


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
