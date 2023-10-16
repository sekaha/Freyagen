from collections import Counter


def get_grams(file):
    """
    opens tsv file and converts it into Counter dict with gram and freq as columns
    """
    grams = Counter()

    with open(file) as f:
        for l in f:
            chrs, freq = l.strip().split("\t")
            grams[chrs] = int(freq)

    return grams


bigrams = get_grams("res/bigrams.txt")
