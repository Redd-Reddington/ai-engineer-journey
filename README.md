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
- [x] Thu: pytest, fixtures, parametrization, 94% coverage.
- [x] Fri: NumPy arrays, indexing, broadcasting, vectorization, and timing loops against vectorized code
- [x] Sat: Finish the mini-project. Library System turned into a tested CLI tool (`library_app`) with JSON persistence, a README and a GitHub Actions workflow, 20 NumPy exercises, weekly review.


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
- Data lives in memory only, so it resets every run (fixed in the CLI version below)
- No due dates or late fees
- Search is a simple case-insensitive keyword match on title and author


## Mini-project: Library App (CLI)

The Library System turned into an installable command-line tool with JSON persistence and a test suite. It lives in its own folder, `library_app/`, with its own `pyproject.toml`, README and tests.
Built to practice packaging, persistence, CLI design and testing:

| Concept | Where it's used |
|---|---|
| Package structure | `models.py`, `library.py`, `storage.py`, `cli.py` split by responsibility |
| Persistence | `save` / `load` write the library to JSON; books carry a `"type"` field so eBooks reload as `EBook` |
| Single source of truth | Members store only borrowed ISBNs; loans are rebuilt on load through `Library.checkout` |
| CLI | Typer commands that load, act, save, and turn `LibraryError` into a clean `Error: ...` message with exit code 1 |
| Testing | pytest fixtures, `parametrize`, `tmp_path` and Typer's `CliRunner` |
| CI | GitHub Actions workflow runs the tests on every push |

### Files
- `library_app/library_app/`: the package (`models.py`, `library.py`, `storage.py`, `cli.py`)
- `library_app/tests/`: `conftest.py`, `test_library.py`, `test_storage.py`, `test_cli.py`
- `library_app/pyproject.toml`: dependencies, `library` entry point, pytest config
- `.github/workflows/tests.yml`: CI workflow (runs from the `library_app` folder)

Quick start:
```bash
cd library_app
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
library --help
```

### Commands
| Command | Arguments | What it does |
|---|---|---|
| `add-book` | `ISBN TITLE AUTHOR YEAR` | Add a book |
| `add-ebook` | `ISBN TITLE AUTHOR YEAR SIZE_MB` | Add an eBook |
| `register` | `MEMBER_ID NAME EMAIL` | Register a member |
| `checkout` | `MEMBER_ID ISBN` | Lend a book to a member |
| `return` | `MEMBER_ID ISBN` | Return a book |
| `search` | `KEYWORD` | Search titles and authors |
| `available` | | List books not on loan |

Every command accepts `--db PATH` (default `library.json` in the current folder).

### What I learned
- A CLI runs once per command, so state has to be saved to disk or it is forgotten
- Storing one source of truth (ISBNs on members) and rebuilding the rest avoids two structures drifting apart
- Click treats `-1` as an option flag, so the test for a bad file size uses `0` instead
- `pip install -e .` from the repo root fails when the root has several top-level folders; install from inside the project folder
- GitHub only reads workflows from the repo root's `.github/`, so a subfolder project needs `working-directory`

### Known limitations
- `Member.borrowed` is a public list, so outside code can bypass the loan rules
- No due dates, fines or loan history
- The whole file is loaded and saved on every command
- No file locking, so two commands at the same moment can overwrite each other
- Emails are stored in plain text and not validated; `Book` doesn't validate the author
- ISBNs are treated as opaque strings (no checksum validation)


## Mini-project: NumPy Practice

Practice scripts for NumPy fundamentals, plus a benchmark showing why vectorized code is faster.
Built to practice four core NumPy concepts:

| Concept | Where it's used |
|---|---|
| Arrays and shapes | 1D and 3D arrays, `.ndim`, `.shape` |
| Indexing and slicing | `array[start:end:step]` on rows and columns, negative indexes, reversing |
| Broadcasting | `(1, 4) + (4, 1)` expands to a full grid; dimensions must match or be 1 |
| Vectorization | `np.vectorize` compared with native array operations |

### Files
- `NumPy/numpy_practise.py`: notes and examples, with each topic in a commented-out block
- `NumPy/vectorized_operations.py`: benchmark of loop vs `np.vectorize` vs native NumPy

Quick start: `python NumPy/vectorized_operations.py`

### Benchmark results
1,000,000 random floats, computing `x ** 2` (one run, results vary by machine):

| Method | Time |
|---|---|
| Python loop | 0.1140s |
| `np.vectorize` | 0.1961s |
| Native NumPy (`x ** 2`) | 0.0023s (~49x faster than the loop) |

### What I learned
- `np.vectorize` is a convenience wrapper, not real vectorization. It still calls the Python function once per element, so it was slower than the plain loop.
- Native array operations run in compiled C over contiguous typed memory.
- Use `np.vectorize` only when the logic can't be written with array operations or `np.where`.

### Known limitations
- Timings come from a single run, so they vary between runs
- Only one array size (1,000,000) is benchmarked


## Testing

Tests use [pytest](https://docs.pytest.org/) with `pytest-cov`. The root `tests/` folder covers the earlier mini-projects; `library_app/tests/` covers the CLI tool.

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

### Library App tests
Run from inside `library_app/`:

```bash
python -m pytest --cov=library_app
```

| Test file | Covers |
|---|---|
| `library_app/tests/test_library.py` | Model validation, duplicates, checkout/return rules, failed checkout changing nothing, search, dunder methods |
| `library_app/tests/test_storage.py` | JSON round trip (EBook type, loans, join date), missing file, saved format |
| `library_app/tests/test_cli.py` | Every command via `CliRunner`: exit codes, messages, state persisting between runs |

**Result:** 36 tests passing, 99% total coverage (library, models and storage 100%, cli 96%).

### What I learned
- **Fixtures** build reusable test objects (`conftest.py` shares them across files)
- **`parametrize`** runs one test body against many inputs
- **`pytest.raises`** checks that the right error is raised
- **`tmp_path`, `monkeypatch`, `capsys`** for files, fake command lines and captured output
- **`CliRunner`** invokes a Typer app in-process and returns the exit code and output
- Coverage shows which lines ran, not whether the assertions are good
