"""
Tests for library_system.py.

Pytest collects any file named test_*.py, and inside it any function named
test_*. A test PASSES if it finishes without an error and FAILS if an assert
is false or an unexpected exception is raised.
"""

import pytest
from dataclasses import FrozenInstanceError
from library_system import (
    Book, EBook, Member,
    BookNotFoundError, MemberNotFoundError, DuplicateError,
    BookUnavailableError, BorrowLimitError,
)


# =====================================================================
# checkout / return
# =====================================================================

# "library" and "member" are fixtures from conftest.py: pytest sees the
# parameter names and builds both objects automatically.
def test_checkout_records_loan_on_both_sides(library, member):
    book = library.checkout(1, "111")           # ACT: member 1 borrows Dune

    assert book.title == "Dune"                 # checkout returned the right book
    assert book in member.borrowed              # member side of the loan recorded
    assert book not in library.available_books()  # library side recorded too


# parametrize runs this ONE test function once per row below, so it counts as
# 2 tests. The first argument names the parameters; each tuple is one run.
# ids= gives each run a readable name, so a failure shows
# "test_checkout_errors[unknown-member]" instead of "[99-111-MemberNot...]".
@pytest.mark.parametrize("member_id, isbn, error", [
    (99, "111", MemberNotFoundError),           # member 99 doesn't exist
    (1, "000", BookNotFoundError),              # ISBN 000 doesn't exist
], ids=["unknown-member", "unknown-book"])
def test_checkout_errors(library, member, member_id, isbn, error):
    # pytest.raises(X) passes ONLY if the code inside raises X.
    # If no error is raised, or a different one is, the test fails.
    with pytest.raises(error):
        library.checkout(member_id, isbn)


def test_borrow_limit(library, member):
    for isbn in ("111", "222", "333"):          # ARRANGE: reach the limit of 3
        library.checkout(1, isbn)

    # match= also checks the error MESSAGE (it's a regex search), so we know
    # it's the limit error and carries the right text.
    with pytest.raises(BorrowLimitError, match="already has 3 books"):
        library.checkout(1, "444")              # a 4th book must be refused


def test_book_already_on_loan(library, member):
    other = Member(2, "Kofi", "kofi@example.com")   # a second person
    library.register_member(other)
    library.checkout(1, "111")                  # Ama takes Dune
    with pytest.raises(BookUnavailableError):
        library.checkout(2, "111")              # Kofi can't take it too


def test_return_book(library, member):
    library.checkout(1, "111")
    library.return_book(1, "111")

    assert member.borrowed == []                # member's side undone
    assert len(library.available_books()) == 4  # all 4 books free again


def test_return_book_not_held(library, member):
    # Ama never borrowed 111, so returning it must raise an error.
    with pytest.raises(BookUnavailableError):
        library.return_book(1, "111")


# =====================================================================
# registering books and members
# =====================================================================

def test_duplicate_book_rejected(library):
    # ISBN "111" already exists from the fixture, so adding it again fails.
    with pytest.raises(DuplicateError):
        library.add_book(Book("111", "Other", "Someone", 2000))


def test_duplicate_member_rejected(library, member):
    # member_id 1 is already registered by the member fixture.
    with pytest.raises(DuplicateError):
        library.register_member(Member(1, "Copy", "copy@example.com"))


# =====================================================================
# queries and dunder methods
# =====================================================================

@pytest.mark.parametrize("isbn, expected", [
    ("111", True),                              # in the library
    ("222", True),
    ("999", False),                             # not in the library
], ids=["dune", "emma", "missing"])
def test_contains(library, isbn, expected):
    # "isbn in library" calls Library.__contains__ behind the scenes.
    assert (isbn in library) == expected


@pytest.mark.parametrize("keyword, count", [
    ("dune", 1),                                # matches a title
    ("AUSTEN", 1),                              # capitals still match an author
    ("the", 1),                                 # partial match: "The Hobbit"
    ("zzz", 0),                                 # nothing matches
], ids=["title", "author-caps", "partial", "no-match"])
def test_search(library, keyword, count):
    assert len(library.search(keyword)) == count


def test_len_and_getitem(library):
    assert len(library) == 4                    # __len__
    assert library["111"].title == "Dune"       # __getitem__
    with pytest.raises(KeyError):               # a bad key raises KeyError
        library["000"]


def test_iter_yields_all_books(library):
    # "for b in library" calls __iter__. Books come back in insertion order.
    assert [b.isbn for b in library] == ["111", "222", "333", "444"]


def test_contains_accepts_book_object(library):
    # __contains__ accepts a Book object as well as an ISBN string.
    assert library["111"] in library


def test_library_str_summary(library, member):
    library.checkout(1, "111")
    # str(library) calls __str__: name, books, members, loans.
    assert str(library) == "Test Library: 4 books, 1 members, 1 on loan"


# =====================================================================
# dataclass validation (Book, EBook, Member)
# =====================================================================

# Each row has the arguments for Book(...) plus the error text we expect.
# "*args" below unpacks the tuple into separate arguments.
@pytest.mark.parametrize("args, message", [
    (("", "Title", "Author", 2000), "ISBN cannot be empty"),
    (("1", "   ", "Author", 2000), "Title cannot be empty"),
    (("1", "Title", "Author", 2999), "future"),
], ids=["blank-isbn", "blank-title", "future-year"])
def test_book_validation(args, message):
    with pytest.raises(ValueError, match=message):
        Book(*args)                             # __post_init__ should reject it


def test_ebook_rejects_non_positive_size():
    with pytest.raises(ValueError, match="positive"):
        EBook("1", "T", "A", 2000, file_size_mb=0)


def test_ebook_str_includes_size():
    e = EBook("5", "Dune", "Herbert", 1965, file_size_mb=2.4)
    # EBook.__str__ reuses Book's text and adds the eBook part.
    assert str(e) == "'Dune' by Herbert (1965) [eBook, 2.4 MB]"


def test_member_blank_name_rejected():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Member(3, "  ", "x@example.com")


def test_member_repr_hides_email(member):
    # The email field uses repr=False, so it must not appear in repr().
    assert "ama@example.com" not in repr(member)


def test_can_borrow_flips_at_limit(library, member):
    assert member.can_borrow                    # 0 books: allowed
    for isbn in ("111", "222", "333"):
        library.checkout(1, isbn)
    assert not member.can_borrow                # 3 books: at the limit


def test_book_is_frozen(library):
    # frozen=True means changing a field raises FrozenInstanceError.
    with pytest.raises(FrozenInstanceError):
        library["111"].title = "Changed"