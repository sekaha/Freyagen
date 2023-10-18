from corpus import get_grams

layout = [
    "'lugdzwh.y",
    "oretpcsnai",
    "qx-bkfvm,j",
]

chars = get_grams("res/characters.txt")

cols = [
    sum([chars[layout[y][x]] for y in range(len(layout))])
    for x in range(len(layout[0]))
]  # sorted(
# key=lambda x: sum(chars[c] for c in x),
# )

total = sum(cols)


print(total)
