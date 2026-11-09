"""Tests for word_freq_json.py (the copy that adds --json).

The core behaviour is tested in test_word_freq.py. This file only covers
what is different in the JSON edition, plus one check that both versions
agree on the counts.
"""

import json      # to parse the JSON text our program prints
import sys       # to fake the command line (sys.argv)

import pytest

import word_freq as word_freq    # (the "as word_freq" is redundant: same name)
import word_freq_json


# A fixture defined INSIDE this file: only tests in this file can use it.
# (Fixtures in conftest.py are shared by every file; this one is local.)
# It creates a small text file and hands its path to any test that asks.
@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("The cat sat. The cat ran. A dog ran!\n", encoding="utf-8")
    return f


# A "consistency" test: two separate implementations should agree.
# If someone edits one copy and forgets the other, this fails.
def test_both_versions_count_the_same(sample_file):
    assert word_freq.count_words(sample_file) == word_freq_json.count_words(sample_file)


def test_to_json_structure(sample_file):
    counts = word_freq_json.count_words(sample_file)   # ARRANGE: a Counter

    # ACT: to_json(counts, 2) returns TEXT. json.loads turns that text back
    # into a Python dict so we can inspect it. If the text were not valid
    # JSON, loads would raise an error and the test would fail.
    data = json.loads(word_freq_json.to_json(counts, 2))

    # ASSERT: each field matches what we compute independently from counts.
    total = sum(counts.values())
    assert data["total_words"] == total
    assert data["unique_words"] == len(counts)
    assert len(data["top"]) == 2                       # we asked for top 2

    # The top entry should be "cat" with 2 occurrences. The percent is
    # recalculated here with the same formula the program uses.
    assert data["top"][0] == {"word": "cat", "count": 2,
                              "percent": round(2 / total * 100, 2)}


# main() reads the command line, so the test must FAKE one.
#   monkeypatch: a built-in fixture that temporarily changes something and
#                automatically puts it back after the test.
#   capsys:      a built-in fixture that captures everything the program
#                prints, so the test can read it afterwards.
def test_main_json_stdout_is_pure_json(sample_file, monkeypatch, capsys):
    # Pretend the user typed:  python word_freq_json.py sample.txt --json
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file), "--json"])

    word_freq_json.main()                              # ACT: run the program

    out = capsys.readouterr().out                      # .out = what went to stdout
    # If anything other than JSON was printed to stdout, json.loads fails.
    # That matters because other programs may read this output.
    assert json.loads(out)["top"][0]["word"] == "cat"


# stdout = the program's real OUTPUT.  stderr = status/diagnostic messages.
# Keeping them separate means "--json > result.json" saves clean JSON, while
# the [open]/[close]/[timed] messages still show on screen.
def test_status_lines_go_to_stderr(sample_file, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file), "--json"])
    word_freq_json.main()
    err = capsys.readouterr().err                      # .err = what went to stderr
    # Messages from your context manager ([open]/[close]) and the @timed
    # decorator ([timed]) must all be in stderr.
    assert "[open]" in err and "[close]" in err and "[timed]" in err


# Same fake command line but WITHOUT --json: the normal table should print.
def test_without_flag_prints_table(sample_file, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", str(sample_file)])
    word_freq_json.main()
    out = capsys.readouterr().out
    assert "Total words:" in out


# sys.exit() raises a SystemExit exception, so pytest.raises can catch it.
# Without this, the exit would stop the whole test run.
def test_missing_file_exits(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["word_freq_json.py", "does_not_exist.txt"])
    with pytest.raises(SystemExit):
        word_freq_json.main()