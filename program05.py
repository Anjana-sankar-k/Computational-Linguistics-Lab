def fst_plural(word):

    # Split lexical form at morpheme boundary
    root, suffix = word.split("^")

    output = ""

    # Copy root characters
    output += root

    # e-insertion rule
    if root[-1] in ['x', 's', 'z'] and suffix == 's':
        output += 'e'

    # Add suffix
    output += suffix

    return output

words = [
    "box^s",
    "bus^s",
    "quiz^s",
    "cat^s",
    "dog^s"
]

for w in words:
    print(w, "→", fst_plural(w))
