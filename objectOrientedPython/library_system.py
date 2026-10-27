"""
Library system: dataclasses + inheritance + composition + dunder methods.

Concepts used:
  - @dataclass (frozen=True)      -> Book, EBook (immutable data)
  - field(repr=False)             -> Member.email stays out of the printed repr
  - __post_init__                 -> validation right after an object is created
  - Inheritance (is-a)            -> EBook(Book)
  - Composition (has-a / owns-a)  -> Library owns books, members and loans
  - Dunder methods                -> __len__, __iter__, __contains__, __getitem__, __str__

How the pieces fit together:
  Book / EBook  -> plain data about a book (what it is)
  Member        -> plain data about a person (who they are, what they hold)
  Library       -> the logic: who may borrow what, and the rules around it
"""

from dataclasses import dataclass, field, FrozenInstanceError
from datetime import date
from typing import ClassVar, Iterator


# =====================================================================
# Custom exceptions
# =====================================================================
# Every library problem gets its own exception type, so calling code can
# react to each one specifically (or catch LibraryError to catch them all).
# Returning error strings instead would hide bugs; raising forces the
# caller to deal with the problem.

class LibraryError(Exception):
    """Base class for all library errors. Catch this to catch any of them."""


class BookNotFoundError(LibraryError):
    """The ISBN doesn't exist in the library."""


class MemberNotFoundError(LibraryError):
    """The member id doesn't exist in the library."""


class DuplicateError(LibraryError):
    """Tried to add a book or member that is already registered."""


class BookUnavailableError(LibraryError):
    """The book is already on loan (or the member doesn't hold it)."""


class BorrowLimitError(LibraryError):
    """The member already has the maximum number of books."""


# =====================================================================
# Data classes: these only HOLD data, so @dataclass writes
# __init__, __repr__ and __eq__ for us.
# =====================================================================

# frozen=True makes instances immutable: once a Book is created, nobody can
# change its title or year. It also makes Book hashable (usable in sets and
# as dict keys), because frozen + eq auto-generates __hash__.
@dataclass(frozen=True)
class Book:
    isbn: str      # unique id for the book; the Library uses it as the lookup key
    title: str
    author: str
    year: int

    # Dataclasses call __post_init__ automatically right after the generated
    # __init__ finishes. It's the place to validate the values.
    def __post_init__(self):
        if not self.isbn.strip():           # .strip() so "   " counts as empty
            raise ValueError("ISBN cannot be empty")
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if self.year > date.today().year:   # a book can't be published in the future
            raise ValueError("Publication year cannot be in the future")

    # __str__ is the friendly version used by print(); __repr__ (auto-generated
    # by the dataclass) is the developer version.
    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"


# EBook inherits from Book (EBook "is a" Book), so it gets isbn, title, author
# and year for free and only adds what is new.
# A child of a frozen dataclass must also be frozen, otherwise Python raises an error.
@dataclass(frozen=True)
class EBook(Book):
    file_size_mb: float    # the only new field; fields are ordered parent first

    def __post_init__(self):
        # super() runs the parent's validation (isbn/title/year) first, so we
        # don't copy that code. Skipping this call would silently drop those checks.
        super().__post_init__()
        if self.file_size_mb <= 0:
            raise ValueError("File size must be positive")

    def __str__(self):
        # Reuse the parent's text and add the eBook-specific part.
        return f"{super().__str__()} [eBook, {self.file_size_mb} MB]"


# Not frozen: a Member changes over time (they borrow and return books).
@dataclass
class Member:
    member_id: int
    name: str
    # repr=False keeps the email out of print(member) and logs, the same trick
    # as the password field in your Person notes.
    email: str = field(repr=False)
    # Mutable defaults like [] are not allowed directly; default_factory makes
    # a brand-new list for every Member, so members never share one list.
    borrowed: list[Book] = field(default_factory=list)
    # default_factory runs date.today() when each Member is created
    joined: date = field(default_factory=date.today)

    # ClassVar marks this as a class variable, NOT a dataclass field: it is
    # shared by every Member and doesn't appear in __init__ or __repr__.
    MAX_LOANS: ClassVar[int] = 3

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

    # A property is read like an attribute (member.can_borrow, no brackets)
    # but computed fresh each time from the current list.
    @property
    def can_borrow(self) -> bool:
        return len(self.borrowed) < self.MAX_LOANS


# =====================================================================
# Library: a regular class, because it has behaviour (rules and actions),
# not just data.
# =====================================================================

class Library:
    """A Library HAS books, members and loans (composition)."""

    def __init__(self, name: str):
        self.name = name
        # Dicts give instant lookup by key. The leading underscore signals
        # "internal": outside code should use the methods, not touch these.
        self._books: dict[str, Book] = {}      # isbn -> Book
        self._members: dict[int, Member] = {}  # member_id -> Member
        self._loans: dict[str, int] = {}       # isbn -> id of the member holding it
        # A book is "on loan" exactly when its ISBN is a key in _loans.

    # ----- managing records -----

    def add_book(self, book: Book) -> None:
        # Refuse duplicates so one ISBN can never point at two different books.
        if book.isbn in self._books:
            raise DuplicateError(f"Book {book.isbn} already exists")
        self._books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise DuplicateError(f"Member {member.member_id} already exists")
        self._members[member.member_id] = member

    def _get_member(self, member_id: int) -> Member:
        # Helper so checkout and return_book share one "find member" step.
        try:
            return self._members[member_id]
        except KeyError:
            # "from None" hides the raw KeyError so the user only sees our message.
            raise MemberNotFoundError(f"No member with id {member_id}") from None

    # ----- core actions -----

    def checkout(self, member_id: int, isbn: str) -> Book:
        member = self._get_member(member_id)    # raises if the member is unknown

        # Validate everything BEFORE changing any data. If a check fails we
        # raise, and nothing has been modified, so the library stays consistent.
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        if isbn in self._loans:                 # someone already has it
            raise BookUnavailableError(f"{self._books[isbn]} is already checked out")
        if not member.can_borrow:               # at the 3-book limit
            raise BorrowLimitError(
                f"{member.name} already has {Member.MAX_LOANS} books"
            )

        # All checks passed: record the loan in BOTH places so they stay in sync.
        book = self._books[isbn]
        self._loans[isbn] = member_id           # library side: who has this book
        member.borrowed.append(book)            # member side: what they hold
        return book

    def return_book(self, member_id: int, isbn: str) -> Book:
        member = self._get_member(member_id)

        # .get() returns None for an unknown ISBN instead of raising, so this
        # one check covers both "book isn't on loan" and "someone else has it".
        if self._loans.get(isbn) != member_id:
            raise BookUnavailableError(f"{member.name} does not have book {isbn}")

        book = self._books[isbn]
        member.borrowed.remove(book)            # undo both sides of the loan
        del self._loans[isbn]
        return book

    # ----- queries -----

    def search(self, keyword: str) -> list[Book]:
        keyword = keyword.lower()               # lowercase both sides = case-insensitive
        # List comprehension: keep each book whose title OR author contains the keyword.
        return [
            b for b in self._books.values()
            if keyword in b.title.lower() or keyword in b.author.lower()
        ]

    def available_books(self) -> list[Book]:
        # Available = in the catalogue but not currently in the loans dict.
        return [b for isbn, b in self._books.items() if isbn not in self._loans]

    # ----- dunder methods: let a Library behave like a built-in collection -----

    def __len__(self) -> int:
        # Called by len(library)
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        # Called by "for book in library"; we hand back an iterator over the books.
        return iter(self._books.values())

    def __contains__(self, item) -> bool:
        # Called by "x in library". Accepts a Book object or a plain ISBN string.
        isbn = item.isbn if isinstance(item, Book) else item
        return isbn in self._books

    def __getitem__(self, isbn: str) -> Book:
        # Called by library["111"]. Raises KeyError for a bad key, like a real dict.
        try:
            return self._books[isbn]
        except KeyError:
            raise KeyError(f"No book with ISBN {isbn}") from None

    def __str__(self) -> str:
        # Called by print(library): a one-line summary.
        return (
            f"{self.name}: {len(self._books)} books, "
            f"{len(self._members)} members, {len(self._loans)} on loan"
        )


# =====================================================================
# Demo: runs only when you execute this file directly
# (python library_system.py), not when another file imports it.
# =====================================================================

if __name__ == "__main__":
    lib = Library("City Library")

    # Stock the shelves. The Dune entry is an EBook, which works anywhere a
    # Book is expected, because an EBook is a Book.
    lib.add_book(Book("111", "The Hobbit", "J.R.R. Tolkien", 1937))
    lib.add_book(Book("222", "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997))
    lib.add_book(Book("333", "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 1950))
    lib.add_book(EBook("444", "Dune", "Frank Herbert", 1965, file_size_mb=2.4))
    lib.add_book(Book("555", "Matilda", "Roald Dahl", 1988))

    alice = Member(1, "Alice", "alice@example.com")
    bob = Member(2, "Bob", "bob@example.com")
    lib.register_member(alice)
    lib.register_member(bob)

    # Dunder methods in action
    print(lib)                                   # __str__
    print(alice)                                 # dataclass repr; note: no email shown
    print(f"Books in library: {len(lib)}")       # __len__
    print("Has ISBN 111?", "111" in lib)         # __contains__
    print("Lookup 444:", lib["444"])             # __getitem__

    print("\nSearch 'the':")
    for book in lib.search("the"):
        print("  ", book)

    # Alice borrows up to her limit of 3
    print("\nCheckouts:")
    lib.checkout(1, "111")
    lib.checkout(1, "222")
    lib.checkout(1, "333")
    print(f"  Alice has {len(alice.borrowed)} books")

    # Small helper: run an action, and print either OK or the error it raised.
    # This shows how the custom exceptions let us handle each failure clearly.
    def attempt(label, fn, *args):
        try:
            fn(*args)
            print(f"  {label}: OK")
        except LibraryError as e:                # one except catches every library error
            print(f"  {label}: {type(e).__name__} -> {e}")

    # Each call below should FAIL, and each fails with a different exception
    attempt("Alice borrows a 4th book", lib.checkout, 1, "444")      # over the limit
    attempt("Bob borrows a book Alice has", lib.checkout, 2, "111")  # already on loan
    attempt("Unknown member", lib.checkout, 99, "444")               # no such member
    attempt("Unknown book", lib.checkout, 2, "000")                  # no such book

    print("\nReturns:")
    attempt("Alice returns 111", lib.return_book, 1, "111")          # works
    attempt("Bob borrows 111", lib.checkout, 2, "111")               # now it's free
    attempt("Bob returns a book he doesn't have", lib.return_book, 2, "222")

    print("\nAvailable now:")
    for book in lib.available_books():           # uses __iter__-style data via the method
        print("  ", book)

    # Validation in __post_init__ stops bad objects from ever existing
    print("\nValidation:")
    for bad in (
        lambda: Book("999", "Future Book", "Nobody", 2999),               # future year
        lambda: EBook("998", "Bad EBook", "Nobody", 2000, file_size_mb=-1),  # negative size
        lambda: Member(3, "  ", "x@example.com"),                         # blank name
    ):
        try:
            bad()
        except ValueError as e:
            print("  ValueError ->", e)

    # frozen=True: trying to change a Book after creation is blocked
    try:
        lib["111"].title = "Changed"      # pyright: ignore[reportAttributeAccessIssue]
    except Exception as e:
        print("  Frozen ->", type(e).__name__)
