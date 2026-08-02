def plural_y_fsa(word):

    vowels = "aeiou"

    # Case 1 : vowel + y + s
    if len(word) >= 3:
        if word[-1] == 's' and word[-2] == 'y':
            if word[-3] in vowels:
                return True

    # Case 2 : consonant + ies
    if len(word) >= 4:
        if word.endswith("ies"):
            if word[-4] not in vowels:
                return True

    return False

words = [
    "boys",
    "toys",
    "ponies",
    "skies",
    "puppies",
    "boies",
    "toies",
    "ponys"
]

for w in words:
    print(w, plural_y_fsa(w))
