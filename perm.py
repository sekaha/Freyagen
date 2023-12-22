from itertools import permutations
from time import time

keys = "abcdefghijklmnopqrstuvwxz,./;"
swaps = "ab"  # "abcdefghijklmnopqrstuvwxz,./;"

s = time()

red_cache = {
    "".join(p): 0
    for k in swaps
    for i in range(len(keys))
    for j in range(i, len(keys))
    for p in permutations(k + keys[i] + keys[j], 3)
    if p[0] != p[1] and p[1] != p[2]
}

print(len(red_cache))

print((time() - s) * 1000)
