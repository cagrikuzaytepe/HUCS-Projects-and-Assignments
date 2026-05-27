import hashlib
import random
from typing import Dict, List, Tuple

import numpy as np
import gensim.downloader

# pip install --quiet --upgrade "numpy>=1.25" "gensim>=4.3"   // I used this version

# Load the model.
_MODEL = gensim.downloader.load("word2vec-google-news-300")
_VECTOR_SIZE = _MODEL.vector_size


def _token_rng(token: str) -> random.Random:
    seed = int(hashlib.md5(token.encode()).hexdigest(), 16)
    return random.Random(seed)


def replace_with_similar(
    sentence: str,
    indices: List[int],
    *,
    topn: int = 5,
) -> Tuple[str, Dict[str, List[Tuple[str, float]]]]:
    tokens = sentence.split()
    similar_words_dict: Dict[str, List[Tuple[str, float]]] = {}

    for idx in indices:
        original = tokens[idx]
        sims = _MODEL.most_similar(original, topn=topn)
        similar_words_dict[original] = sims
        tokens[idx] = _token_rng(original).choice(sims)[0]

    return " ".join(tokens), similar_words_dict


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return 0.0 if denom == 0.0 else float(np.dot(a, b) / denom)


def sentence_vector(
    sentence: str,
) -> Tuple[Dict[str, np.ndarray], np.ndarray]:
    tokens = sentence.split()
    vec_dict: Dict[str, np.ndarray] = {}

    for tok in tokens:
        if tok not in vec_dict:  # only first occurrence kept
            vec_dict[tok] = (
                _MODEL[tok]
                if tok in _MODEL
                else np.zeros(_VECTOR_SIZE, dtype=np.float32)
            )

    sent_vec = (
        np.mean(list(vec_dict.values()), axis=0)
        if vec_dict
        else np.zeros(_VECTOR_SIZE, dtype=np.float32)
    )
    return vec_dict, sent_vec


def most_similar_sentences(
    file_path: str,
    query: str,
) -> List[Tuple[str, float]]:
    _, q_vec = sentence_vector(query)

    sims: List[Tuple[str, float]] = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            s = line.rstrip("\n")
            _, s_vec = sentence_vector(s)
            sims.append((s, _cosine(q_vec, s_vec)))

    sims.sort(key=lambda t: t[1], reverse=True)
    return sims[:20]


""" 
if __name__ == "__main__":
    with open("output.txt", "w", encoding="utf-8") as f:
        sentence = "NLP is a fascinating field of study and I love learning about it"
        indices = [3, 4, 10]
        new_sentence, most_similar_dict = replace_with_similar(sentence, indices)

        print(most_similar_dict.keys(), end="\n\n", file=f)
        print(most_similar_dict["fascinating"], end="\n\n", file=f)
        print(most_similar_dict["field"], end="\n\n", file=f)
        print(most_similar_dict["learning"], end="\n\n", file=f)
        print(new_sentence, end="\n\n", file=f)

        print(
            "----------------------------------------------------------------------------------------------------",
            end="\n\n",
            file=f,
        )

        vector_dict, sentence_vec = sentence_vector(
            "I am a student studying NLP at Hacettepe University"
        )
        print(vector_dict.keys(), end="\n\n", file=f)
        print(vector_dict["I"][:5], end="\n\n", file=f)
        print(vector_dict["studying"][145:150], end="\n\n", file=f)
        print(vector_dict["Hacettepe"][295:], end="\n\n", file=f)

        print(
            "----------------------------------------------------------------------------------------------------",
            end="\n\n",
            file=f,
        )

        file_path = "sentences.txt"

        query1 = "Is swimming a good sport ?"
        results1 = most_similar_sentences(file_path, query1)
        for sentence, score in results1[:3]:
            print(f"{score:.5f} -> {sentence}", end="\n\n", file=f)

        print("--------------------------------------------------", end="\n\n", file=f)

        query2 = "Does Turkey have good universities ?"
        results2 = most_similar_sentences(file_path, query2)
        for sentence, score in results2[:3]:
            print(f"{score:.5f} -> {sentence}", end="\n\n", file=f)

        print("--------------------------------------------------", end="\n\n", file=f)

        query3 = "What happened to your backpack ?"
        results3 = most_similar_sentences(file_path, query3)
        for sentence, score in results3[:3]:
            print(f"{score:.5f} -> {sentence}", end="\n\n", file=f)
 """
