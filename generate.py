from keyboard import Keyboard
from corpus import get_grams

from time import time

# constrain > generate > swap columns > brute force
# probably sfb, sfs, scissors, lsbs and bad redirects get you 90% of the way there at least as far as current scoring algorithms/metrics go

valid = "qwjldyu/fp" + "astoghenri" + "zxcvbkm,.;"
bigrams = get_grams("res/bigrams.txt", valid)
skipgrams = get_grams("res/1-skip.txt", valid)

# qwerty = Keyboard(staggered=True)
recurva = Keyboard(["frdpvqjuoy", "sntcb.heai", "zxkgwml-',"])

# print(qwerty.get_fitness(bigrams, skipgrams))
# print(recurva.get_fitness(bigrams, skipgrams))
qwerty = Keyboard(staggered=True)

s = time()
global_fit = float("inf")
t = 0

for _ in range(100000):
    fitness = float("inf")
    qwerty = Keyboard(["yclmkzfu,;", "isrtgpneao", "qvwdjbh/.x"], staggered=True)

    for j in range(30):
        qwerty.mutate()
    qwerty.swaps = None
    qwerty.get_fitness(bigrams, skipgrams, 0.1)

    for i in range(5000):
        t += 1
        qwerty.mutate()

        new_fit = qwerty.get_fitness(bigrams, skipgrams, 0.1)

        if new_fit < fitness:
            fitness = new_fit
            qwerty.accept()

        else:
            qwerty.reject()

        if new_fit < global_fit:
            print(
                "staggered " + f"thread{_}, epoch-{i} in {round(time() - s, 3)}s, ",
                new_fit,
            )
            qwerty.swaps = None
            qwerty.get_fitness(bigrams, skipgrams, 0.1)
            # print(
            #    f"SFB {(100*qwerty.sfb / qwerty.bg_count) : 0.2f}, SFS {(100*qwerty.sfs / qwerty.sg_count) : 0.2f}"
            # )
            print(qwerty)
            global_fit = new_fit

print(t)
