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
                ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";"],
                ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
            ]
        else:
            self.layout = layout

        self.finger = {
            "p": ((0,), (9,)),
            "r": ((1,), (8,)),
            "m": ((2,), (7,)),
            "i": ((3, 4), (5, 6)),
        }

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
        self.distances = {}
        self.precompute_distances()

        # implement as mask for locked
        unlocked = None  # a set
        finger_locked = None  # make a set. this should be easy, just only swap with a valid finger index if it's in this list

        # Adjacency rules
        groups = ["isrtneao"]

        # Columns adjacency handeling and probabilities, a key in a column is just as likely to be chosen as a key not in a column, hopefully producing some balance
        self.keys = "".join(["".join([k for k in row]) for row in self.layout])
        self.cols = [
            "rl",
            "hnb"
            # "rfvtgb",
            # "yhnujm",
        ]  #  "rfvtgb", "ujmyhn",
        self.normal_keys = "".join(
            [k for k in self.keys if k not in "".join(self.cols)]
        )

        self.col_id = {k: 0 for k in self.normal_keys}

        for i, col in enumerate(self.cols):
            for k in col:
                self.col_id[k] = i + 1

        col_key_count = sum([len(c) for c in self.cols])
        self.col_prob = col_key_count / len(self.keys)

        # JUST DO new cache.get(,old_cache.get())
        self.cache = {}
        self.cur_cache = {}
        self.swaps = None  # used for swap history and unswapping

    def __repr__(self):
        # for k in self.keys:
        #     x, y = self.key_pos[k]
        #     self.layout[y][x] = k

        return "\n".join(
            [" ".join(row[:5]) + "  " + " ".join(row[5:]) for row in self.layout]
        )

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
        return self.distances.get((x1 - x2, y1, y2), 0)

    def mutate(self):
        if len(self.cols) > 0 and random() < self.col_prob:
            col1 = choice(self.cols)

            while True:
                finger = choice(choice(list(self.finger.values())))

                # get the keys of another random column
                col2 = [
                    self.layout[y][x]
                    for x in range(finger[0], finger[-1] + 1)
                    for y in range(len(self.layout))
                ]

                # from col2 choose the same amount of unique elements as col1 to swap
                if len(col1) <= len(col2):
                    swaps = sample(col2, len(col1))
                    # if all the elements of
                    if all(self.col_id[swaps[0]] == self.col_id[k] for k in swaps):
                        break

            self.swaps = list(zip(col1, swaps))
        else:
            c1 = choice(self.normal_keys)
            c2 = choice(self.normal_keys)

            self.swaps = list(zip(c1, c2))

        for c1, c2 in self.swaps:
            self.swap(c1, c2)

        # print("mutate", list(self.swaps))
        # print(self)

    def swap(self, c1, c2):
        # change to xy i reckon...
        x1, y1, x2, y2 = *self.key_pos[c1], *self.key_pos[c2]

        self.layout[y1][x1], self.layout[y2][x2] = c2, c1
        self.key_pos[c1], self.key_pos[c2] = self.key_pos[c2], self.key_pos[c1]

    def accept(self):
        self.cache.update(self.cur_cache)

    def reject(self):
        for c1, c2 in self.swaps:
            self.swap(c1, c2)

        # print("reject", list(self.swaps))
        # print(self)


k = make_keyboard_from_file("layouts/qwerty.txt", False)

s = time()

for i in range(1000000):
    k.mutate()
    k.reject()

print(round((time() - s), 5), "s")
print(k)
