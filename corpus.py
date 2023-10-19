from collections import Counter


def get_grams(file, valid):
    """
    opens tsv file and converts it into Counter dict with gram and freq as columns
    """
    grams = Counter()

    with open(file) as f:
        for l in f:
            chars, freq = l.strip().split("\t")

            if all(c in valid for c in chars):
                grams[chars] = int(freq)

    return grams
