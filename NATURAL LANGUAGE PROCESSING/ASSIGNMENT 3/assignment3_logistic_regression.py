import string
import re
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.exceptions import ConvergenceWarning
import warnings

warnings.filterwarnings(
    "ignore", category=UserWarning
)  # It hides unnecessary warning messages
warnings.filterwarnings("ignore", category=ConvergenceWarning)

nltk.download("stopwords")


# Preprocessing
def preprocess_text(text):
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)  # Remove punctuation
    text = re.sub(r"\d+", " ", text)  # Remove numbers
    text = text.lower()
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    text = re.sub(r"\s+", " ", " ".join(words)).strip()  # Remove extra spaces
    return text


# Load dataset
dataset = load_dataset("imdb")
train_df = pd.DataFrame(dataset["train"])
test_df = pd.DataFrame(dataset["test"])

train_df["text"] = train_df["text"].apply(preprocess_text)
test_df["text"] = test_df["text"].apply(preprocess_text)


# Bias Score Calculation
def bias_scores(df):
    # Splits the texts into positive and negative reviews separately.
    pos_texts = df[df["label"] == 1]["text"]
    neg_texts = df[df["label"] == 0]["text"]

    pos_counter = Counter()
    neg_counter = Counter()

    for text in pos_texts:
        pos_counter.update(text.split())
    for text in neg_texts:
        neg_counter.update(text.split())

    all_words = set(pos_counter.keys()).union(set(neg_counter.keys()))
    scores = []

    for word in all_words:
        fp = pos_counter.get(word, 0)  # frequency in positive reviews
        fn = neg_counter.get(word, 0)  # frequency in negative reviews
        ft = fp + fn  # total frequency (positive + negative)
        if ft == 0:
            continue
        bias_score = abs(fp - fn) / ft * math.log(ft)
        bias_score = float(f"{bias_score:.10f}")
        scores.append((word, fp, fn, ft, bias_score))

    def sort_key(item):
        return (-item[4], item[0])

    scores.sort(key=sort_key)
    return scores[:10000]


# Feature Extraction
scores = bias_scores(train_df)
top_words = [word for word, _, _, _, _ in scores]

vectorizer = CountVectorizer(vocabulary=top_words)
X_train = vectorizer.transform(train_df["text"]).toarray()
X_test = vectorizer.transform(test_df["text"]).toarray()

y_train = train_df["label"].values
y_test = test_df["label"].values

# Logistic Regression Training
train_accuracies = []
test_accuracies = []

for max_iter in range(1, 26):
    model = LogisticRegression(max_iter=max_iter, solver="lbfgs")
    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    train_acc = accuracy_score(y_train, train_preds)
    test_acc = accuracy_score(y_test, test_preds)

    train_accuracies.append(train_acc)
    test_accuracies.append(test_acc)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(range(1, 26), train_accuracies, label="Training Accuracy", marker="o")
plt.plot(range(1, 26), test_accuracies, label="Test Accuracy", marker="x")
plt.title("Logistic Regression Accuracy vs Max Iterations")
plt.xlabel("Max Iterations")
plt.ylabel("Accuracy")
plt.xticks(range(1, 26))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Show bias scores examples
print(scores[:2])
print(scores[-2:])

"""
# Analysis:
In this assignment, we explored the behavior of a Logistic Regression classifier as the maximum number of iterations increased from 1 to 25. The plotted graph clearly shows a strong learning pattern during the early stages.

Initially, with only a few iterations (between 1 and 5), both the training and test accuracies rise sharply. This is expected because the model starts learning the most basic, easy-to-separate patterns in the IMDB sentiment data. During this phase, the model is underfitting — it hasn't learned enough yet.

Between 5 and 15 iterations, we observe a continued steady improvement. The training accuracy moves up smoothly, and the test accuracy also improves alongside it. This is the sweet spot where the model is learning complex decision boundaries but still generalizing well to unseen data.

After about 15 to 17 iterations, the test accuracy curve flattens out and even slightly fluctuates. Meanwhile, the training accuracy keeps rising. This is a classic early sign of overfitting: the model is starting to "memorize" the training data rather than "understanding" the general patterns. Even though the training score looks great (~94%), the test accuracy (~87%) doesn't improve anymore — sometimes it even drops a tiny bit.

Thus, based on the graph, the optimal choice would be using around 16 to 18 iterations. At this point, the model achieves a strong generalization ability without overfitting much. Beyond 18 iterations, adding more iterations brings almost no benefits and may even harm the performance slightly on unseen data.

To summarize: more training is not always better. It’s all about finding the balance between learning enough and not memorizing too much!

In a real-world NLP project, I would stop the training early based on validation performance (early stopping), but for this assignment, observing this behavior through the graph gives exactly the insights we expect.

Overall, the logistic regression model performed impressively well given such a simple Bag-of-Words representation — showing how strong even basic methods can be when used correctly.

"""
