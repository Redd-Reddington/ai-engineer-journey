"""Save and load a Library as JSON.

Books are stored with a "type" field so load() knows which class to rebuild.
Members store only the ISBNs they hold; loans are rebuilt on load by calling
Library.checkout, so there is a single source of truth.
"""

import json
from datetime import date
from pathlib import Path

from library_app.library import Library
from library_app.models import Book, EBook, Member

DEFAULT_NAME = "City Library"


def save(lib: Library, path: Path) -> None:
    data = {
        "name": lib.name,
        "books": [_book_to_dict(b) for b in lib],
        "members": [
            {
                "member_id": m.member_id,
                "name": m.name,
                "email": m.email,
                "joined": m.joined.isoformat(),
                "borrowed": [b.isbn for b in m.borrowed],
            }
            for m in lib.members()
        ],
    }
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)  # write-then-rename so a crash can't leave a half-written file


def load(path: Path) -> Library:
    path = Path(path)
    if not path.exists():
        return Library(DEFAULT_NAME)

    data = json.loads(path.read_text(encoding="utf-8"))
    lib = Library(data["name"])
    for b in data["books"]:
        lib.add_book(_book_from_dict(b))
    for m in data["members"]:
        lib.register_member(
            Member(
                member_id=m["member_id"],
                name=m["name"],
                email=m["email"],
                joined=date.fromisoformat(m["joined"]),
            )
        )
        for isbn in m["borrowed"]:
            lib.checkout(m["member_id"], isbn)
    return lib


def _book_to_dict(book: Book) -> dict:
    d = {
        "type": "ebook" if isinstance(book, EBook) else "book",
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "year": book.year,
    }
    if isinstance(book, EBook):
        d["file_size_mb"] = book.file_size_mb
    return d


def _book_from_dict(d: dict) -> Book:
    if d["type"] == "ebook":
        return EBook(d["isbn"], d["title"], d["author"], d["year"], d["file_size_mb"])
    return Book(d["isbn"], d["title"], d["author"], d["year"])
