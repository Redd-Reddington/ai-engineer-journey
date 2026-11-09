"""
conftest.py: shared fixtures.

Pytest loads this file automatically before running any test, and every test
file in this folder can use the fixtures defined here. You never import them.
"""

import pytest
from library_system import Library, Book, Member


# @pytest.fixture turns this function into a fixture: a recipe for building
# something a test needs. A test asks for it by putting the function's NAME
# in its parameters, e.g. def test_x(library): ...
# Pytest then calls this function and passes in whatever it returns.
@pytest.fixture
def library():
    lib = Library("Test Library")                    # Library requires a name
    # Four books with known ISBNs, so tests can refer to "111", "222", etc.
    lib.add_book(Book("111", "Dune", "Herbert", 1965))
    lib.add_book(Book("222", "Emma", "Austen", 1815))
    lib.add_book(Book("333", "Matilda", "Dahl", 1988))
    lib.add_book(Book("444", "The Hobbit", "Tolkien", 1937))
    return lib
    # Each test gets a BRAND NEW library, so one test borrowing a book
    # can never affect another test. This is called test isolation.


# A fixture can use another fixture: asking for "library" here makes pytest
# build it first and pass it in. The test and this fixture then share the
# SAME library object, which is why the member is registered into it.
@pytest.fixture
def member(library):
    m = Member(1, "Ama", "ama@example.com")          # Member requires an email
    library.register_member(m)                       # so checkout(1, ...) works
    return m