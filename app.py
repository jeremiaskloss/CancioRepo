from __future__ import annotations

from flask import Flask, request, render_template

from cifraclub import search_songs, fetch_song
from urllib.parse import urlparse
from typing import Optional

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
    url: Optional[str] = request.args.get('url')
    title_param: Optional[str] = request.args.get('title')

    # Normalize and validate title
    if not isinstance(title_param, str) or not title_param.strip():
        title = 'Canción'
    else:
        title = title_param.strip()

    chords = None
    error = None

    # Validate URL parameter
    if not isinstance(url, str) or not url.strip():
        error = 'Falta la URL de la canción.'
    else:
        parsed = urlparse(url.strip())
        if parsed.scheme not in ('http', 'https') or 'cifraclub.com' not in parsed.netloc:
            error = 'URL inválida. Debe pertenecer a CifraClub.'

    if not error:
        chords = fetch_song(url.strip())

    return render_template('song.html', title=title, chords=chords, error=error)


if __name__ == '__main__':
    app.run(debug=True)
