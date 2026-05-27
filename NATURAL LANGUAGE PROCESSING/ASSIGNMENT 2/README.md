# Assignment 2 — N-gram Language Model

Implementation of a bigram language model with add-k smoothing and text generation via sampling.
Part of **AIN442 / BBM497 – Natural Language Processing**, Hacettepe University.

## Tech Stack

- Python 3
- Standard library (`re`, `random`, `codecs`)

## How to Run

```bash
python assignment2.py
```

Provide Turkish text corpus files (`.txt`) as input. The script trains a bigram model, computes perplexity on a test set, and generates sample sentences.

## Key Features

- Turkish-aware tokenization with regex patterns supporting Turkish characters and numbers
- Sentence boundary handling with `<s>` and `</s>` padding tokens
- Bigram probability estimation with add-k smoothing for unseen pairs
- Text generation using the `followDict` for sampling next tokens given a context

## Key Learnings

- Bigram models capture short-range dependencies but fail at longer-range grammatical coherence; perplexity drops significantly with more training data
- Add-k smoothing (Laplace) redistributes probability mass to unseen n-grams, preventing zero probability assignments during evaluation
- Turkish morphology creates a large, sparse vocabulary, making smoothing especially important compared to less morphologically rich languages
