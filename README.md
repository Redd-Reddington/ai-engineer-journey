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