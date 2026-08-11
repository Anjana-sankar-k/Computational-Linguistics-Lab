import re

# 1. Create the dummy input file
sample_text = """Humbert Humbert went to the store.
the big bug was not the the one he wanted.
42 answers were given by the wise raven.
7 birds flew into a mysterious grotto.
The raven flew into the grotto quietly.
grottos are cool, but a raven is cooler.
...First impressions matter a lot.
"Welcome to the jungle," said the guide.
"""

input_filename = "input_text.txt"
with open(input_filename, "w") as f:
    f.write(sample_text)

# 2. Updated Regular Expression Patterns
regex_a = re.compile(r"\b([a-zA-Z]+)\s+\1\b")

# FIXED B: Allows for optional punctuation (like .) at the end of the line
regex_b = re.compile(r"^\d+.*\b[a-zA-Z]+\b[.,!?\"'\s]*$", re.MULTILINE)

regex_c = re.compile(r"^(?=.*\bgrotto\b)(?=.*\braven\b).*$", re.MULTILINE)

# D: Captures the first word. (Note: For line 3, it correctly registers 'answers')
regex_d = re.compile(r"^[^a-zA-Z]*([a-zA-Z]+)", re.MULTILINE)

# 3. Read and Process
print("--- PROCESSING FILE INPUT ---\n")

with open(input_filename, "r") as file:
    content = file.read()
    lines = content.splitlines()

    print("=== Task A: Consecutive Repeated Words ===")
    matches_a = regex_a.findall(content)
    for match in matches_a:
        print(f"Found consecutive repetition of: '{match}'")
        
    print("\n=== Task B: Starts with Integer, Ends with Word ===")
    for line in lines:
        if regex_b.match(line):
            print(f"Matched Line: '{line}'")

    print("\n=== Task C: Contains both 'grotto' and 'raven' ===")
    for line in lines:
        if regex_c.match(line):
            print(f"Matched Line: '{line}'")

    print("\n=== Task D: Register First Word of Sentences ===")
    for line in lines:
        match = regex_d.search(line)
        if match:
            print(f"Line: '{line}' -> First Word Register: '{match.group(1)}'")
