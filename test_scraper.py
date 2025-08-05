import requests
from types import SimpleNamespace

from scraper import search_song, fetch_song


def test_search_song_empty_query():
    assert search_song('') == []


def test_search_song_nonsense_returns_empty(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        html = "<html><body>No results</body></html>"
        return SimpleNamespace(text=html, raise_for_status=lambda: None)
    monkeypatch.setattr(requests, "get", fake_get)
    assert search_song("nonsensezzz") == []


def test_fetch_song_http_error_returns_none(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        raise requests.RequestException
    monkeypatch.setattr(requests, "get", fake_get)
    assert fetch_song("http://example.com/404") is None


def test_fetch_song_no_cifra_elements_returns_none(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        html = "<html><body><div>no chords</div></body></html>"
        return SimpleNamespace(text=html, raise_for_status=lambda: None)
    monkeypatch.setattr(requests, "get", fake_get)
    assert fetch_song("http://example.com/no_chords") is None


def test_fetch_song_preserves_alignment(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        html = "<pre>C      G\nLetra de prueba</pre>"
        return SimpleNamespace(text=html, raise_for_status=lambda: None)
    monkeypatch.setattr(requests, "get", fake_get)
    content = fetch_song("http://example.com/song")
    assert content == "C      G\nLetra de prueba"


def test_fetch_song_fallback_cifra_class(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        html = '<span class="cifra-blah">C F G<br>Letra de prueba</span>'
        return SimpleNamespace(text=html, raise_for_status=lambda: None)
    monkeypatch.setattr(requests, "get", fake_get)
    content = fetch_song("http://example.com/custom_layout")
    assert content == "C F G\nLetra de prueba"
