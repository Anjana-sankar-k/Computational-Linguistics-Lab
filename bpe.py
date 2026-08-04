corpus = [
    "low",
    "lower",
    "lowest",
    "newest",
    "widest"
]

def initialize_vocab(words):
    vocab = {}

    for word in words:
        chars = " ".join(list(word)) + " </w>"
        vocab[chars] = vocab.get(chars,0)+1

    return vocab


vocab = initialize_vocab(corpus)

print("Initial Vocabulary:")
for word,count in vocab.items():
    print(word, ":", count)


def get_pairs(vocab):

    pairs = {}

    for word,freq in vocab.items():

        symbols = word.split()

        for i in range(len(symbols)-1):

            pair = (symbols[i],symbols[i+1])

            pairs[pair] = pairs.get(pair,0)+freq

    return pairs


def merge_vocab(pair,vocab):

    new_vocab={}

    bigram = " ".join(pair)

    replacement = "".join(pair)


    for word,freq in vocab.items():

        new_word = word.replace(
            bigram,
            replacement
        )

        new_vocab[new_word]=freq


    return new_vocab


num_merges = 10


for i in range(num_merges):

    pairs = get_pairs(vocab)


    if not pairs:
        break


    best_pair=max(
        pairs,
        key=pairs.get
    )


    print("\nStep",i+1)

    print("Most frequent pair:",
          best_pair,
          "frequency:",
          pairs[best_pair])


    vocab=merge_vocab(
        best_pair,
        vocab
    )


    print("Updated vocabulary:")

    for word in vocab:
        print(word)


