from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def index():
    # Sample data:
    songs = [
        {'title': 'Love on top', 'artist': 'Beyonce', 'album': '4'},
        {'title': "What's My Age Again", 'artist': 'Blink 182', 'album': 'Enema of the State'},
        {'title': 'Treasure', 'artist': 'Bruno Mars', 'album': 'Unknown'},
    ]
    return render_template('index.html', songs=songs*20)


@app.route('/song/<int:song_id>')
def song(song_id):
    # Look up location for song_id, return file here
    return url_for('static', filename='untitled.mp3')


@app.route('/search/<query>')
def search(query):
    return query


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
