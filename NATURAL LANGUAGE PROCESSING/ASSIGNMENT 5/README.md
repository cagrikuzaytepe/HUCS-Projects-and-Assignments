# Assignment 5 — News Classification and Article Enhancement Pipeline

End-to-end NLP pipeline that (1) fine-tunes BERT for 4-class news category classification and (2) uses the Gemini API to rewrite article titles and content into a polished, publication-ready format.
Part of **AIN442 / BBM497 – Natural Language Processing**, Hacettepe University.

## Tech Stack

- Python 3
- Hugging Face `transformers` (BERT fine-tuning, `Trainer` API)
- PyTorch
- `google-generativeai` (Gemini API)
- scikit-learn (metrics)
- pandas, NumPy, matplotlib, seaborn
- Jupyter Notebook (ran on Google Colab with T4 GPU)

## Dataset

**AG News** (30,000 train / 7,600 test subset): news articles categorized into World (0), Sports (1), Business (2), Sci/Tech (3).

## Prerequisites

```bash
pip install transformers[torch] datasets pandas scikit-learn matplotlib seaborn google-generativeai tqdm
```

A Google Gemini API key is required for Part 2 and Part 3.

## How to Run

```bash
jupyter notebook assignment5.ipynb
```

Upload `train.csv` and `test.csv` to your Colab session. Set your Gemini API key in the designated cell before running Part 2.

**Note:** The API key cell in this notebook has been cleared. Do not commit credentials.

## Key Learnings

- Fine-tuned `bert-base-uncased` for 4-class classification; best test F1 (macro) ≈ 0.927 achieved with batch_size=32, max_length=256, 3 epochs, weight_decay=0
- Prompt engineering: explicit output format (`TITLE: ... ARTICLE: ...`) with regex parsing was necessary for reliable structured extraction from Gemini
- Temperature 0.7 + top_p 0.9 provided a good balance between factual accuracy and writing fluency for article rewriting
