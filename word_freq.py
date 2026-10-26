#!/usr/bin/env python3
"""Word-frequency analyzer.

Showcases:
  * generator          -> iter_words() streams words lazily, line by line
  * context manager    -> open_text() opens/closes the file and reports stats
  * decorator          -> @timed measures how long analysis steps take
  * comprehensions     -> list / set / dict comprehensions in the analysis

Usage:
  python word_freq.py path/to/file.txt --top 15 --min-length 3
  python word_freq.py --demo
"""

import argparse
import re
import tempfile
import time
from collections import Counter
from contextlib import contextmanager
from functools import wraps
from pathlib import Path

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at", "for",
    "with", "is", "are", "was", "were", "it", "its", "this", "that", "as", "by",
    "be", "from", "i", "you", "he", "she", "we", "they", "not", "so", "if",
}
WORD_RE = re.compile(r"[a-zA-Z']+")


# ---------- decorator ----------
def timed(func):
    """Print how long the wrapped function took."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[timed] {func.__name__} took {elapsed:.2f} ms")
        return result
    return wrapper


# ---------- context manager ----------
@contextmanager
def open_text(path):
    """Open a text file safely and report basic stats when done."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    f = path.open(encoding="utf-8", errors="replace")
    print(f"[open] {path.name} ({path.stat().st_size} bytes)")
    try:
        yield f
    finally:
        f.close()
        print(f"[close] {path.name} closed")


# ---------- generator ----------
def iter_words(lines, min_length=1):
    """Lazily yield lowercase words from an iterable of lines."""
    for line in lines:
        for match in WORD_RE.finditer(line):
            word = match.group().lower().strip("'")
            if len(word) >= min_length:
                yield word


# ---------- analysis ----------
@timed
def count_words(path, min_length=1, use_stopwords=True):
    with open_text(path) as f:
        words = iter_words(f, min_length)
        if use_stopwords:
            words = (w for w in words if w not in STOPWORDS)
        return Counter(words)


@timed
def summarize(counts, top_n):
    total = sum(counts.values())
    unique = {w for w in counts}                                   # set comprehension
    percentages = {w: round(c / total * 100, 2)                    # dict comprehension
                   for w, c in counts.items()}
    top = counts.most_common(top_n)
    rows = [f"{i:>2}. {w:<15} {c:>5}  {percentages[w]:>5}%"        # list comprehension
            for i, (w, c) in enumerate(top, start=1)]
    return total, len(unique), rows


def run_demo():
    sample = (
        "The quick brown fox jumps over the lazy dog.\n"
        "The dog was not amused; the fox was quick, and the fox was clever.\n"
        "A lazy dog is a happy dog, but a quick fox is a busy fox!\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
        tmp.write(sample)
    return tmp.name


def main():
    parser = argparse.ArgumentParser(description="Word-frequency analyzer")
    parser.add_argument("path", nargs="?", help="text file to analyze")
    parser.add_argument("--top", type=int, default=10, help="how many words to show")
    parser.add_argument("--min-length", type=int, default=1, help="ignore shorter words")
    parser.add_argument("--keep-stopwords", action="store_true", help="don't filter common words")
    parser.add_argument("--demo", action="store_true", help="analyze a built-in sample")
    args = parser.parse_args()

    path = run_demo() if args.demo or not args.path else args.path

    try:
        counts = count_words(path, args.min_length, not args.keep_stopwords)
    except FileNotFoundError as e:
        parser.error(str(e))

    if not counts:
        print("No words found.")
        return

    total, unique, rows = summarize(counts, args.top)
    print(f"\nTotal words: {total} | Unique words: {unique}\n")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
