from keyboard import Keyboard
from corpus import get_grams

from time import time


bigrams = get_grams("res/bigrams.txt")
skipgrams = get_grams("res/bigrams.txt")

# qwerty = Keyboard(staggered=True)
recurva = Keyboard(["frdpvqjuoy", "sntcb.heai", "zxkgwml-',"])

# print(qwerty.get_fitness(bigrams, skipgrams))
# print(recurva.get_fitness(bigrams, skipgrams))
qwerty = Keyboard(staggered=True)

# needed for init
qwerty.get_fitness(bigrams, skipgrams)

s = time()
global_fit = float("inf")
t = 0
for _ in range(100000):
    qwerty = Keyboard(["qwjldyu-fp", "astoghenri", "zxcvbkm,.'"], staggered=True)
    qwerty.get_fitness(bigrams, skipgrams)
    fitness = float("inf")

    for i in range(5000):
        t += 1
        qwerty.mutate()

        # print(qwerty)

        new_fit = qwerty.get_fitness(bigrams, skipgrams)

        if new_fit < fitness:
            fitness = new_fit
            qwerty.accept()

        else:
            qwerty.reject()

        if new_fit < global_fit:
            print(
                f"Staggered thread{_}, epoch-{i} in {round(time() - s, 3)}s, ", new_fit
            )
            print(qwerty)
            global_fit = new_fit

print(t)
