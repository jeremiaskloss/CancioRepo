from __future__ import annotations

from flask import Flask, request, render_template

from cifraclub import search_songs, fetch_song

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    results = []
    if request.method == 'POST':
        query = request.form.get('q', '').strip()
        if query:
            results = search_songs(query)
    return render_template('index.html', query=query, results=results)


@app.route('/song')
def song():
    url = request.args.get('url')
    title = request.args.get('title', 'Canción')
    chords = None
    if url:
        chords = fetch_song(url)
    return render_template('song.html', title=title, chords=chords)


if __name__ == '__main__':
    app.run(debug=True)
