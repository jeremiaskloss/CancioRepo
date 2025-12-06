import pytest

from cifraclub_cli import parse_chords, parse_search_results, Song


SEARCH_HTML = """
<html><body>
<ul>
<li><a href="/legiao-urbana/tempo-perdido/">Tempo Perdido</a></li>
<li><a href="/legiao-urbana/tempo-perdido/">Duplicado</a></li>
<li><a href="/legiao-urbana/sera/">Será</a></li>
<li><a href="/invalid/url">Ignorar</a></li>
</ul>
</body></html>
"""


CHORDS_PRE_HTML = """
<pre>Intro: C G Am F\nVerso: C G</pre>
"""


CHORDS_DIV_HTML = """
<div class="cifra_centro">[C]Intro [G]Verso</div>
"""


def test_parse_search_results_returns_unique_songs():
    results = list(parse_search_results(SEARCH_HTML))
    assert results == [
        Song(title="Tempo Perdido", url="https://www.cifraclub.com.br/legiao-urbana/tempo-perdido/"),
        Song(title="Será", url="https://www.cifraclub.com.br/legiao-urbana/sera/"),
    ]


def test_parse_chords_prefers_pre_block():
    text = parse_chords(CHORDS_PRE_HTML)
    assert "Intro" in text and "Verso" in text


def test_parse_chords_handles_div_variants():
    text = parse_chords(CHORDS_DIV_HTML)
    assert "Intro" in text
