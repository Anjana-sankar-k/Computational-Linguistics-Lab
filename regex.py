import re

# 1. Define the compiled regular expressions
# Note: re.M (MULTILINE) allows ^ and $ to match the start/end of individual lines
patterns = {
    "a. Consecutive repeated words": re.compile(r'\b([A-Za-z]+)\s+\1\b', re.I),
    "b. Starts with int, ends with word": re.compile(r'^\d+.*\b[A-Za-z]+\b$', re.M),
    "c. Contains both 'grotto' and 'raven'": re.compile(r'\b(grotto\b.*\braven|raven\b.*\bgrotto)\b', re.I),
    "d. First word of a sentence (Captured in Group 1)": re.compile(r'(?:^|[\.!?]\s+)([A-Za-z]+)')
}

def process_text(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return

    print("=== REGULAR EXPRESSION MATCHING RESULTS ===\n")

    # Pattern A: Consecutive repeated words
    print("--- A. Consecutive Repeated Words ---")
    for match in patterns["a. Consecutive repeated words"].finditer(content):
        print(f"Matched text: '{match.group(0)}' (Repeated word: '{match.group(1)}')")

    # Pattern B: Line starting with integer, ending with word
    print("\n--- B. Starts with Int, Ends with Word ---")
    # We finditer across the whole file; re.M handles the line-by-line logic
    for match in patterns["b. Starts with int, ends with word"].finditer(content):
        print(f"Matched Line: '{match.group(0)}'")

    # Pattern C: Both grotto and raven
    print("\n--- C. Contains both 'grotto' and 'raven' ---")
    # For this pattern, it's often easiest to check line by line to show local context
    for line_num, line in enumerate(content.splitlines(), 1):
        if patterns["c. Contains both 'grotto' and 'raven'"].search(line):
            print(f"Line {line_num}: '{line.strip()}'")

    # Pattern D: First word of a sentence placed in a register
    print("\n--- D. First Word of a Sentence (Register 1) ---")
    for match in patterns["d. First word of a sentence (Captured in Group 1)"].finditer(content):
        print(f"Sentence starter found! Register 1 holds: '{match.group(1)}'")

if __name__ == "__main__":
    # Create a sample input file to demonstrate functionality if it doesn't exist
    sample_content = """Humbert Humbert went to the store. The bug was not the the bug he wanted.
42 blocks away, there was a hidden cavern.
They found a deep grotto near the raven nest.
However, grottos and ravenous birds don't count.
The raven flew into the dark grotto swiftly!
Hello world! This is a test. Is it working? Yes.
"""
    
    import os
    if not os.path.exists("input.txt"):
        with open("input.txt", "w", encoding="utf-8") as f:
            f.write(sample_content)
        print("Created sample 'input.txt' file for demonstration.")

    process_text("input.txt")
