import re
import random

# Pronoun substitutions
REFLECTIONS = {
    "i": "you",
    "me": "you",
    "my": "your",
    "mine": "yours",
    "myself": "yourself",
    "am": "are"
}

# ELIZA Therapist Rules
THERAPIST_RULES = [

    (r"I need (.*)", [
        "Why do you need {0}?",
        "Would getting {0} really help you?",
        "What would it mean if you got {0}?"
    ]),

    (r"I am (.*)", [
        "How long have you been {0}?",
        "Why do you think you are {0}?",
        "How does being {0} make you feel?"
    ]),

    (r"I feel (.*)", [
        "Why do you feel {0}?",
        "Do you often feel {0}?",
        "Can you tell me more about feeling {0}?"
    ]),

    (r"I want (.*)", [
        "Why do you want {0}?",
        "What would happen if you got {0}?",
        "Do you think getting {0} would make you happy?"
    ]),

    (r"I can't (.*)", [
        "Why can't you {0}?",
        "What makes you think you can't {0}?",
        "Have you always felt that you couldn't {0}?"
    ]),

    (r"My (.*)", [
        "Tell me more about your {0}.",
        "How does your {0} affect you?",
        "Why is your {0} important to you?"
    ]),

    (r"Because (.*)", [
        "Is that the real reason?",
        "Does that reason explain everything?",
        "What other reasons might there be?"
    ]),

    (r"Yes", [
        "You seem quite certain.",
        "I see. Can you tell me more?"
    ]),

    (r"No", [
        "Why not?",
        "Can you explain why?",
        "Are you sure?"
    ]),

    (r"(.*)", [
        "Please tell me more.",
        "Can you elaborate on that?",
        "How does that make you feel?",
        "Why do you say that?",
        "I understand. Please continue."
    ])
]


def reflect(text):
    """
    Replace first-person words with second-person words.
    Example:
        'my family likes me'
        -> 'your family likes you'
    """
    words = text.lower().split()

    for i, word in enumerate(words):
        if word in REFLECTIONS:
            words[i] = REFLECTIONS[word]

    return " ".join(words)


def generate_response(user_input):
    """
    Matches user input against therapist rules
    and returns an appropriate response.
    """

    if user_input.strip().upper() == "BYE BYE":
        return None

    for pattern, responses in THERAPIST_RULES:

        match = re.match(pattern, user_input, re.IGNORECASE)

        if match:

            groups = match.groups()

            reflected_groups = [
                reflect(group) if group else ""
                for group in groups
            ]

            response = random.choice(responses)

            return response.format(*reflected_groups)

    return "Please tell me more."


def main():

    print("=" * 60)
    print("              ELIZA THERAPIST")
    print("        Type 'BYE BYE' to end the chat.")
    print("=" * 60)

    print("\nTherapist: Hello. I'm here to listen.")
    print("Therapist: What would you like to talk about today?")

    while True:

        try:
            user_input = input("\nYou: ")

        except (KeyboardInterrupt, EOFError):
            print("\nTherapist: Goodbye.")
            break

        response = generate_response(user_input)

        if response is None:
            print("\nTherapist: Goodbye. Take care. BYE BYE!")
            break

        print("\nTherapist:", response)


if __name__ == "__main__":
    main()
