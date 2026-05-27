import string
import re
import math
import pandas as pd
from collections import Counter
from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score

nltk.download("stopwords")


# Preprocessing Function
def preprocess_text(text):
    # Remove punctuation
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    # Remove digits
    text = re.sub(r"\d+", " ", text)
    # Lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = " ".join(words)
    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Load and Preprocess Data
dataset = load_dataset("imdb")
train_df = pd.DataFrame(dataset["train"])
test_df = pd.DataFrame(dataset["test"])

train_df["text"] = train_df["text"].apply(preprocess_text)
test_df["text"] = test_df["text"].apply(preprocess_text)


# Naive Bayes Classifier
class NaiveBayesClassifier:
    def __init__(self):
        self.total_pos_words = 0
        self.total_neg_words = 0
        self.vocab_size = 0
        self.prior_pos = 0
        self.prior_neg = 0
        self.pos_counter = Counter()
        self.neg_counter = Counter()

    def fit(self, train_df):
        pos_texts = train_df[train_df["label"] == 1]["text"]
        neg_texts = train_df[train_df["label"] == 0]["text"]

        for text in pos_texts:
            self.pos_counter.update(text.split())
        for text in neg_texts:
            self.neg_counter.update(text.split())

        self.total_pos_words = sum(self.pos_counter.values())
        self.total_neg_words = sum(self.neg_counter.values())
        self.vocab_size = len(
            set(self.pos_counter.keys()).union(set(self.neg_counter.keys()))
        )

        self.prior_pos = len(pos_texts) / len(train_df)
        self.prior_neg = len(neg_texts) / len(train_df)

    def predict(self, text):
        text = preprocess_text(text)
        words = text.split()

        log_prob_pos = math.log(self.prior_pos)
        log_prob_neg = math.log(self.prior_neg)

        for word in words:
            log_prob_pos += math.log(
                (self.pos_counter.get(word, 0) + 1)
                / (self.total_pos_words + self.vocab_size)
            )
            log_prob_neg += math.log(
                (self.neg_counter.get(word, 0) + 1)
                / (self.total_neg_words + self.vocab_size)
            )

        y_predicted = 1 if log_prob_pos > log_prob_neg else 0
        return (y_predicted, log_prob_pos, log_prob_neg)


# Testing

nb = NaiveBayesClassifier()
nb.fit(train_df)

print(nb.total_pos_words)
print(nb.total_neg_words)
print(nb.vocab_size)
print(nb.prior_pos)
print(nb.prior_neg)
print(nb.pos_counter["great"])
print(nb.neg_counter["great"])

prediction1 = nb.predict(test_df.iloc[0]["text"])
prediction2 = nb.predict("This movie will be place at 1st in my favourite movies!")
prediction3 = nb.predict(
    "I couldn't wait for the movie to end, so I turned it off halfway through. :D It was a complete disappointment."
)

print(f"{'Positive' if prediction1[0] == 1 else 'Negative'}")
print(prediction1)

print(f"{'Positive' if prediction2[0] == 1 else 'Negative'}")
print(prediction2)

print(f"{'Positive' if prediction3[0] == 1 else 'Negative'}")
print(prediction3)

print(preprocess_text("This movie will be place at 1st in my favourite movies!"))
print(
    preprocess_text(
        "I couldn't wait for the movie to end, so I turned it off halfway through. :D It was a complete disappointment."
    )
)

# Accuracy test
y_true = test_df["label"].values
y_pred = [nb.predict(text)[0] for text in test_df["text"]]

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy}")
