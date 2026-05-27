# Assignment 4 — Sentiment Analysis with LSTM

Custom LSTM implementation for binary sentiment classification on movie reviews, with comparison against PyTorch's built-in LSTM.
Part of **BBM409 – Machine Learning**, Hacettepe University.

## Tech Stack

- Python 3
- PyTorch
- NLTK (tokenization, stopwords, lemmatization)
- TensorFlow/Keras (text preprocessing)
- gensim (FastText word vectors via downloader)
- scikit-learn (metrics)
- Jupyter Notebook (ran on Google Colab with T4 GPU)

## Dataset

**IMDB Movie Reviews** (10,000 subset): balanced 5,000 positive / 5,000 negative reviews. Split 70% train / 15% validation / 15% test.

## Prerequisites

```bash
pip install torch nltk tensorflow gensim scikit-learn pandas numpy matplotlib seaborn jupyter
```

Download NLTK data at runtime:
```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('opinion_lexicon')
```

## How to Run

```bash
jupyter notebook assignment4.ipynb
```

The notebook downloads the FastText model (`fasttext-wiki-news-subwords-300`) automatically via gensim on first run (several GB download). Update `file_path` to point to your IMDB CSV.

## Key Learnings

- Built an LSTM cell from scratch using `nn.Module` gates (forget, input, candidate, output), compared against `nn.LSTM`; the custom cell achieved ~84% test accuracy
- Used FastText pre-trained word vectors as embedding initialization; high OOV rate (~35%) highlighted the effect of domain mismatch between general FastText and movie review vocabulary
- Visualized sentiment-rich word vectors in 2D/3D using PCA to confirm that positive and negative words cluster separately in the embedding space
