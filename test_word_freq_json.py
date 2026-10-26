"""Tests for word_freq_json.py (the copy that adds --json).

The core behaviour is tested in test_word_freq.py. This file only covers
what is different in the JSON edition, plus one check that both versions
agree on the counts.
"""

import json
import sys

import pytest

import word_freq
import word_freq_json


@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("The cat sat. The cat ran. A dog ran!\n", encoding="utf-8")
    return f


def test_both_versions_count_the_same(sample_file):
    assert word_freq.count_words(sample_file) == word_freq_json.count_words(sample_file)


def test_to_json_structure(sample_file):
    counts = word_freq_json.count_words(sample_file)
    data = json.loads(word_freq_json.to_json(counts, 2))
    total = sum(counts.values())
    assert data["total_words"] == total
    assert data["unique_words"] == len(counts)
    assert len(data["top"]) == 2
    assert data["top"][0] == {"word": "cat", "count": 2,
                              "percent": round(2 / total * 100, 2)}


def test_main_json_stdout_is_pure_json(sample_file, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file), "--json"])
    word_freq_json.main()
    out = capsys.readouterr().out
    assert json.loads(out)["top"][0]["word"] == "cat"


def test_status_lines_go_to_stderr(sample_file, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file), "--json"])
    word_freq_json.main()
    err = capsys.readouterr().err
    assert "[open]" in err and "[close]" in err and "[timed]" in err


def test_without_flag_prints_table(sample_file, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file)])
    word_freq_json.main()
    out = capsys.readouterr().out
    assert "Total words:" in out


def test_missing_file_exits(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", "does_not_exist.txt"])
    with pytest.raises(SystemExit):
        word_freq_json.main()
