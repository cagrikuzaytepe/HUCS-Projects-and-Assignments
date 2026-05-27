#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 15:06:51 2025

@author: ilyas
"""
import re
import random


class ngramLM:

    def __init__(self):
        self.numOfTokens = 0
        self.sizeOfVocab = 0
        self.numOfSentences = 0
        self.sentences = []
        self.unigramCounts = {}
        self.bigramCounts = {}
        self.followDict = {}

    def trainFromFile(self, fn):
        tokenPattern = re.compile(
            r"""(?x)
            (?:[A-ZÇĞIİÖŞÜ]\.)+              
            | \d+(?:\.\d*)?(?:'\w+)?   
            | \w+(?:-\w+)*(?:'\w+)?  
            | \.\.\.  
            | [][,;.?():_!#^+$%&><|/{()=}\"\'\\\"\`-]
        """
        )
        with open(fn, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line = line.replace("I", "ı").replace("İ", "i")
                tokens = tokenPattern.findall(line)
                if not tokens:
                    continue
                tokens = [token.lower() for token in tokens]
                current_sentence = []
                for token in tokens:
                    current_sentence.append(token)
                    if token in [".", "?", "!"]:
                        sentPadded = ["<s>"] + current_sentence + ["</s>"]
                        self.sentences.append(sentPadded)
                        current_sentence = []
                if current_sentence:
                    sentPadded = ["<s>"] + current_sentence + ["</s>"]
                    self.sentences.append(sentPadded)
        self.numOfSentences = len(self.sentences)
        for sent in self.sentences:
            for token in sent:
                self.numOfTokens += 1
                self.unigramCounts[token] = self.unigramCounts.get(token, 0) + 1
            for i in range(len(sent) - 1):
                bigram = (sent[i], sent[i + 1])
                self.bigramCounts[bigram] = self.bigramCounts.get(bigram, 0) + 1
        self.sizeOfVocab = len(self.unigramCounts)
        self.followDict = {}
        for (w1, w2), count in self.bigramCounts.items():
            self.followDict.setdefault(w1, []).append((w2, count))
        for w1 in self.followDict:
            self.followDict[w1].sort(key=lambda x: (-x[1], x[0]))

    def vocab(self):
        return sorted(self.unigramCounts.items(), key=lambda x: (-x[1], x[0]))

    def bigrams(self):
        return sorted(self.bigramCounts.items(), key=lambda x: (-x[1], x[0]))

    def unigramCount(self, word):
        return self.unigramCounts.get(word, 0)

    def bigramCount(self, bigram):
        return self.bigramCounts.get(bigram, 0)

    def unigramProb(self, word):
        if word not in self.unigramCounts:
            return 0
        return self.unigramCounts[word] / self.numOfTokens

    def bigramProb(self, bigram):
        w1, w2 = bigram
        if w1 not in self.unigramCounts:
            return 0
        return self.bigramCounts.get(bigram, 0) / self.unigramCounts[w1]

    def unigramProb_SmoothingUNK(self, word):
        return (self.unigramCounts.get(word, 0) + 1) / (
            self.numOfTokens + self.sizeOfVocab + 1
        )

    def bigramProb_SmoothingUNK(self, bigram):
        w1, w2 = bigram
        if w1 not in self.unigramCounts:
            return 1 / (self.sizeOfVocab + 1)
        return (self.bigramCounts.get(bigram, 0) + 1) / (
            self.unigramCounts[w1] + self.sizeOfVocab + 1
        )

    def sentenceProb(self, sent):
        if len(sent) < 2:
            return self.unigramProb_SmoothingUNK(sent[0]) if sent else 0
        prob = 1.0
        for i in range(len(sent) - 1):
            prob *= self.bigramProb_SmoothingUNK((sent[i], sent[i + 1]))
        return prob

    def generateSentence(self, sent=["<s>"], maxFollowWords=1, maxWordsInSent=20):
        current = list(sent)
        words_generated = 0
        while words_generated < maxWordsInSent:
            last = current[-1]
            if last == "</s>":
                break
            if last not in self.followDict or not self.followDict[last]:
                break
            k = maxFollowWords if maxFollowWords >= 1 else 1
            candidates = self.followDict[last][:k]
            total = sum(freq for (_, freq) in candidates)
            rnd = random.randint(1, total)
            cum = 0
            next_word = None
            for token, freq in candidates:
                cum += freq
                if rnd <= cum:
                    next_word = token
                    break
            if next_word is None:
                break
            current.append(next_word)
            words_generated += 1
            if next_word == "</s>":
                break
        if current[-1] != "</s>":
            current.append("</s>")
        return current


def main():
    lm = ngramLM()
    lm.trainFromFile("hw02_tinyTestCorpus.txt")

    with open("output11.txt", "w", encoding="utf-8") as f:

        print(lm.numOfTokens, file=f)
        print(lm.sizeOfVocab, file=f)
        print(lm.numOfSentences, file=f)

        print(lm.sentences, file=f)
        print(lm.vocab(), file=f)
        print(lm.bigrams(), file=f)

        print(lm.unigramCount("a"), file=f)
        print(lm.unigramCount("b"), file=f)
        print(lm.unigramCount("g"), file=f)

        print(lm.unigramProb("a"), file=f)
        print(lm.unigramProb("b"), file=f)
        print(lm.unigramProb("g"), file=f)

        print(lm.bigramCount(("a", "b")), file=f)
        print(lm.bigramCount(("b", "a")), file=f)
        print(lm.bigramCount(("a", "g")), file=f)
        print(lm.bigramCount(("g", "a")), file=f)
        print(lm.bigramCount(("g", "g")), file=f)

        print(lm.bigramProb(("a", "b")), file=f)
        print(lm.bigramProb(("b", "a")), file=f)
        print(lm.bigramProb(("g", "a")), file=f)
        print(lm.bigramProb(("a", "g")), file=f)
        print(lm.bigramProb(("g", "g")), file=f)

        print(lm.unigramProb_SmoothingUNK("a"), file=f)
        print(lm.unigramProb_SmoothingUNK("b"), file=f)
        print(lm.unigramProb_SmoothingUNK("g"), file=f)

        print(lm.bigramProb_SmoothingUNK(("a", "b")), file=f)
        print(lm.bigramProb_SmoothingUNK(("b", "a")), file=f)
        print(lm.bigramProb_SmoothingUNK(("g", "a")), file=f)
        print(lm.bigramProb_SmoothingUNK(("a", "g")), file=f)
        print(lm.bigramProb_SmoothingUNK(("g", "g")), file=f)

        print(lm.sentenceProb(["<s>", "a", "f", "d", ".", "</s>"]), file=f)
        print(lm.sentenceProb(["<s>", "a", "c", "d", ".", "</s>"]), file=f)
        print(lm.sentenceProb(["<s>", "a", "b", "c", "d", ".", "</s>"]), file=f)
        print(lm.sentenceProb(["<s>", "</s>"]), file=f)
        print(lm.sentenceProb(["<s>"]), file=f)
        print(lm.sentenceProb(["a"]), file=f)


if __name__ == "__main__":
    main()
