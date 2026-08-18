import re
import math
from collections import Counter
from sklearn.linear_model import LogisticRegression


# ============================================================
# 1. CONFUSION SETS
# ============================================================

CONFUSION_SETS = [
    {"write", "right", "rite"},
    {"peace", "piece"},
    {"their", "there", "they're"}
]


# ============================================================
# 2. TRAINING DATA
#    Each sentence has the CORRECT word marked.
# ============================================================

TRAIN_DATA = [

    # write / right / rite
    ("I want to write a letter", "write"),
    ("Please write your name", "write"),
    ("She will write a story", "write"),
    ("He can write very well", "write"),

    ("Turn right at the corner", "right"),
    ("Take a right turn", "right"),
    ("You are right about this", "right"),
    ("The shop is on the right", "right"),

    ("The wedding rite was beautiful", "rite"),
    ("They performed the ancient rite", "rite"),

    # peace / piece
    ("We all want peace", "peace"),
    ("The country needs peace", "peace"),
    ("They finally made peace", "peace"),

    ("I ate a piece of cake", "piece"),
    ("Give me a piece of paper", "piece"),
    ("She broke a piece of glass", "piece"),

    # their / there / they're
    ("Their house is beautiful", "their"),
    ("I like their new car", "their"),
    ("Their dog is friendly", "their"),

    ("The book is there", "there"),
    ("Put the bag there", "there"),
    ("There is a problem", "there"),

    ("They're going to school", "they're"),
    ("They're very happy", "they're"),
    ("I think they're coming", "they're"),
]


# ============================================================
# 3. BUILD WORD AND BIGRAM COUNTS
# ============================================================

all_words = []

for sentence, correct_word in TRAIN_DATA:
    words = re.findall(r"[a-z']+", sentence.lower())
    all_words.extend(words)

unigram_counts = Counter(all_words)

bigram_counts = Counter()

for sentence, correct_word in TRAIN_DATA:
    words = re.findall(r"[a-z']+", sentence.lower())

    for i in range(len(words) - 1):
        bigram_counts[(words[i], words[i + 1])] += 1

vocabulary_size = len(unigram_counts)


# ============================================================
# 4. PROBABILITY FUNCTIONS
# ============================================================

def unigram_probability(word):
    """
    P(word)
    Add-one smoothing is used.
    """
    return (
        unigram_counts[word] + 1
    ) / (
        sum(unigram_counts.values()) + vocabulary_size
    )


def bigram_probability(word1, word2):
    """
    P(word2 | word1)
    """
    return (
        bigram_counts[(word1, word2)] + 1
    ) / (
        unigram_counts[word1] + vocabulary_size
    )


# ============================================================
# 5. FEATURE EXTRACTION
# ============================================================

def extract_features(candidate, previous_word, next_word,
                     original_word):

    # Feature 1: Unigram log probability
    unigram_feature = math.log(
        unigram_probability(candidate)
    )

    # Feature 2: Left bigram probability
    left_bigram_feature = math.log(
        bigram_probability(previous_word, candidate)
    )

    # Feature 3: Right bigram probability
    right_bigram_feature = math.log(
        bigram_probability(candidate, next_word)
    )

    # Feature 4: Exact match flag
    exact_match = int(candidate == original_word)

    return [
        unigram_feature,
        left_bigram_feature,
        right_bigram_feature,
        exact_match
    ]


# ============================================================
# 6. CREATE TRAINING FEATURES
# ============================================================

X = []
y = []

for sentence, correct_word in TRAIN_DATA:

    words = re.findall(r"[a-z']+", sentence.lower())

    for i, word in enumerate(words):

        # Only train on confusion-set words
        confusion_set = None

        for group in CONFUSION_SETS:
            if word in group:
                confusion_set = group
                break

        if confusion_set is None:
            continue

        # Get context
        previous_word = words[i - 1] if i > 0 else "<START>"
        next_word = words[i + 1] if i < len(words) - 1 else "<END>"

        # Evaluate every candidate
        for candidate in confusion_set:

            features = extract_features(
                candidate,
                previous_word,
                next_word,
                word
            )

            X.append(features)

            # 1 = correct candidate
            # 0 = incorrect candidate
            y.append(int(candidate == correct_word))


# ============================================================
# 7. TRAIN LOGISTIC REGRESSION
# ============================================================

model = LogisticRegression()

model.fit(X, y)

print("Model trained successfully!")


# ============================================================
# 8. FIND CONFUSION SET FOR A WORD
# ============================================================

def get_confusion_set(word):

    for group in CONFUSION_SETS:
        if word in group:
            return group

    return None


# ============================================================
# 9. CORRECT A WORD
# ============================================================

def correct_word(words, index):

    original_word = words[index]

    confusion_set = get_confusion_set(original_word)

    if confusion_set is None:
        return original_word

    previous_word = (
        words[index - 1]
        if index > 0
        else "<START>"
    )

    next_word = (
        words[index + 1]
        if index < len(words) - 1
        else "<END>"
    )

    candidates = list(confusion_set)

    feature_list = []

    for candidate in candidates:

        features = extract_features(
            candidate,
            previous_word,
            next_word,
            original_word
        )

        feature_list.append(features)

    # Logistic Regression probabilities
    probabilities = model.predict_proba(feature_list)[:, 1]

    # Find candidate with highest P(y=1)
    best_index = probabilities.argmax()

    best_candidate = candidates[best_index]

    print("\nTarget:", original_word)

    for candidate, probability in zip(
        candidates, probabilities
    ):
        print(
            f"{candidate:8} -> "
            f"{probability:.4f}"
        )

    print("Selected:", best_candidate)

    return best_candidate


# ============================================================
# 10. PROCESS INPUT SENTENCE
# ============================================================

def correct_sentence(sentence):

    words = re.findall(r"[a-z']+", sentence.lower())

    corrected_words = []

    for i, word in enumerate(words):

        if get_confusion_set(word):

            corrected = correct_word(words, i)

        else:
            corrected = word

        corrected_words.append(corrected)

    return " ".join(corrected_words)


# ============================================================
# 11. MAIN PROGRAM
# ============================================================

text = input("Enter a sentence: ")

result = correct_sentence(text)

print("\nOriginal:")
print(text)

print("\nCorrected:")
print(result)
