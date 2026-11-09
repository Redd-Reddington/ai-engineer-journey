"""Tests for word_freq.py (the original version, no --json). Run with:  pytest -v
...(your original docstring stays as is)...
"""

import inspect    # a standard-library module for examining Python objects
import sys        # to fake the command line (sys.argv)

import pytest

import word_freq as word_freq


# ---------- helpers ----------

# A fixture local to this file: builds a small text file and hands its path
# to any test that asks for "sample_file". tmp_path (built in to pytest)
# gives it a temporary folder that is deleted afterwards.
@pytest.fixture
def sample_file(tmp_path):
    """A small text file reused by several tests."""
    f = tmp_path / "sample.txt"
    f.write_text("The cat sat. The cat ran. A dog ran!\n", encoding="utf-8")
    return f


# ---------- generator: iter_words ----------
# A generator produces values one at a time (using yield) instead of building
# a whole list. These tests check both WHAT it yields and THAT it's a generator.

def test_iter_words_is_a_generator():
    # Calling a generator function doesn't run its body yet: it returns a
    # generator object. inspect.isgenerator() checks for that object type.
    assert inspect.isgenerator(word_freq.iter_words(["hello"]))


def test_iter_words_lowercases_and_splits():
    # iter_words takes an iterable of LINES. list(...) pulls every value out
    # of the generator so we can compare against a normal list.
    assert list(word_freq.iter_words(["Hello, World!"])) == ["hello", "world"]


def test_iter_words_keeps_inner_apostrophes_only():
    # "don't" keeps its apostrophe (it's inside the word), but the quote marks
    # around 'quoted' are stripped (they're at the edges).
    assert list(word_freq.iter_words(["don't 'quoted'"])) == ["don't", "quoted"]


def test_iter_words_min_length():
    # Words shorter than 3 letters ("a", "an") are dropped. Note this is
    # NOT the stopword filter: that happens later, in count_words.
    words = list(word_freq.iter_words(["a an the python"], min_length=3))
    assert words == ["the", "python"]


def test_iter_words_ignores_digits_and_punctuation():
    # Only letters count as word characters, so "week1" becomes "week" and
    # the "42" and "--" disappear entirely.
    assert list(word_freq.iter_words(["week1 -- 42"])) == ["week"]


# ---------- context manager: open_text ----------
# A context manager is what makes "with ... as f:" work. Its main promise:
# cleanup ALWAYS happens (here: the file gets closed), even after an error.

def test_open_text_closes_file(sample_file):
    with word_freq.open_text(sample_file) as f:
        assert not f.closed        # inside the with-block: file is open
    # After the block ends, "f" still refers to the file object, so we can
    # check that the context manager closed it.
    assert f.closed


def test_open_text_closes_file_even_after_error(sample_file):
    # pytest.raises wraps the whole with-block, because we EXPECT the error.
    with pytest.raises(ValueError):
        with word_freq.open_text(sample_file) as f:
            raise ValueError("boom")    # simulate something going wrong inside
    # The key promise: the file was closed even though an error happened.
    assert f.closed


def test_open_text_missing_file(tmp_path):
    # The file doesn't exist, so opening it must raise FileNotFoundError.
    with pytest.raises(FileNotFoundError):
        with word_freq.open_text(tmp_path / "nope.txt"):
            pass                        # never reached; the error comes first


# ---------- decorator: timed ----------
# A decorator wraps a function to add behaviour (here: print how long it took).

def test_timed_returns_result_and_keeps_name(capsys):
    # You can define a small function INSIDE a test and decorate it, so the
    # test doesn't depend on any real function in your code.
    @word_freq.timed
    def add(a, b):
        return a + b

    assert add(2, 3) == 5                 # the wrapper still returns the result
    # functools.wraps makes the wrapper copy the original's name. Without it,
    # add.__name__ would be "wrapper".
    assert add.__name__ == "add"
    # capsys recorded what was printed; readouterr().out is stdout.
    assert "[timed] add took" in capsys.readouterr().out


# ---------- analysis ----------

def test_count_words_filters_stopwords(sample_file):
    counts = word_freq.count_words(sample_file)   # default: stopwords removed
    assert counts["cat"] == 2
    # Stopwords like "the" and "a" were filtered out of the Counter.
    assert "the" not in counts and "a" not in counts


def test_count_words_keep_stopwords(sample_file):
    counts = word_freq.count_words(sample_file, use_stopwords=False)
    assert counts["the"] == 2             # now "the" is counted


def test_summarize_totals_and_rows(sample_file):
    counts = word_freq.count_words(sample_file)
    # summarize returns THREE values, unpacked into three variables.
    total, unique, rows = word_freq.summarize(counts, 2)
    assert total == sum(counts.values())  # total = every word occurrence
    assert unique == len(counts)          # unique = number of different words
    assert len(rows) == 2                 # we asked for the top 2 rows
    assert "cat" in rows[0]               # most common word comes first


def test_main_missing_file_exits(monkeypatch, capsys):
    # monkeypatch fakes the command line: python word_freq.py does_not_exist.txt
    monkeypatch.setattr(sys, "argv", ["word_freq.py", "does_not_exist.txt"])
    # sys.exit() raises SystemExit, so pytest.raises can catch it.
    with pytest.raises(SystemExit):
        word_freq.main()