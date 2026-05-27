import codecs

"""
Assignment 1 - Code template for AIN442/BBM497

@author: İsmail Furkan Atasoy
"""


def initialVocabulary():
    return list(
        "abcçdefgğhıijklmnoöprsştuüvyzwxq"
        + "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZWXQ"
        + "0123456789 "
        + "!'^#+$%&/{([)]=}*?\\_-<>|.:´,;`@€¨~\"é"
    )


def bpeCorpus(corpus, maxMergeCount=10):
    words = corpus.split()

    tokenized_corpus = []
    for word in words:
        tokens = [" "] + list(word) + ["_"]
        tokenized_corpus.append(tokens)

    vocabulary = initialVocabulary()[:]

    merges = []

    for _ in range(maxMergeCount):
        pair_counts = {}
        for tokens in tokenized_corpus:
            for i in range(len(tokens) - 1):
                pair = (tokens[i], tokens[i + 1])
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

        if not pair_counts:
            break

        max_count = max(pair_counts.values())

        candidates = [p for p, c in pair_counts.items() if c == max_count]

        most_freq_pair = min(candidates)

        merges.append((most_freq_pair, pair_counts[most_freq_pair]))

        new_token = most_freq_pair[0] + most_freq_pair[1]

        vocabulary.append(new_token)

        for w_idx, tokens in enumerate(tokenized_corpus):
            merged_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == most_freq_pair:
                    merged_tokens.append(new_token)
                    i += 2
                else:
                    merged_tokens.append(tokens[i])
                    i += 1
            tokenized_corpus[w_idx] = merged_tokens

    return (merges, vocabulary, tokenized_corpus)


def bpeFN(fn, maxMergeCount=10):
    with codecs.open(fn, "r", encoding="utf-8") as f:
        corpus_text = f.read()

    return bpeCorpus(corpus_text, maxMergeCount)


def bpeTokenize(str, merges):
    words = str.split()

    tokenized_words = []
    for word in words:
        tokens = [" "] + list(word) + ["_"]
        tokenized_words.append(tokens)

    for pair, _count in merges:
        new_token = pair[0] + pair[1]

        for w_idx, tokens in enumerate(tokenized_words):
            merged_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
                    merged_tokens.append(new_token)
                    i += 2
                else:
                    merged_tokens.append(tokens[i])
                    i += 1
            tokenized_words[w_idx] = merged_tokens

    return tokenized_words


def bpeFNToFile(infn, maxMergeCount=10, outfn="output.txt"):
    (Merges, Vocabulary, TokenizedCorpus) = bpeFN(infn, maxMergeCount)
    outfile = open(outfn, "w", encoding="utf-8")
    outfile.write("Merges:\n")
    outfile.write(str(Merges))
    outfile.write("\n\nVocabulary:\n")
    outfile.write(str(Vocabulary))
    outfile.write("\n\nTokenizedCorpus:\n")
    outfile.write(str(TokenizedCorpus))
    outfile.close()


if __name__ == "__main__":
    print("\n----- bpeFN('hw01_tiny.txt') with default maxMergeCount 10 -----")
    merges, vocab, tokenized = bpeFN("hw01_tiny.txt")
    print("Merges:", merges)
    print("Vocabulary:", vocab)
    print("TokenizedCorpus:", tokenized)

    print("\n----- bpeFN('hw01_tiny.txt', maxMergeCount 100) -----")
    merges2, vocab2, tokenized2 = bpeFN("hw01_tiny.txt", 100)
    print("Merges:", merges2)
    print("Vocabulary:", vocab2)
    print("TokenizedCorpus:", tokenized2)

    print("\n----- Output for 'hw01_bilgisayar.txt' -----")
    bpeFNToFile("hw01_bilgisayar.txt", 1000, "output1.txt")
    bpeFNToFile("hw01_bilgisayar.txt", 200, "output2.txt")
    print("Check output1.txt and output2.txt for results.")
