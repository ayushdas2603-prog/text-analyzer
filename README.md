# text-analyzer

A lightweight Python command-line tool that analyzes text and reports word, sentence and paragraph counts, top words, lexical diversity, reading time and a readability score.

No external dependencies. Just the Python standard library.

## Features

- Character counts (with and without spaces)
- Word, unique word, sentence, paragraph and line counts
- Average word length and average sentence length
- Lexical diversity (unique words / total words)
- Top N most frequent words (common stop words are skipped)
- Longest words
- Estimated reading time
- Flesch Reading Ease score with a plain-English label
- Plain text report or JSON output

## Requirements

- Python 3.7 or newer

## Installation

```bash
git clone https://github.com/<your-username>/text-analyzer.git
cd text-analyzer
```

## Usage

Analyze a file:

```bash
python text_analyzer.py myfile.txt
```

Analyze a string directly:

```bash
python text_analyzer.py -t "Paste some text here. It works on short snippets too."
```

Read from standard input:

```bash
cat myfile.txt | python text_analyzer.py
```

Or run it with no arguments, paste your text, and press `Ctrl+D` (`Ctrl+Z` then `Enter` on Windows).

### Options

| Option | Description |
| --- | --- |
| `file` | Path to a text file to analyze |
| `-t`, `--text` | Analyze the given text instead of a file |
| `--top N` | Number of top words to show (default: 10) |
| `--json` | Output results as JSON |

## Example output

```
============================================
  TEXT ANALYSIS REPORT
============================================
characters (with spaces)       123
characters (no spaces)         98
words                          24
unique words                   20
sentences                      2
paragraphs                     1
lines                          1
avg word length                4.08
avg sentence length (words)    12.0
lexical diversity              0.833
reading time (min)             0.12
flesch reading ease            72.4
readability                    Fairly easy
longest words                  ...
```

## Use as a module

```python
from text_analyzer import TextAnalyzer

analyzer = TextAnalyzer("Hello world. This is a test.")
print(analyzer.word_count())
print(analyzer.top_words(5))
print(analyzer.summary())
```

## How readability is scored

The tool uses the Flesch Reading Ease formula. Higher scores mean easier text:

| Score | Meaning |
| --- | --- |
| 90+ | Very easy |
| 80-89 | Easy |
| 70-79 | Fairly easy |
| 60-69 | Plain English |
| 50-59 | Fairly difficult |
| 30-49 | Difficult |
| Below 30 | Very difficult |

Syllable counting is heuristic, so scores are approximate.

## Ideas for future work

- Sentiment analysis
- Bigram and trigram frequency
- Custom stop word lists
- Support for other languages
- A simple GUI

## Contributing

Issues and pull requests are welcome.

## License

MIT. Add a `LICENSE` file to your repo to make this official.
