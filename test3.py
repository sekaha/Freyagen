from random import randint, shuffle
from time import time

# reservoir sampeling

chars = "qwertyuiopa;sdfghjklzxcvbnm,./"  # "qwertyuiopghzxcvbnm,./"
swaps = [
    (chars[i], chars[j]) for i in range(len(chars)) for j in range(i + 1, len(chars))
]
##################################

choices = list(range(len(swaps)))
s = time()
checks = 0

for _ in range(100000):
    ran_num = randint(0, len(swaps))
    i = 0
    j = randint(i + 1, len(swaps) - 1)

    choices[i], choices[j] = choices[j], choices[i]

    while i < len(swaps) and choices[i] != ran_num:
        if i < len(swaps) - 1:
            j = randint(i + 1, len(swaps) - 1)
            choices[i], choices[j] = choices[j], choices[i]

        i += 1

print(checks)
print(round(time() - s, 2))

##################################
# print(combos)
# choices = list(range(len(combos)))
# j = 0
#
# for _ in range(10000):
#     shuffle(choices)
#     ran_num = randint(0, len(combos))
#     i = 0
#     markov = []
#
#     while i < len(combos) and choices[i] != ran_num:
#         markov.append(choices[i])
#         i += 1
#     print(markov)
#     j += len(markov)
#
# print(j / 10000)
#
