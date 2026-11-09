# AI Engineer Journey

A 26-week plan to become an Applied AI Engineer.

## Goals
- Build and ship LLM-powered apps (RAG, agents)
- Complete a production-style agent project in coming weeks.
- Commit and document progress weekly

## Progress

### Week 1: Setup and Python Refresh
- [x] Mon: Environment setup
- [x] Tue: Kaggle Python, part 1
- [x] Wed: Kaggle Python, part 2
- [x] Thu: Generators and decorators
- [x] Fri: Context managers and Git
- [x] Sat: Community and mini-project

### Week 2: Professional Python
- [x] Mon: Classes, dataclasses, inheritance vs composition, dunder methods, library system practice
- [x] Tue: Type hints and mypy basics, Exceptions, custom exception classes, the logging module. Type hints to Monday's code and run mypy
- [x] Wed: venv, pip, requirements.txt, pyproject.toml, src layout, __init__.py, pytest, argparse, Typer, Basic CLI applications.
- [x] Thursday: pytest, fixtures, parametrization, 94% coverage.


## Mini-project: Word-Frequency Analyzer

A command-line tool that reads a text file and prints its most common words.
Built to practice four core Python concepts:

| Concept | Where it's used |
|---|---|
| Generator | `iter_words()` streams words one at a time |
| Context manager | `open_text()` opens a file and always closes it |
| Decorator | `@timed` measures how long a function takes |
| Comprehensions | list, set and dict comprehensions in `summarize()` |

### Files
- `word_freq.py`: the compact version
- `word_freq_commented.py`: the same program with beginner-friendly comments
- `word_freq_json.py`: same program plus a `--json` flag
- `test_word_freq.py`, `test_word_freq_json.py`: pytest tests (run with `python -m pytest -v`)

Quick start: `python word_freq.py --demo`

### Usage
```bash
python word_freq.py --demo
python word_freq.py README.md --top 15 --min-length 3
python word_freq.py myfile.txt --keep-stopwords
```

### Options
| Option | Description |
|---|---|
| `--top N` | How many words to show (default 10) |
| `--min-length N` | Ignore words shorter than N letters |
| `--keep-stopwords` | Don't filter common words like "the" |
| `--demo` | Analyze a built-in sample text |

### Known limitations
- Digits are ignored, so `week1` is counted as `week`
- URLs get split into separate words
- Only plain English letters are recognized (no accents)


## Mini-project: Library System

A small library model built with Python dataclasses. It tracks books and members, and enforces borrowing rules.
Built to practice five core object-oriented concepts:

| Concept | Where it's used |
|---|---|
| Dataclasses | `Book`, `EBook` and `Member` hold data; `frozen=True`, `field(default_factory=...)`, `field(repr=False)` and `ClassVar` are all used |
| Validation | `__post_init__` rejects bad data (future year, empty name, negative file size) |
| Inheritance (is-a) | `EBook(Book)` adds `file_size_mb` and reuses the parent's validation via `super()` |
| Composition (has-a) | `Library` owns its books, members and loans |
| Dunder methods | `Library` supports `len()`, `for ... in`, `in` and `library["isbn"]` |

### Files
- `objectOrientedPython/library_system.py`: the full program, with comments explaining the logic

Quick start: `python objectOrientedPython/library_system.py`

### Rules enforced
- A book can't be checked out twice
- A member can borrow at most 3 books
- Unknown members, unknown books and duplicate records are rejected

Each rule raises its own exception (`BookUnavailableError`, `BorrowLimitError`, `BookNotFoundError`, `MemberNotFoundError`, `DuplicateError`), all inheriting from `LibraryError`.

### Usage
```bash
python objectOrientedPython/library_system.py
```

Running the file prints a demo: stocking the shelves, searching, checkouts, every error case, and validation checks.

### Known limitations
- Data lives in memory only, so it resets every run
- No due dates or late fees
- Search is a simple case-insensitive keyword match on title and author


## Testing

Tests live in `tests/` and use [pytest](https://docs.pytest.org/) with `pytest-cov`.

```bash
pip install pytest pytest-cov
python -m pytest                      # run all tests
python -m pytest -v                   # verbose: one line per test
python -m pytest -k "borrow_limit"    # run tests matching a name
python -m pytest --cov=library_system --cov=word_freq --cov=word_freq_json --cov-report=term-missing
```

| Test file | Covers |
|---|---|
| `tests/test_library.py` | Library system: checkout/return rules, custom exceptions, dunder methods, dataclass validation |
| `tests/test_word_freq.py` | Word-frequency tool: generator, context manager, decorator, counting |
| `tests/test_word_freq_json.py` | `--json` edition: JSON output, stdout vs stderr, CLI behaviour |
| `tests/test_word_freq_files.py` | `count_words` on real temp files, parametrized options |

**Result:** 52 tests passing, 94% total coverage (library_system 100%).
The coverage floor is set to 80% in `pyproject.toml`.

### What I learned
- **Fixtures** build reusable test objects (`conftest.py` shares them across files)
- **`parametrize`** runs one test body against many inputs
- **`pytest.raises`** checks that the right error is raised
- **`tmp_path`, `monkeypatch`, `capsys`** for files, fake command lines and captured output
- Coverage shows which lines ran, not whether the assertions are good