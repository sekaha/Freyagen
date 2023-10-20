from corpus import get_grams
from keyboard import Keyboard
from math import exp, log
from random import random, uniform, sample


class Annealer:
    def __init__(self, keyboard, bigrams, skipgrams):
        # key board variables
        self.kb = keyboard
        self.best_fitness = float("inf")
        self.best = None

        # corpus info used in fitness function
        self.bigrams = bigrams
        self.skipgrams = skipgrams

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
        self.kb.get_fitness(self.bigrams, self.skipgrams)
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

            self.kb.get_fitness(self.bigrams, self.skipgrams)
            # work towards calculating standard deviation
            std_dev += abs(self.kb.cur_fitness - self.kb.fitness) / len(combos)

            self.kb.reject()
            # self.kb.accept()

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
        k = 0
        stays = 0

        # run until it reaches max stays
        while stays < self.max_stays:
            k += 1

            # check a markov chain of the same length as number of keys
            for _ in range(self.key_count):
                self.kb.mutate()
                self.kb.get_fitness(self.bigrams, self.skipgrams)

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

            # cool down
            self.cool_down(k)


valid = "yclmkzfu,;" + "isrtgpneao" + "qvwdjbh/.x"

bigrams = get_grams("res/bigrams.txt", valid)
skipgrams = get_grams("res/1-skip.txt", valid)
layout = Keyboard(staggered=True)

A = Annealer(layout, bigrams, skipgrams)
A.run()
