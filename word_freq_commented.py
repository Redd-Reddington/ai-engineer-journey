#!/usr/bin/env python3
"""Word-frequency analyzer (beginner-friendly, heavily commented version).

WHAT THIS PROGRAM DOES
    You give it a text file. It reads the file, counts how many times each
    word appears, and prints the most common words.

THE FOUR PYTHON IDEAS IT DEMONSTRATES
    1. Generator        -> iter_words()   hands out words ONE AT A TIME
    2. Context manager  -> open_text()    opens a file and ALWAYS closes it
    3. Decorator        -> @timed         adds a stopwatch to a function
    4. Comprehensions   -> in summarize() one-line ways to build lists/sets/dicts

THE BIG PICTURE (the order things happen in)
    main()
      -> count_words()        (read the file and count)
           -> open_text()     (open the file safely)
           -> iter_words()    (pull out words one by one)
      -> summarize()          (turn counts into percentages and table rows)
      -> print the results
"""

# ----------------------------------------------------------------------------
# IMPORTS: tools that Python already provides. We "import" the ones we need.
# ----------------------------------------------------------------------------
import argparse   # reads options typed in the terminal, like --top 15
import re         # "regular expressions": a mini-language for finding patterns in text
import tempfile   # creates temporary files (used only by the demo)
import time       # lets us measure time (used by the stopwatch decorator)
from collections import Counter     # a dictionary specialised for counting things
from contextlib import contextmanager  # makes it easy to build a context manager
from functools import wraps         # keeps a decorated function's name intact
from pathlib import Path            # a friendly way to work with file paths

# ----------------------------------------------------------------------------
# SETTINGS (constants). Written in CAPITALS by convention: "don't change me".
# ----------------------------------------------------------------------------

# Very common words that tell us little ("the", "and", ...). We skip them.
# This is a *set* (curly braces, no colons). Sets are very fast for the
# question "is this word in the collection?".
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "with", "is", "are", "was", "were", "it", "its", "this", "that", "as", "by",
    "be", "from", "i", "you", "he", "she", "we", "they", "not", "so", "if",
}

# A pattern that describes "what counts as a word":
#   [a-zA-Z']  = any one letter (lower or upper case) or an apostrophe
#   +          = one or more of those in a row
# So "don't" is one word, and "hello," gives "hello" (the comma is ignored).
WORD_RE = re.compile(r"[a-zA-Z']+")


# ============================================================================
# 1) THE DECORATOR  ->  @timed
# ============================================================================
# A decorator is a function that takes ANOTHER function and wraps it with
# extra behaviour. Here the extra behaviour is a stopwatch.
#
# Think of it like putting a function inside a box that says:
#   "start the timer -> run the function -> stop the timer -> print the time".
def timed(func):
    """Print how long the wrapped function took."""

    # @wraps makes the wrapped function keep its real name (e.g. "count_words")
    # instead of being called "wrapper" in our printout.
    @wraps(func)
    def wrapper(*args, **kwargs):
        # *args and **kwargs mean "accept whatever arguments were given and
        # pass them along untouched". This lets @timed work on ANY function.
        start = time.perf_counter()            # note the time before running
        result = func(*args, **kwargs)         # run the real function
        elapsed = (time.perf_counter() - start) * 1000  # seconds -> milliseconds
        print(f"[timed] {func.__name__} took {elapsed:.2f} ms")
        return result                          # hand back the real function's answer

    return wrapper  # the box that replaces the original function


# ============================================================================
# 2) THE CONTEXT MANAGER  ->  open_text()
# ============================================================================
# A context manager is used with the `with` keyword. It guarantees that
# "clean up" code runs when you're finished, even if an error happens.
# Classic example: closing a file so it doesn't stay locked or leak memory.
#
# @contextmanager lets us write one with a simple function that has a `yield`:
#   - code BEFORE yield = setup (runs when the `with` block starts)
#   - the yielded value = what you get after "as" in `with ... as f`
#   - code AFTER yield  = cleanup (runs when the `with` block ends)
@contextmanager
def open_text(path):
    """Open a text file safely and report basic stats when done."""
    path = Path(path)  # turn the text path into a Path object

    # Setup, step 1: stop early with a clear error if the file doesn't exist.
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")

    # Setup, step 2: open the file.
    #   encoding="utf-8"   -> read the file as UTF-8 text (the common standard)
    #   errors="replace"   -> if a weird byte appears, put a ? instead of crashing
    f = path.open(encoding="utf-8", errors="replace")
    print(f"[open] {path.name} ({path.stat().st_size} bytes)")

    try:
        yield f  # <-- the `with` block runs here, using f
    finally:
        # `finally` ALWAYS runs: after success, and also after an error.
        f.close()
        print(f"[close] {path.name} closed")


# ============================================================================
# 3) THE GENERATOR  ->  iter_words()
# ============================================================================
# A generator is a function that uses `yield` instead of `return`.
# Instead of building one giant list of every word, it hands out ONE word,
# pauses, and continues when asked for the next one.
#
# Why that's nice: a 5 GB file would not fit in memory as a list of words,
# but a generator only ever holds one line and one word at a time.
def iter_words(lines, min_length=1):
    """Lazily yield lowercase words from an iterable of lines."""
    # A file object gives us one line at a time when looped over.
    for line in lines:
        # finditer finds every match of our word pattern in this line.
        for match in WORD_RE.finditer(line):
            # match.group() = the matched text, e.g. "Hello"
            # .lower()      = "hello" (so "The" and "the" count as the same word)
            # .strip("'")   = remove apostrophes from the edges ('hi' -> hi)
            word = match.group().lower().strip("'")

            # Only hand out the word if it's long enough.
            if len(word) >= min_length:
                yield word  # hand out one word, then pause here


# ============================================================================
# 4) THE ANALYSIS
# ============================================================================

# The @timed line below means: "wrap count_words in the stopwatch box".
# It's the same as writing:  count_words = timed(count_words)
@timed
def count_words(path, min_length=1, use_stopwords=True):
    """Read the file and return a Counter like {"fox": 5, "dog": 4, ...}."""
    # `with` uses our context manager: the file is opened here and is
    # guaranteed to be closed when the indented block ends.
    with open_text(path) as f:
        # Start the word stream. Nothing is read yet! Generators are lazy.
        words = iter_words(f, min_length)

        if use_stopwords:
            # A *generator expression* (note the round brackets): it filters
            # the stream, keeping only words that are NOT in STOPWORDS.
            # Still lazy: words are checked one at a time.
            words = (w for w in words if w not in STOPWORDS)

        # Counter(...) pulls every word from the stream and counts them.
        # THIS is the moment the file is actually read.
        return Counter(words)


@timed
def summarize(counts, top_n):
    """Turn raw counts into totals and nicely formatted table rows."""
    total = sum(counts.values())  # all words added together, e.g. 21

    # --- SET COMPREHENSION ---------------------------------------------------
    # Curly braces with no colon build a set. A set never holds duplicates.
    # Reads as: "a set of w, for every w in counts".
    # The number of items = how many DIFFERENT words there are.
    unique = {w for w in counts}

    # --- DICT COMPREHENSION --------------------------------------------------
    # Curly braces WITH a colon build a dictionary.
    # Reads as: "word -> percentage, for every word and count in counts".
    # round(..., 2) keeps two decimal places.
    percentages = {w: round(c / total * 100, 2) for w, c in counts.items()}

    # The N most common (word, count) pairs, highest count first.
    top = counts.most_common(top_n)

    # --- LIST COMPREHENSION --------------------------------------------------
    # Square brackets build a list.
    # Reads as: "a formatted line, for every (rank, (word, count)) in top".
    # enumerate(top, start=1) numbers the items starting at 1.
    # Format codes: {i:>2} = right-align in 2 spaces, {w:<15} = left-align in 15,
    #               {c:>5} = right-align in 5, and so on. They make columns line up.
    rows = [
        f"{i:>2}. {w:<15} {c:>5}  {percentages[w]:>5}%"
        for i, (w, c) in enumerate(top, start=1)
    ]

    return total, len(unique), rows


# ============================================================================
# DEMO + MAIN PROGRAM
# ============================================================================
def run_demo():
    """Create a small temporary text file so you can try the program."""
    sample = (
        "The quick brown fox jumps over the lazy dog.\n"
        "The dog was not amused; the fox was quick, and the fox was clever.\n"
        "A lazy dog is a happy dog, but a quick fox is a busy fox!\n"
    )
    # delete=False keeps the file on disk after we close it, so we can read it.
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(sample)
    return tmp.name  # the path of the temporary file


def main():
    """Read the terminal options, run the analysis, print the results."""
    # --- 1. Describe the options the program accepts --------------------------
    parser = argparse.ArgumentParser(description="Word-frequency analyzer")
    # nargs="?" means the file path is optional.
    parser.add_argument("path", nargs="?", help="text file to analyze")
    parser.add_argument("--top", type=int, default=10, help="how many words to show")
    parser.add_argument("--min-length", type=int, default=1, help="ignore shorter words")
    # action="store_true": the option is False unless you type it.
    parser.add_argument("--keep-stopwords", action="store_true",
                        help="don't filter common words")
    parser.add_argument("--demo", action="store_true", help="analyze a built-in sample")
    args = parser.parse_args()  # read what the user actually typed

    # --- 2. Decide which file to analyze --------------------------------------
    # Use the demo file if --demo was typed OR no path was given.
    path = run_demo() if args.demo or not args.path else args.path

    # --- 3. Count the words ---------------------------------------------------
    try:
        counts = count_words(path, args.min_length, not args.keep_stopwords)
    except FileNotFoundError as e:
        # Show a clean error message instead of a scary traceback.
        parser.error(str(e))

    # An empty Counter is "falsy", so this catches files with no words.
    if not counts:
        print("No words found.")
        return

    # --- 4. Summarize and print -----------------------------------------------
    total, unique, rows = summarize(counts, args.top)
    print(f"\nTotal words: {total} | Unique words: {unique}\n")
    print("\n".join(rows))  # join the list of rows into one text, one per line


# This line means: "only run main() when this file is run directly",
# not when another file imports it. It's standard in Python scripts.
if __name__ == "__main__":
    main()
