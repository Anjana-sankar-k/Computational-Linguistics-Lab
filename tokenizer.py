import re
def tokenize(text):
    
    # Split common contractions
    text = re.sub(r"(\w+)n't\b", r"\1 n't", text)
    text = re.sub(r"(\w+)'re\b", r"\1 're", text)
    text = re.sub(r"(\w+)'ve\b", r"\1 've", text)
    text = re.sub(r"(\w+)'ll\b", r"\1 'll", text)
    text = re.sub(r"(\w+)'d\b", r"\1 'd", text)
    text = re.sub(r"(\w+)'m\b", r"\1 'm", text)
    text = re.sub(r"(\w+)'s\b", r"\1 's", text)

    # Regex pattern
    pattern = r"""
        (?:[A-Za-z]\.){2,}[A-Za-z]?\.?      # Abbreviations (U.S.A.)
        |
        [A-Za-z]+(?:-[A-Za-z]+)+            # Hyphenated words
        |
        \d+(?:\.\d+)?                       # Numbers
        |
        [A-Za-z]+                           # Normal words
        |
        '[A-Za-z]+                          # Contraction parts ('re, 've, etc.)
        |
        [^\w\s]                             # Punctuation / symbols
    """

    tokens = re.findall(pattern, text, re.VERBOSE)

    return tokens

text = "U.S.A. isn't famous only for ice-cream! It's amazing, isn't it?"

tokens = tokenize(text)

print(tokens)
