# Assignment 2 — Classification with Machine Learning Algorithms

Classification assignment using two datasets: Portuguese Bank Marketing (binary classification) and BMI/Weight categories (6-class classification).
Part of **BBM409 – Machine Learning**, Hacettepe University.

## Tech Stack

- Python 3
- NumPy, pandas, scikit-learn
- Jupyter Notebook

## Datasets

- `portuguese_bank_marketing_numeric_random_subsampled.csv` — predicting whether a client subscribed to a term deposit
- `weights_bmi_6classes.csv` — classifying individuals into 6 BMI weight categories

## Prerequisites

```bash
pip install numpy pandas scikit-learn jupyter
```

## How to Run

The source code is in the submission archive (`2210356036.zip`). Extract it and open the notebook:

```bash
unzip 2210356036.zip
jupyter notebook <extracted_notebook>.ipynb
```

## Key Learnings

- Applied and compared multiple classifiers (e.g., decision trees, SVM, k-NN) on real-world tabular datasets
- Handled class imbalance and evaluated models using precision, recall, and F1 score in addition to accuracy
- Explored the effect of feature scaling on distance-based and gradient-based classifiers
