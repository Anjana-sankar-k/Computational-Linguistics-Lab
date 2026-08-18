import re
from collections import Counter


# --------------------------------------------------
# 1. CORPUS
# --------------------------------------------------

corpus = """
the cat sat on the mat
the cat ate the fish
the dog sat on the mat
the dog ate the food
the fish was on the mat
"""

# Tokenize corpus
words = re.findall(r"[a-z]+", corpus.lower())

# Vocabulary
vocabulary = set(words)

# Word frequencies
word_counts = Counter(words)


# --------------------------------------------------
# 2. BIGRAM FREQUENCY TABLE
# --------------------------------------------------

bigram_counts = Counter()

for i in range(len(words) - 1):
    bigram = (words[i], words[i + 1])
    bigram_counts[bigram] += 1


# --------------------------------------------------
# 3. BIGRAM PROBABILITY
# --------------------------------------------------

def bigram_probability(previous, word):

    numerator = bigram_counts[(previous, word)] + 1
    denominator = word_counts[previous] + len(vocabulary)

    return numerator / denominator


# --------------------------------------------------
# 4. EDIT DISTANCE
# --------------------------------------------------

def edit_distance(s1, s2):

    m = len(s1)
    n = len(s2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1]   # replace
                )

    return dp[m][n]


# --------------------------------------------------
# 5. GENERATE CANDIDATES
# --------------------------------------------------

def generate_candidates(word):

    candidates = []

    for candidate in vocabulary:

        # Only consider words within edit distance 1
        if edit_distance(word, candidate) == 1:
            candidates.append(candidate)

    return candidates


# --------------------------------------------------
# 6. NOISY CHANNEL PROBABILITY
# --------------------------------------------------

def noisy_channel_probability(wrong_word, candidate):

    distance = edit_distance(wrong_word, candidate)

    # Simple assumption:
    # smaller edit distance = more likely typo

    if distance == 1:
        return 1.0

    elif distance == 2:
        return 0.5

    else:
        return 0.1


# --------------------------------------------------
# 7. NOISY CHANNEL SPELL CHECKER
# --------------------------------------------------

def noisy_channel_correct(previous_word, wrong_word):

    candidates = generate_candidates(wrong_word)

    if not candidates:
        return wrong_word

    best_candidate = wrong_word
    best_score = 0

    for candidate in candidates:

        # P(wrong word | candidate)
        channel_probability = noisy_channel_probability(
            wrong_word,
            candidate
        )

        # P(candidate | previous word)
        language_probability = bigram_probability(
            previous_word,
            candidate
        )

        # Noisy Channel Model
        score = channel_probability * language_probability

        if score > best_score:
            best_score = score
            best_candidate = candidate

    return best_candidate


# --------------------------------------------------
# 8. BIGRAM-ONLY SPELL CHECKER
# --------------------------------------------------

def bigram_correct(previous_word, wrong_word):

    candidates = generate_candidates(wrong_word)

    if not candidates:
        return wrong_word

    best_candidate = wrong_word
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
# 9. SPELL CHECK INPUT
# --------------------------------------------------

def spell_check(text, method):

    input_words = re.findall(r"[a-z]+", text.lower())

    corrected = []

    previous_word = None

    for word in input_words:

        if word in vocabulary:

            corrected.append(word)
            previous_word = word

        else:

            if previous_word is not None:

                if method == "bigram":
                    correction = bigram_correct(
                        previous_word,
                        word
                    )

                else:
                    correction = noisy_channel_correct(
                        previous_word,
                        word
                    )

            else:
                correction = word

            corrected.append(correction)
            previous_word = correction

    return " ".join(corrected)


# --------------------------------------------------
# 10. MAIN PROGRAM
# --------------------------------------------------

text = input("Enter a sentence: ")

bigram_result = spell_check(text, "bigram")
noisy_result = spell_check(text, "noisy")

print("\nOriginal:")
print(text)

print("\nBigram LM Correction:")
print(bigram_result)

print("\nNoisy Channel Correction:")
print(noisy_result)
