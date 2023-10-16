from keyboard import Keyboard
from corpus import get_grams

from time import time


bigrams = get_grams("res/bigrams.txt")
skipgrams = get_grams("res/bigrams.txt")

qwerty = Keyboard(staggered=True)
recurva = Keyboard(["frdpvqjuoy", "sntcb.heai", "zxkgwml-',"])

# print(qwerty.get_fitness(bigrams, skipgrams))
# print(recurva.get_fitness(bigrams, skipgrams))

print(qwerty)

qwerty = Keyboard()

# needed for init
qwerty.get_fitness(bigrams, skipgrams)

fitness = float("inf")

for i in range(1000000):
    qwerty.mutate()

    new_fit = qwerty.get_fitness(bigrams, skipgrams)

    if new_fit < fitness:
        print(qwerty)
        print(new_fit)
        fitness = new_fit
        qwerty.accept()

    else:
        qwerty.reject()
