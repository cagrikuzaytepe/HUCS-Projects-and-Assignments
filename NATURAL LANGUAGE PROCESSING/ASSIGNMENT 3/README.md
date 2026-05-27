# Assignment 3 — Text Classification: Naive Bayes and Logistic Regression

Implementation of Naive Bayes (`_nb.py`) and Logistic Regression (`_lr.py`) classifiers for binary sentiment classification, trained and evaluated on the IMDB dataset.
Part of **AIN442 / BBM497 – Natural Language Processing**, Hacettepe University.

## Tech Stack

- Python 3
- `datasets` (Hugging Face, for IMDB loading)
- NLTK (stopwords)
- scikit-learn (`accuracy_score`)
- pandas, NumPy

## Dataset

**IMDB Sentiment Dataset** loaded via `datasets.load_dataset("imdb")`: 25,000 train / 25,000 test reviews, binary labels (positive/negative).

## Prerequisites

```bash
pip install datasets nltk scikit-learn pandas numpy
python -m nltk.downloader stopwords
```

## How to Run

```bash
# Naive Bayes classifier
python assignment3_naive_bayes.py

# Logistic Regression classifier
python assignment3_logistic_regression.py
```

Both scripts preprocess the dataset, train the respective classifier, and print accuracy on the test set.

## Key Learnings

- Naive Bayes is fast to train and competitive at text classification despite the naive independence assumption; log-probabilities are used to avoid underflow with long documents
- Logistic Regression with TF-IDF features typically outperforms Naive Bayes on sentiment tasks because it learns feature weights discriminatively rather than generatively
- Text preprocessing (lowercasing, punctuation removal, stopword filtering) significantly impacts both models, with stopword removal being particularly important for Naive Bayes
