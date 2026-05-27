# Assignment 1 — Byte Pair Encoding (BPE) Tokenization

Implementation of the BPE tokenization algorithm from scratch, including corpus training, vocabulary construction, and tokenization of new strings.
Part of **AIN442 / BBM497 – Natural Language Processing**, Hacettepe University.

## Tech Stack

- Python 3
- Standard library only (`codecs`, `re`)

## How to Run

```bash
python assignment1.py
```

The script runs BPE on `hw01_tiny.txt` with default and custom merge counts, then writes full output for `hw01_bilgisayar.txt` to `output1.txt` (1000 merges) and `output2.txt` (200 merges).

Provide your own `.txt` corpus files or use the included ones.

## Key Functions

| Function | Description |
|----------|-------------|
| `bpeCorpus(corpus, maxMergeCount)` | Trains BPE on a string corpus, returns merges, vocabulary, and tokenized corpus |
| `bpeFN(fn, maxMergeCount)` | Same as above but reads from a file |
| `bpeTokenize(str, merges)` | Tokenizes a new string using a pre-trained merge list |
| `bpeFNToFile(infn, maxMergeCount, outfn)` | Convenience wrapper that writes output to a file |

## Key Learnings

- BPE iteratively merges the most frequent adjacent symbol pair; tie-breaking by lexicographic order ensures deterministic output
- The number of merge operations directly controls vocabulary granularity: too few merges leaves most tokens as single characters, too many approaches word-level tokenization
- Turkish text requires Unicode-aware handling (`codecs.open` with UTF-8) due to characters like ç, ğ, ş, ü
