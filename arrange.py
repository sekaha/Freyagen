from corpus import get_grams
import re
from random import randint

print(list(range(0, 3, 2)))
print(1 / 0)

layout = """p x y w f  q k h , u
n o i s c  m t r a e
b ' j v z  d g l . -"""

chars = get_grams("res/characters.txt", "".join(layout))

layout_cleaned = [list(row) for row in layout.replace(" ", "").split("\n")]
cols = [c for c in zip(*layout_cleaned)]
left_i = cols[3:5]
right_i = cols[6:8]
cols = cols[0:3] + cols[7:10]

cols.sort(key=lambda x: sum([chars[c] for c in x]))

for x, (a, b) in enumerate(zip(cols[::2], cols[1::2])):
    if randint(0, 1):
        a, b = b, a

    for y in range(3):
        layout_cleaned[y][x] = a[y]
        layout_cleaned[y][-(x + 1)] = b[y]

print("\n".join((["".join(row) for row in layout_cleaned])))


# chars = get_grams("res/characters.txt", "".join(layout))

# sorted_cols = [col for col in zip(*(layout.replace(" ", "").split("\n")[3:4] + layout.replace(" ", "").split("\n")[6:7]))]
# sorted_cols.sort(key=lambda x: chars[x[0]] + chars[x[2]])

# print(sorted_cols)
