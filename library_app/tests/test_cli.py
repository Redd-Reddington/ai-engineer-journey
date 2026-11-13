import pytest
from typer.testing import CliRunner

from library_app.cli import app

runner = CliRunner()


@pytest.fixture
def db(tmp_path):
    return str(tmp_path / "lib.json")


def run(db, *args):
    return runner.invoke(app, [*args, "--db", db])


@pytest.fixture
def seeded(db):
    run(db, "add-book", "111", "The Hobbit", "Tolkien", "1937")
    run(db, "add-ebook", "444", "Dune", "Herbert", "1965", "2.4")
    run(db, "register", "1", "Alice", "alice@example.com")
    run(db, "register", "2", "Bob", "bob@example.com")
    return db


def test_add_book_success_and_duplicate(db):
    ok = run(db, "add-book", "111", "The Hobbit", "Tolkien", "1937")
    assert ok.exit_code == 0 and "Added" in ok.output
    dup = run(db, "add-book", "111", "Again", "Someone", "2000")
    assert dup.exit_code == 1 and "already exists" in dup.output


def test_add_book_invalid_year(db):
    result = run(db, "add-book", "1", "Future", "Nobody", "2999")
    assert result.exit_code == 1 and "future" in result.output


def test_add_ebook_success_and_bad_size(db):
    assert run(db, "add-ebook", "1", "Dune", "Herbert", "1965", "2.4").exit_code == 0
    bad = run(db, "add-ebook", "2", "Bad", "Nobody", "2000", "0")
    assert bad.exit_code == 1 and "positive" in bad.output


def test_register_success_and_duplicate(db):
    assert run(db, "register", "1", "Alice", "a@x.com").exit_code == 0
    assert run(db, "register", "1", "Alice", "a@x.com").exit_code == 1


def test_checkout_success_persists_between_runs(seeded):
    ok = run(seeded, "checkout", "1", "111")
    assert ok.exit_code == 0 and "Checked out" in ok.output
    # a separate invocation must see the loan
    again = run(seeded, "checkout", "2", "111")
    assert again.exit_code == 1 and "already checked out" in again.output


def test_checkout_unknown_member(seeded):
    result = run(seeded, "checkout", "99", "111")
    assert result.exit_code == 1 and "No member" in result.output


def test_return_success_and_failure(seeded):
    run(seeded, "checkout", "1", "111")
    assert run(seeded, "return", "1", "111").exit_code == 0
    bad = run(seeded, "return", "1", "111")
    assert bad.exit_code == 1 and "does not have" in bad.output


def test_search(seeded):
    hit = run(seeded, "search", "hobbit")
    assert hit.exit_code == 0 and "The Hobbit" in hit.output
    miss = run(seeded, "search", "zzz")
    assert "No matches" in miss.output


def test_available_excludes_loaned_books(seeded):
    run(seeded, "checkout", "1", "111")
    result = run(seeded, "available")
    assert "Dune" in result.output and "Hobbit" not in result.output
