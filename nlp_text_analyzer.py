"""
NLP Text Analyzer
-----------------
Extracts linguistic information from text using spaCy:
sentences, tokens, POS tags, lemmas, dependencies, named entities,
noun chunks, keywords, word frequency and basic statistics.

Setup:
    pip install spacy
    python -m spacy download en_core_web_sm

Usage:
    python nlp_text_analyzer.py                 # analyzes the built-in sample
    python nlp_text_analyzer.py -f myfile.txt   # analyzes a text file
    python nlp_text_analyzer.py -t "Some text"  # analyzes inline text
"""
import argparse
from collections import Counter

import spacy

SAMPLE_TEXT = (
    "Google announced a new Generative AI research center in Bengaluru on Monday. "
    "The company said that the new center will focus on developing large language "
    "models and AI-powered applications. Several engineers and researchers will "
    "work on the project."
)


class TextAnalyzer:
    def __init__(self, text, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            raise SystemExit(
                f"spaCy model '{model}' not found. Run:\n"
                f"    python -m spacy download {model}"
            )
        self.text = " ".join(text.split())  # normalise whitespace
        self.doc = self.nlp(self.text)

    # ---- individual analyses -------------------------------------------
    def sentences(self):
        return [s.text.strip() for s in self.doc.sents]

    def tokens(self):
        """Per-token linguistic features."""
        return [
            {
                "text": t.text,
                "lemma": t.lemma_,
                "pos": t.pos_,
                "tag": t.tag_,
                "dep": t.dep_,
                "head": t.head.text,
                "is_stop": t.is_stop,
            }
            for t in self.doc
            if not t.is_space
        ]

    def entities(self):
        return [(e.text, e.label_, spacy.explain(e.label_)) for e in self.doc.ents]

    def noun_chunks(self):
        return [c.text for c in self.doc.noun_chunks]

    def pos_distribution(self):
        return Counter(t.pos_ for t in self.doc if not t.is_space)

    def content_words(self):
        """Lemmatised words that are not stop words or punctuation."""
        return [
            t.lemma_.lower()
            for t in self.doc
            if not (t.is_stop or t.is_punct or t.is_space)
        ]

    def word_frequency(self, n=10):
        return Counter(self.content_words()).most_common(n)

    def keywords(self, n=8):
        """Simple keyword extraction: frequent nouns/proper nouns/adjectives."""
        words = [
            t.lemma_.lower()
            for t in self.doc
            if t.pos_ in {"NOUN", "PROPN", "ADJ"} and not t.is_stop
        ]
        return Counter(words).most_common(n)

    def verbs(self):
        return sorted({t.lemma_.lower() for t in self.doc if t.pos_ == "VERB"})

    def statistics(self):
        words = [t for t in self.doc if t.is_alpha]
        sents = list(self.doc.sents)
        uniq = {t.lower_ for t in words}
        return {
            "characters": len(self.text),
            "sentences": len(sents),
            "words": len(words),
            "unique words": len(uniq),
            "avg words/sentence": round(len(words) / max(len(sents), 1), 2),
            "avg word length": round(sum(len(t) for t in words) / max(len(words), 1), 2),
            "lexical diversity": round(len(uniq) / max(len(words), 1), 3),
        }

    # ---- report ----------------------------------------------------------
    def report(self):
        line = "=" * 64

        def head(title):
            print(f"\n{line}\n{title}\n{line}")

        head("TEXT")
        print(self.text)

        head("STATISTICS")
        for k, v in self.statistics().items():
            print(f"{k:<22}{v}")

        head("SENTENCES")
        for i, s in enumerate(self.sentences(), 1):
            print(f"{i}. {s}")

        head("TOKENS  (text | lemma | POS | dependency -> head)")
        for t in self.tokens():
            print(f"{t['text']:<14}{t['lemma']:<14}{t['pos']:<7}{t['dep']:<10}-> {t['head']}")

        head("NAMED ENTITIES")
        for text, label, desc in self.entities() or [("(none)", "", "")]:
            print(f"{text:<28}{label:<10}{desc}")

        head("NOUN CHUNKS")
        print(", ".join(self.noun_chunks()))

        head("PART-OF-SPEECH DISTRIBUTION")
        for pos, c in self.pos_distribution().most_common():
            print(f"{pos:<8}{c:>3}  {'#' * c}")

        head("VERBS (lemmas)")
        print(", ".join(self.verbs()))

        head("KEYWORDS")
        for w, c in self.keywords():
            print(f"{w:<16}{c}")

        head("TOP CONTENT WORDS")
        for w, c in self.word_frequency():
            print(f"{w:<16}{c}")


def main():
    p = argparse.ArgumentParser(description="NLP Text Analyzer")
    p.add_argument("-f", "--file", help="path to a text file")
    p.add_argument("-t", "--text", help="text to analyze")
    args = p.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = args.text or SAMPLE_TEXT

    TextAnalyzer(text).report()


if __name__ == "__main__":
    main()