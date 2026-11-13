"""The Library class and its custom exceptions."""

from typing import Iterator

from library_app.models import Book, Member


class LibraryError(Exception):
    """Base class for all library errors."""


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


class Library:
    """A Library HAS books, members and loans (composition)."""

    def __init__(self, name: str):
        self.name = name
        self._books: dict[str, Book] = {}
        self._members: dict[int, Member] = {}
        self._loans: dict[str, int] = {}  # isbn -> member_id

    # ----- managing records -----

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise DuplicateError(f"Book {book.isbn} already exists")
        self._books[book.isbn] = book

    def register_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise DuplicateError(f"Member {member.member_id} already exists")
        self._members[member.member_id] = member

    def _get_member(self, member_id: int) -> Member:
        try:
            return self._members[member_id]
        except KeyError:
            raise MemberNotFoundError(f"No member with id {member_id}") from None

    # ----- core actions -----

    def checkout(self, member_id: int, isbn: str) -> Book:
        member = self._get_member(member_id)
        if isbn not in self._books:
            raise BookNotFoundError(f"No book with ISBN {isbn}")
        if isbn in self._loans:
            raise BookUnavailableError(f"{self._books[isbn]} is already checked out")
        if not member.can_borrow:
            raise BorrowLimitError(
                f"{member.name} already has {Member.MAX_LOANS} books"
            )
        book = self._books[isbn]
        self._loans[isbn] = member_id
        member.borrowed.append(book)
        return book

    def return_book(self, member_id: int, isbn: str) -> Book:
        member = self._get_member(member_id)
        if self._loans.get(isbn) != member_id:
            raise BookUnavailableError(f"{member.name} does not have book {isbn}")
        book = self._books[isbn]
        member.borrowed.remove(book)
        del self._loans[isbn]
        return book

    # ----- queries -----

    def search(self, keyword: str) -> list[Book]:
        keyword = keyword.lower()
        return [
            b for b in self._books.values()
            if keyword in b.title.lower() or keyword in b.author.lower()
        ]

    def available_books(self) -> list[Book]:
        return [b for isbn, b in self._books.items() if isbn not in self._loans]

    def members(self) -> list[Member]:
        """Public read access so storage doesn't touch _members."""
        return list(self._members.values())

    # ----- dunder methods -----

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books.values())

    def __contains__(self, item) -> bool:
        isbn = item.isbn if isinstance(item, Book) else item
        return isbn in self._books

    def __getitem__(self, isbn: str) -> Book:
        try:
            return self._books[isbn]
        except KeyError:
            raise KeyError(f"No book with ISBN {isbn}") from None

    def __str__(self) -> str:
        return (
            f"{self.name}: {len(self._books)} books, "
            f"{len(self._members)} members, {len(self._loans)} on loan"
        )
