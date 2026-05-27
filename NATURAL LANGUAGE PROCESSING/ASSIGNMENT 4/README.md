# Assignment 4 — Word2Vec: Semantic Similarity and Sentence Retrieval

Three utilities built on top of Google News Word2Vec (300-D) embeddings: lexical substitution with semantically similar words, sentence vectorization, and cosine-similarity-based sentence retrieval.
Part of **AIN442 / BBM497 – Natural Language Processing**, Hacettepe University.

## Tech Stack

- Python 3
- gensim >= 4.3 (`word2vec-google-news-300`, ~1.5 GB download)
- NumPy

## Functions

| Function | Description |
|----------|-------------|
| `replace_with_similar(sentence, indices)` | Replaces words at given indices with a semantically similar word sampled from top-5 neighbors |
| `sentence_vector(sentence)` | Computes a sentence vector as the mean of its word vectors |
| `most_similar_sentences(file_path, query)` | Ranks sentences in a file by cosine similarity to a query sentence |

## Prerequisites

```bash
pip install "numpy>=1.25" "gensim>=4.3"
```

The Word2Vec model is downloaded automatically by gensim on first run.

## How to Run

```bash
python assignment4.py
# or open the notebook
jupyter notebook assignment4.ipynb
```

Output is written to `output.txt`. Provide a `sentences.txt` file with one sentence per line for the retrieval task.

## Key Learnings

- Mean-of-word-vectors is a simple but effective sentence representation; it loses word order but captures the topical content of the sentence
- Deterministic word replacement (seeded RNG based on token hash) ensures reproducible outputs without manual seed tracking
- Out-of-vocabulary words (not in the Google News model) are represented as zero vectors, which can skew sentence similarity scores for short sentences with many OOV terms
