"""Typer CLI. Every command: load -> act -> save, with clean error messages."""

from pathlib import Path

import typer

from library_app.library import LibraryError
from library_app.models import Book, EBook, Member
from library_app.storage import load, save

app = typer.Typer(help="Small library manager backed by a JSON file.")

DbOption = typer.Option(Path("library.json"), "--db", help="Path to the JSON data file.")


def _fail(message: str) -> None:
    typer.echo(f"Error: {message}", err=True)
    raise typer.Exit(code=1)


@app.command("add-book")
def add_book(isbn: str, title: str, author: str, year: int, db: Path = DbOption):
    """Add a book to the library."""
    lib = load(db)
    try:
        lib.add_book(Book(isbn, title, author, year))
    except (LibraryError, ValueError) as e:
        _fail(str(e))
    save(lib, db)
    typer.echo(f"Added {lib[isbn]}")


@app.command("add-ebook")
def add_ebook(
    isbn: str, title: str, author: str, year: int, size_mb: float, db: Path = DbOption
):
    """Add an eBook to the library."""
    lib = load(db)
    try:
        lib.add_book(EBook(isbn, title, author, year, size_mb))
    except (LibraryError, ValueError) as e:
        _fail(str(e))
    save(lib, db)
    typer.echo(f"Added {lib[isbn]}")


@app.command()
def register(member_id: int, name: str, email: str, db: Path = DbOption):
    """Register a new member."""
    lib = load(db)
    try:
        lib.register_member(Member(member_id, name, email))
    except (LibraryError, ValueError) as e:
        _fail(str(e))
    save(lib, db)
    typer.echo(f"Registered {name} (id {member_id})")


@app.command()
def checkout(member_id: int, isbn: str, db: Path = DbOption):
    """Check a book out to a member."""
    lib = load(db)
    try:
        book = lib.checkout(member_id, isbn)
    except LibraryError as e:
        _fail(str(e))
    save(lib, db)
    typer.echo(f"Checked out {book}")


@app.command("return")
def return_book(member_id: int, isbn: str, db: Path = DbOption):
    """Return a book."""
    lib = load(db)
    try:
        book = lib.return_book(member_id, isbn)
    except LibraryError as e:
        _fail(str(e))
    save(lib, db)
    typer.echo(f"Returned {book}")


@app.command()
def search(keyword: str, db: Path = DbOption):
    """Search titles and authors (case-insensitive)."""
    results = load(db).search(keyword)
    if not results:
        typer.echo("No matches.")
        return
    for book in results:
        typer.echo(f"{book.isbn}: {book}")


@app.command()
def available(db: Path = DbOption):
    """List books that are not on loan."""
    books = load(db).available_books()
    if not books:
        typer.echo("No books available.")
        return
    for book in books:
        typer.echo(f"{book.isbn}: {book}")


if __name__ == "__main__":
    app()
