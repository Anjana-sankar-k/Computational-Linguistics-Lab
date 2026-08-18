import re
from collections import Counter


# --------------------------------------------------
# 1. TOKENIZE CORPUS AND CREATE VOCABULARY
# --------------------------------------------------

corpus = """
the cat sat on the mat
the cat ate the fish
the dog sat on the mat
the dog ate the food
the fish was on the mat
"""

# Get words from corpus
words = re.findall(r"[a-z]+", corpus.lower())

# Unique vocabulary
vocabulary = set(words)

print("Vocabulary:")
print(vocabulary)


# --------------------------------------------------
# 2. CREATE BIGRAM FREQUENCY TABLE
# --------------------------------------------------

bigram_counts = Counter()

for i in range(len(words) - 1):
    bigram = (words[i], words[i + 1])
    bigram_counts[bigram] += 1

print("\nBigram Frequencies:")
for bigram, count in bigram_counts.items():
    print(bigram, ":", count)


# Count how many times each word occurs
word_counts = Counter(words)


# --------------------------------------------------
# BIGRAM PROBABILITY
# P(word2 | word1)
# --------------------------------------------------

def bigram_probability(word1, word2):

    # Add-one smoothing
    numerator = bigram_counts[(word1, word2)] + 1
    denominator = word_counts[word1] + len(vocabulary)

    return numerator / denominator


# --------------------------------------------------
# 3. FIND EDIT DISTANCE 1 CANDIDATES
# --------------------------------------------------

def edit_distance_one(word):

    letters = "abcdefghijklmnopqrstuvwxyz"
    candidates = set()

    # DELETE one character
    for i in range(len(word)):
        candidate = word[:i] + word[i + 1:]
        candidates.add(candidate)

    # INSERT one character
    for i in range(len(word) + 1):
        for c in letters:
            candidate = word[:i] + c + word[i:]
            candidates.add(candidate)

    # REPLACE one character
    for i in range(len(word)):
        for c in letters:
            candidate = word[:i] + c + word[i + 1:]
            candidates.add(candidate)

    return candidates


# --------------------------------------------------
# 4. FIND BEST SPELLING CANDIDATE
# --------------------------------------------------

def correct_word(previous_word, misspelled_word):

    candidates = edit_distance_one(misspelled_word)

    # Only keep candidates that exist in vocabulary
    candidates = candidates.intersection(vocabulary)

    if not candidates:
        return misspelled_word

    # Choose candidate with highest bigram probability
    best_candidate = misspelled_word
    best_probability = 0

    for candidate in candidates:

        probability = bigram_probability(
            previous_word,
            candidate
        )

        if probability > best_probability:
            best_probability = probability
            best_candidate = candidate

    return best_candidate


# --------------------------------------------------
# 5. SCAN INPUT TEXT
# --------------------------------------------------

text = input("\nEnter a sentence: ")

input_words = re.findall(r"[a-z]+", text.lower())

corrected_words = []

previous_word = None

for word in input_words:

    # Word is correct
    if word in vocabulary:

        corrected_words.append(word)
        previous_word = word

    # Word is not in vocabulary
    else:

        if previous_word is not None:

            correction = correct_word(
                previous_word,
                word
            )

        else:
            # No previous word, choose any valid candidate
            candidates = edit_distance_one(word)
            candidates = candidates.intersection(vocabulary)

            if candidates:
                correction = max(
                    candidates,
                    key=lambda x: word_counts[x]
                )
            else:
                correction = word

        print(f"\nMisspelled word: {word}")
        print("Candidates:", edit_distance_one(word).intersection(vocabulary))
        print("Suggested correction:", correction)

        corrected_words.append(correction)
        previous_word = correction


# --------------------------------------------------
# FINAL SENTENCE
# --------------------------------------------------

print("\nCorrected sentence:")
print(" ".join(corrected_words))
