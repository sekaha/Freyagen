# so I gotta do:
# locking
# stagger
# groups
# think of an efficient way to store keys, key positions, etc
# swapping that is reversable
# save layout to text file
# load layout from text file
# caching of penalty scores for bigrams, only update required ones, keep old cache to revert back to
from random import random, choices


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

        # precomputing key positions and distances for faster finding
        self.key_positions = {}

        for y, row in enumerate(self.layout):
            for x, key in enumerate(row):
                self.key_positions[key] = (x, y)

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
        self.cols = ["qaz", "ws"]
        self.col_weights = [1 / len(c) for c in self.cols]

        key_count = sum([len(row) for row in self.layout])
        col_key_count = sum([len(c) for c in self.cols])
        self.col_prob = col_key_count / (key_count)

        # JUST DO new cache.get(,old_cache.get())
        self.cache = {}
        self.cur_cache = {}

    def precompute_distances(self):
        # Possible vectors for a keyboard with touch typing:
        for y1 in range(len(self.layout)):
            for y2 in range(len(self.layout)):
                # possible difference between x1 and x2, really only relevant for index fingers
                for x in range(-1, 2):
                    # for a dx of x1-x2
                    dx = x + self.row_offsets[y1] - self.row_offsets[y2]
                    dy = y1 - y2
                    vector = (x, y1, y2)

                    # pythagorean distance between them
                    self.distances[vector] = (dx**2 + dy**2) ** self.dist_bias

    def get_distance(self, gram):
        x1, y1 = self.key_positions[gram[0]]
        x2, y2 = self.key_positions[gram[1]]

        # only instance this vector returns zero is if the two chars don't occur on the same finger
        return self.distances.get((x1 - x2, y1, y2), 0)

    def swap(self):
        if len(self.cols) > 0 and random() < self.col_prob:
            return "column"
            col = choices(self.cols, self.col_weights)[0]
        else:
            return "key"
            # swap in groups
            # swap individual key, check for finger rule

    def accept(self):
        self.cache.update(self.cur_cache)

    def unswap():
        pass


k = make_keyboard_from_file("layouts/qwerty.txt", False)
k1, k2 = k.key_positions["m"], k.key_positions["y"]

data = {}
for i in range(20000):
    swp = k.swap()
    data[swp] = data.get(swp, 0) + 1

print(5 / 30, "=>", data["column"] / data["key"])
