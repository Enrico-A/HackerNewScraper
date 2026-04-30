from scraper import clean_score


def test_clean_score_extracts_points_from_normal_hacker_news_text():
    # Caso standard: Hacker News mostra il punteggio come "<numero> points".
    assert clean_score("123 points") == 123


def test_clean_score_returns_zero_for_empty_string():
    # Caso senza testo: la funzione deve restare stabile e restituire 0.
    assert clean_score("") == 0


def test_clean_score_handles_unexpected_format_without_digits():
    # Caso anomalo: se non ci sono cifre, non deve sollevare eccezioni.
    assert clean_score("score unavailable") == 0
