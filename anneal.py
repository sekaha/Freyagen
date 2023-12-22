from corpus import get_grams
from keyboard import Keyboard
from math import exp, log
from random import random, uniform, sample, randint

best_fitness = float("inf")
best = None
swaps_n = 0


class Annealer:
    def __init__(self, keyboard, bigrams, skipgrams, trigrams):
        # key board variables
        self.kb = keyboard

        # corpus info used in fitness function
        self.bigrams = bigrams
        self.skipgrams = skipgrams
        self.trigrams = trigrams

        # permutations of the keyboard used for later metrics
        self.key_count = len(self.kb.normal_keys)
        self.combo_list = [
            (self.kb.normal_keys[i], self.kb.normal_keys[j])
            for i in range(self.key_count)
            for j in range(i + 1, self.key_count)
        ]

        # initial acceptance probability
        self.p0 = 0.8

        # calculate stopping time
        self.max_stays = self.get_stopping_time(self.key_count)
        self.t0 = self.get_initial_temp()
        self.t = self.t0
        self.alpha = 0.99

    # Ben-Ameur, Walid. "Computing the initial temperature of simulated annealing." Computational Optimization and Applications 29, no. 3 (2004): 369-385
    # t0 = STD Deviation of costs
    def get_initial_temp(self, k=0):
        self.kb.get_fitness(self.bigrams, self.skipgrams, self.trigrams)
        self.kb.accept()
        std_dev = 0
        combos = self.combo_list

        if k > 0:
            combos = sample(combos, k)

        for (c1, c2) in combos:
            # swap a random set of valid keys
            self.kb.swaps = list(zip(c1, c2))

            for c1, c2 in self.kb.swaps:
                self.kb.swap(c1, c2)

            self.kb.get_fitness(self.bigrams, self.skipgrams, self.trigrams)
            # work towards calculating standard deviation
            std_dev += abs(self.kb.cur_fitness - self.kb.fitness) / len(combos)

            self.kb.reject()

        # the initial temperature that should lead to a p0% chance of making a swap
        return -std_dev / log(self.p0)

    # Calculate a stopping time for the annealing process based on the number of swaps (coupon collector's problem).
    # This is unused, but when constarints are added this may be a necessary addition again
    def get_stopping_time(self, key_count):
        swap_n = key_count * (key_count - 1) / 2
        euler_mascheroni = 0.577215665
        ev = swap_n * log(swap_n) + euler_mascheroni * swap_n + 0.5

        return int(ev) + 1

    # Boltzmann cooling schedule, does not use quenching
    def cool_down(self, k):
        self.t *= self.alpha

    def run(self):
        global best_fitness, best, swaps_n
        k = 0
        stays = 0

        # run until it reaches max stays
        while stays < self.max_stays:
            k += 1

            # check a markov chain of the same length as number of keys
            for _ in range(self.key_count):
                self.kb.mutate()
                swaps_n += 1
                self.kb.get_fitness(self.bigrams, self.skipgrams, self.trigrams)

                # metropolis check
                de = self.kb.cur_fitness - self.kb.fitness
                # print(self.kb.fitness, self.kb.cur_fitness)

                # if de > 0:
                # print("fitness", fitness)
                # print(f"{k} temp", self.t)
                # print("accept", round(exp(-(de) / self.t) * 100, 2))
                if de < 0 or (de > 0 and random() < exp(-(de) / self.t)):
                    self.kb.accept()
                    stays = 0
                else:
                    stays += 1
                    self.kb.reject()

                if self.kb.fitness < best_fitness:
                    best = [[c for c in row] for row in self.kb.layout]
                    print(
                        "new best",
                        round((self.kb.fitness / self.t0) * 100, 2),
                        "%",
                        self.kb.fitness,
                    )
                    print("scissor score:", self.kb.scissor_score)
                    print(self.kb)
                    best_fitness = self.kb.fitness

            # cool down
            self.cool_down(k)


# r1 = "fndpvqjuo."
# r2 = "srtcbyheai"
# r3 = "xzkgwml;',"

# isrtneao

r1 = "ywlfjzudkx"
r2 = "asirghtoen"
r3 = "qpcvb-m,.'"

# r1 = "qwertyuiop"
# r2 = "asdfghjkl;"
# r3 = "zxcvbnm,./"

# r1 = "kwerqyuiop"
# r2 = "tsdfghzal-"
# r3 = "jxcvbnm,.'"

valid = r1 + r2 + r3
bigrams = get_grams("res/bigrams.txt", valid)
skipgrams = get_grams("res/1-skip.txt", valid)
trigrams = get_grams("res/trigrams.txt", valid, 0.98772)
layout = Keyboard([list(r1), list(r2), list(r3)], staggered=True)

i = 0

while True:
    i += 1
    A = Annealer(layout, bigrams, skipgrams, trigrams)
    print(i, "swaps", swaps_n)
    A.run()
