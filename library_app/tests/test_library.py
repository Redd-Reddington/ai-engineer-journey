import pytest

from library_app.library import (
    BookNotFoundError, BookUnavailableError, BorrowLimitError,
    DuplicateError, Library, LibraryError, MemberNotFoundError,
)
from library_app.models import Book, EBook, Member


# ---------- models ----------

@pytest.mark.parametrize("make", [
    lambda: Book("", "T", "A", 2000),
    lambda: Book("1", "  ", "A", 2000),
    lambda: Book("1", "T", "A", 2999),
    lambda: EBook("1", "T", "A", 2000, -1),
    lambda: EBook("1", "T", "A", 2000, 0),
    lambda: Member(1, "  ", "x@example.com"),
])
def test_invalid_objects_rejected(make):
    with pytest.raises(ValueError):
        make()


def test_member_repr_hides_email():
    assert "alice@example.com" not in repr(Member(1, "Alice", "alice@example.com"))


def test_members_do_not_share_borrowed_list():
    a, b = Member(1, "A", "a@x.com"), Member(2, "B", "b@x.com")
    a.borrowed.append(Book("1", "T", "A", 2000))
    assert b.borrowed == []


def test_ebook_is_a_book_and_str_mentions_size():
    e = EBook("1", "Dune", "Herbert", 1965, 2.4)
    assert isinstance(e, Book)
    assert "2.4 MB" in str(e)


# ---------- records ----------

def test_duplicate_book_rejected(lib):
    with pytest.raises(DuplicateError):
        lib.add_book(Book("111", "Other", "Someone", 2000))


def test_duplicate_member_rejected(lib):
    with pytest.raises(DuplicateError):
        lib.register_member(Member(1, "Alice 2", "a2@example.com"))


# ---------- checkout / return ----------

def test_checkout_updates_both_sides(lib):
    book = lib.checkout(1, "111")
    assert book.isbn == "111"
    assert book in lib.members()[0].borrowed
    assert "111" not in [b.isbn for b in lib.available_books()]


def test_return_restores_availability(lib):
    lib.checkout(1, "111")
    lib.return_book(1, "111")
    assert "111" in [b.isbn for b in lib.available_books()]
    assert lib.members()[0].borrowed == []


@pytest.mark.parametrize("member_id, isbn, error", [
    (99, "111", MemberNotFoundError),
    (1, "000", BookNotFoundError),
])
def test_checkout_failures(lib, member_id, isbn, error):
    with pytest.raises(error):
        lib.checkout(member_id, isbn)


def test_cannot_checkout_book_already_on_loan(lib):
    lib.checkout(1, "111")
    with pytest.raises(BookUnavailableError):
        lib.checkout(2, "111")


def test_borrow_limit(lib):
    for isbn in ("111", "222", "333"):
        lib.checkout(1, isbn)
    with pytest.raises(BorrowLimitError):
        lib.checkout(1, "444")


def test_failed_checkout_changes_nothing(lib):
    for isbn in ("111", "222", "333"):
        lib.checkout(1, isbn)
    with pytest.raises(BorrowLimitError):
        lib.checkout(1, "444")
    assert len(lib.members()[0].borrowed) == 3
    assert "444" in [b.isbn for b in lib.available_books()]


@pytest.mark.parametrize("member_id, isbn", [
    (2, "111"),   # someone else has it
    (1, "222"),   # nobody has it
    (1, "000"),   # unknown isbn
])
def test_return_failures(lib, member_id, isbn):
    lib.checkout(1, "111")
    with pytest.raises(BookUnavailableError):
        lib.return_book(member_id, isbn)


def test_all_errors_share_base_class():
    for err in (BookNotFoundError, MemberNotFoundError, DuplicateError,
                BookUnavailableError, BorrowLimitError):
        assert issubclass(err, LibraryError)


# ---------- queries and dunders ----------

def test_search_matches_title_or_author_case_insensitive(lib):
    assert {b.isbn for b in lib.search("ROALD")} == {"222", "333"}
    assert {b.isbn for b in lib.search("hobbit")} == {"111"}
    assert lib.search("zzz") == []


def test_dunder_methods(lib):
    assert len(lib) == 4
    assert "111" in lib
    assert lib["111"] in lib
    assert "000" not in lib
    assert len(list(lib)) == 4
    with pytest.raises(KeyError):
        lib["000"]
    assert "4 books" in str(lib)
