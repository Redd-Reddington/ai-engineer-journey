"""Tests for word_freq.py (the original version, no --json). Run with:  pytest -v

pytest finds functions that start with `test_` and runs them.
Each test uses `assert`: if the statement is False, the test fails.
Special arguments are "fixtures" pytest provides automatically:
  tmp_path -> a fresh temporary folder
  capsys   -> captures what the program prints
  monkeypatch -> lets us temporarily change things (like sys.argv)
"""

import inspect
import sys

import pytest

import word_freq


# ---------- helpers ----------
@pytest.fixture
def sample_file(tmp_path):
    """A small text file reused by several tests."""
    f = tmp_path / "sample.txt"
    f.write_text("The cat sat. The cat ran. A dog ran!\n", encoding="utf-8")
    return f


# ---------- generator: iter_words ----------
def test_iter_words_is_a_generator():
    assert inspect.isgenerator(word_freq.iter_words(["hello"]))


def test_iter_words_lowercases_and_splits():
    assert list(word_freq.iter_words(["Hello, World!"])) == ["hello", "world"]


def test_iter_words_keeps_inner_apostrophes_only():
    assert list(word_freq.iter_words(["don't 'quoted'"])) == ["don't", "quoted"]


def test_iter_words_min_length():
    words = list(word_freq.iter_words(["a an the python"], min_length=3))
    assert words == ["the", "python"]


def test_iter_words_ignores_digits_and_punctuation():
    assert list(word_freq.iter_words(["week1 -- 42"])) == ["week"]


# ---------- context manager: open_text ----------
def test_open_text_closes_file(sample_file):
    with word_freq.open_text(sample_file) as f:
        assert not f.closed
    assert f.closed


def test_open_text_closes_file_even_after_error(sample_file):
    with pytest.raises(ValueError):
        with word_freq.open_text(sample_file) as f:
            raise ValueError("boom")
    assert f.closed


def test_open_text_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        with word_freq.open_text(tmp_path / "nope.txt"):
            pass


# ---------- decorator: timed ----------
def test_timed_returns_result_and_keeps_name(capsys):
    @word_freq.timed
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add.__name__ == "add"          # thanks to functools.wraps
    assert "[timed] add took" in capsys.readouterr().out


# ---------- analysis ----------
def test_count_words_filters_stopwords(sample_file):
    counts = word_freq.count_words(sample_file)
    assert counts["cat"] == 2
    assert "the" not in counts and "a" not in counts


def test_count_words_keep_stopwords(sample_file):
    counts = word_freq.count_words(sample_file, use_stopwords=False)
    assert counts["the"] == 2


def test_summarize_totals_and_rows(sample_file):
    counts = word_freq.count_words(sample_file)
    total, unique, rows = word_freq.summarize(counts, 2)
    assert total == sum(counts.values())
    assert unique == len(counts)
    assert len(rows) == 2
    assert "cat" in rows[0]               # most common word comes first


def test_main_missing_file_exits(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq.py", "does_not_exist.txt"])
    with pytest.raises(SystemExit):
        word_freq.main()
