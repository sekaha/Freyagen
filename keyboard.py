# so I gotta do:
# locking
# stagger
# groups
# think of an efficient way to store keys, key positions, etc
# swapping that is reversable
# save layout to text file
# load layout from text file
# caching of penalty scores for bigrams, only update required ones, keep old cache to revert back to
from random import random, choice, sample
from time import time


def make_keyboard_from_file(file, staggered=False):
    try:
        with open(file, "r") as f:
            return Keyboard([l.split() for l in f], staggered=staggered)
    except FileNotFoundError as e:
        print("Cannot load file, skill issue, error:", e)


class Keyboard:
    def __init__(self, layout=None, staggered=False):
        # Default to qwerty if layout not specified
        if layout == None:
            self.layout = [
                ["q", "w", "e", "r", "t", "b", "u", "i", "o", "p"],
                ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
                ["z", "x", "c", "v", "y", "n", "m", ",", ".", "/"],
            ]
        else:
            self.layout = [list(row) for row in layout]

        self.finger = [((0,), (9,)), ((1,), (8,)), ((2,), (7,)), ((3, 4), (5, 6))]

        # precomputing key positions and distances for faster finding
        self.key_pos = {}

        for y, row in enumerate(self.layout):
            for x, key in enumerate(row):
                self.key_pos[key] = (x, y)

        # O(1) dict retrieval of precomputed distances for our keyboard layout based on dx dy
        if staggered:
            self.row_offsets = [-0.25, 0, 0.5]
        else:
            self.row_offsets = [0, 0, 0]

        # an oxey constant cuz i love oxey, bestie <3
        self.dist_bias = 0.65
        self.lateral_penalty = 0.26
        self.distances = {}
        self.precompute_distances()

        # implement as mask for locked
        finger_locked = None  # make a set. this should be easy, just only swap with a valid finger index if it's in this list

        # Columns adjacency handeling and probabilities, a key in a column is just as likely to be chosen as a key not in a column, hopefully producing some balance
        self.locked = set()
        self.keys = sorted("".join(["".join([k for k in row]) for row in self.layout]))

        # Adjacency rules
        groups = [""]  # ["isrtneao"]
        self.group_id = {
            c: i if c in g else -1 for i, g in enumerate(groups) for c in self.keys
        }

        self.cols = []  # "qaz", "rl", "hnb"]
        self.normal_keys = "".join(
            [
                k
                for k in self.keys
                if k not in "".join(self.cols) and k not in self.locked
            ]
        )

        self.col_id = {k: -1 for k in self.normal_keys}

        for i, col in enumerate(self.cols):
            for k in col:
                self.col_id[k] = i

        col_key_count = sum([len(c) for c in self.cols])
        self.col_prob = col_key_count / len(self.keys)

        # JUST DO new cache.get(,old_cache.get())
        self.cache = {}
        self.cur_cache = {}
        self.swaps = None  # used for swap history and unswapping

        self.fitness = 0
        self.cur_fitness = 0
        self.sfb, self.sfs = 0, 0
        self.bg_count, self.sg_count = 0, 0

    def __repr__(self):
        return "\n".join(
            [" ".join(row[:5]) + "  " + " ".join(row[5:]) for row in self.layout]
        )

    # this needs to be fixed, because it's not technically right
    def get_fitness(self, bigrams, skipgrams, skipgram_pen=0.1):
        """
        bigrams/skipgrams: 2d array of string "bigram" and int frequency
        """
        # print(bigrams, skipgrams)
        self.cur_fitness = self.fitness

        # determine an initial fitness to be cached
        if self.swaps == None:
            self.sfb, self.sfs, self.bg_count, self.sg_count = 0, 0, 0, 0
            for gram in bigrams:
                dist = self.get_distance(gram)
                self.cache[gram] = dist

                # add a penalty for the gram finger distance times the frequency of the gram
                self.cur_fitness += dist * bigrams[gram]
                self.cur_fitness += dist * skipgrams[gram] * skipgram_pen

            self.fitness = self.cur_fitness
        else:
            # flatten swaps list for columns
            new_chars = [c for subset in self.swaps for c in subset]
            new_grams = set(
                "".join(sorted(c + s)) for s in new_chars for c in self.keys if s != c
            )

            for gram in new_grams:
                dist = self.get_distance(gram)
                self.cur_cache[gram] = dist

                # Only add on the difference between the old gram penalty and the new gram penalty and multiply by frequency
                dist_diff = dist - self.cache[gram]
                self.cur_fitness += dist_diff * bigrams[gram]
                self.cur_fitness += dist_diff * skipgrams[gram] * skipgram_pen

        return self.cur_fitness

    def precompute_distances(self):
        # Iterate through possible vectors for a keyboard with touch typing and calculate distances
        for y1 in range(len(self.layout)):
            for y2 in range(len(self.layout)):
                # possible difference between x1 and x2, really only relevant for index fingers
                for x in range(-1, 2):
                    # for a dx of x1-x2
                    dx = x + self.row_offsets[y1] - self.row_offsets[y2]
                    dy = y1 - y2

                    # pythagorean distance between keys
                    self.distances[(x, y1, y2)] = (dx**2 + dy**2) ** self.dist_bias

    def get_distance(self, gram):
        x1, y1 = self.key_pos[gram[0]]
        x2, y2 = self.key_pos[gram[1]]

        # only instance this vector returns zero is if the two chars don't occur on the same finger
        left_indexed = x1 in (3, 4) and x2 in (3, 4)
        right_indexed = x1 in (5, 6) and x2 in (5, 6)

        if x1 == x2 or left_indexed or right_indexed:
            return self.distances.get((x1 - x2, y1, y2), 0)

        # here I could check if the distance is greater than 4 (euclideans 2)... and apply it with scissor penalty

        return 0

    def mutate(self):
        # Column mutation
        if len(self.cols) > 0 and random() < self.col_prob:
            col1 = choice((self.cols))

            while True:
                finger = choice(choice(self.finger))

                # get the keys of another random column
                col2 = [
                    self.layout[y][x]
                    for x in range(finger[0], finger[-1] + 1)
                    for y in range(len(self.layout))
                    if self.layout[y][x]
                ]

                # from col2 choose the same amount of unique elements as col1 to swap
                if len(col1) <= len(col2):
                    swaps = sample(col2, len(col1))

                    if all(self.col_id[swaps[0]] == self.col_id[k] for k in swaps):
                        break

            self.swaps = list(zip(col1, swaps))
        # Regular single key swap mutation
        else:
            while True:
                c1 = choice(self.normal_keys)
                c2 = choice(self.normal_keys)

                if self.group_id[c1] == self.group_id[c2]:
                    break

            self.swaps = list(zip(c1, c2))

        for c1, c2 in self.swaps:
            self.swap(c1, c2)

    def swap(self, c1, c2):
        # change to xy i reckon...
        x1, y1, x2, y2 = *self.key_pos[c1], *self.key_pos[c2]

        self.layout[y1][x1], self.layout[y2][x2] = c2, c1
        self.key_pos[c1], self.key_pos[c2] = self.key_pos[c2], self.key_pos[c1]

    def accept(self):
        self.cache.update(self.cur_cache)
        self.cur_cache = {}
        self.fitness = self.cur_fitness

    def reject(self):
        self.cur_cache = {}

        for c1, c2 in self.swaps:
            self.swap(c1, c2)


# k = Keyboard()  # make_keyboard_from_file("layouts/qwerty.txt", False)
#
# s = time()
#
# for i in range(30):
#     k.mutate()
#     print(k, "\n")
#     # k.reject()
#
# print(round((time() - s), 5), "s")
# print(k)
#
