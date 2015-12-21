from flask import Flask, url_for, render_template
app = Flask(__name__)


@app.route('/')
def index():
    songs = [
        {'title': 'Love on top', 'artist': 'Beyonce'},
        {'title': "What's My Age Again", 'artist': 'Blink 182'},
        {'title': 'Treasure', 'artist': 'Bruno Mars'},
    ]
    return render_template('index.html', songs=songs)


@app.route('/song/<int:song_id>')
def song(song_id):
    return str(song_id)


if __name__ == '__main__':
    app.run()
