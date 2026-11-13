# Library App

A small command-line library manager. Books, eBooks and members are stored in a
JSON file, and the library rules (one copy per loan, 3 books per member) are
enforced on every command.

![tests](https://github.com/<your-username>/<your-repo>/actions/workflows/tests.yml/badge.svg)

## Install

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (macOS/Linux: source .venv/bin/activate)
pip install -e ".[dev]"
```

## Usage

```bash
library --help
library add-book 111 "The Hobbit" "J.R.R. Tolkien" 1937
library register 1 Alice alice@example.com
library checkout 1 111
```

Every command accepts `--db PATH` (default `library.json` in the current folder).

| Command | Arguments | What it does |
|---|---|---|
| `add-book` | `ISBN TITLE AUTHOR YEAR` | Add a book |
| `add-ebook` | `ISBN TITLE AUTHOR YEAR SIZE_MB` | Add an eBook |
| `register` | `MEMBER_ID NAME EMAIL` | Register a member |
| `checkout` | `MEMBER_ID ISBN` | Lend a book to a member |
| `return` | `MEMBER_ID ISBN` | Return a book |
| `search` | `KEYWORD` | Search titles and authors |
| `available` | | List books not on loan |

## Example

```text
$ library add-book 111 "The Hobbit" "J.R.R. Tolkien" 1937
Added 'The Hobbit' by J.R.R. Tolkien (1937)
$ library register 1 Alice alice@example.com
Registered Alice (id 1)
$ library checkout 1 111
Checked out 'The Hobbit' by J.R.R. Tolkien (1937)
$ library checkout 1 111
Error: 'The Hobbit' by J.R.R. Tolkien (1937) is already checked out
```

Failed commands print `Error: ...` to stderr and exit with code 1.

## Design

- `models.py`: `Book`, `EBook` (inherits `Book`), `Member` dataclasses with validation.
- `library.py`: `Library` (composition) and the custom exceptions.
- `storage.py`: JSON save/load. Books carry a `type` field; members store only the
  ISBNs they hold, and loans are rebuilt on load through `checkout`, so there is one
  source of truth.
- `cli.py`: Typer commands: load, act, save, turn `LibraryError` into a clean message.

## Tests

```bash
pytest --cov=library_app
```

## Known limitations

- `Member.borrowed` is a public list, so outside code can bypass the loan rules.
- No due dates, fines or loan history.
- The whole file is loaded and saved on every command; fine for small data, not for large.
- No locking: two commands running at the same moment can overwrite each other.
- Emails are stored in plain text and not validated; `Book` doesn't validate the author.
- ISBNs are treated as opaque strings (no checksum validation).
