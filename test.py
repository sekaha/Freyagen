from math import log, pi
from random import sample

chars = "qwertyuiopasdfghjkl;zxcvbnm,./"
dup = 0
tot = 0


print([(i, j) for i in range(len(chars)) for j in range(i + 1, len(chars))])

key_count = len(chars)


def get_stopping_time(key_count):
    swap_n = key_count * (key_count - 1) / 2
    euler_mascheroni = 0.577215665

    # expected value
    ev = swap_n * log(swap_n) + euler_mascheroni * swap_n + 0.5
    return int(ev + 1)


print(get_stopping_time(len(chars)))

# for i in range(N):
#     visited = set()
#
#     for _ in range((30 * 29) // 2):
#         combo = "aa"
#
#         while combo[0] == combo[1]:
#             combo = "".join(sorted(sample(chars, 2)))
#
#         tot += 1
#         if combo in visited:
#             dup += 1
#         visited.add(combo)
#
# print(dup / (30 * (30 * 29) // 2))
N = 10000
i = 0
max_j = 0

for _ in range(N):
    visited = set()

    j = 0
    while len(visited) < (len(chars) * (len(chars) - 1)) // 2:
        combo = "aa"
        while combo[0] == combo[1]:
            combo = "".join(sorted(sample(chars, 2)))
        i += 1
        j += 1
        visited.add(combo)
    max_j = max(max_j, j)

print(i / N, max_j)
