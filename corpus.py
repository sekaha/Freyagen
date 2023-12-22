from collections import Counter


def get_grams(file, valid, percent=1.0):
    """
    opens tsv file and converts it into Counter dict with gram and freq as columns
    """
    grams = Counter()

    with open(file) as f:
        for l in f:
            chars, freq = l.strip().split("\t")

            if all(c in valid for c in chars):
                grams[chars] = int(freq)

    if percent < 1.0:
        total = sum(grams.values())
        target = total * percent
        elapsed = 0

        for i, v in enumerate(grams.values()):
            if elapsed >= target:
                return grams.most_common(i)
            elapsed += v
    else:
        return grams
