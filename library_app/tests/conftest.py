import pytest

from library_app.library import Library
from library_app.models import Book, EBook, Member


@pytest.fixture
def lib():
    library = Library("Test Library")
    library.add_book(Book("111", "The Hobbit", "J.R.R. Tolkien", 1937))
    library.add_book(Book("222", "Matilda", "Roald Dahl", 1988))
    library.add_book(Book("333", "The BFG", "Roald Dahl", 1982))
    library.add_book(EBook("444", "Dune", "Frank Herbert", 1965, 2.4))
    library.register_member(Member(1, "Alice", "alice@example.com"))
    library.register_member(Member(2, "Bob", "bob@example.com"))
    return library
