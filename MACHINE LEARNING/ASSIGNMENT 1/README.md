# Assignment 1 — Perceptron Learning Algorithm and Fisher's Linear Discriminant

Implementation of the Perceptron learning algorithm for binary classification and Fisher's Linear Discriminant (LDA) for dimensionality reduction and visualization.
Part of **BBM409 – Machine Learning**, Hacettepe University.

## Tech Stack

- Python 3
- NumPy, pandas, matplotlib, seaborn
- scikit-learn (train/test split, metrics)
- ucimlrepo (dataset fetching)
- Jupyter Notebook

## Dataset

**Banknote Authentication** (UCI ML Repository, ID 267): 1,372 samples with 4 wavelet-transform features extracted from banknote images, binary labels (genuine/forged).

## Prerequisites

```bash
pip install numpy pandas matplotlib seaborn scikit-learn ucimlrepo jupyter
```

## How to Run

```bash
jupyter notebook assignment1.ipynb
```

Run cells in order. The notebook fetches the dataset automatically via `ucimlrepo`.

## Key Learnings

- Implemented Perceptron from scratch using NumPy; achieved ~98.5% test accuracy on a linearly separable dataset
- Explored how feature selection (via correlation analysis) affects the decision boundary in 2D
- Implemented Fisher's LDA projection and visualized class separation in 1D; observed that Fisher's projection maximizes inter-class distance while collapsing within-class variance
