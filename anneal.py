from corpus import get_grams
from keyboard import Keyboard
from math import exp, log
from random import random, uniform

# List based simulated annealing algorithm used for a similar problem known as TSA
# This produces decent results
# We use the cooling schedule proposed by the Boltzmann simulated annealing algoirthn p0?
# temperature controlling procedure of LBSA is adaptive according to the topology of solution space of the problem
# The advantage of insensitive parameter is very attractive, allowing LBSA algorithm to be applied in
# diverse problems without much effort on tuning parameters to produce promising results
class Annealer:
    def __init__(self, keyboard, bigrams, skipgrams):
        # initial temp is absolute value of f(y) - f(x) (first mutation ig)
        # keeps a priority queue tempature list -- should probably use a maxheap

        # initial acceptance probability
        self.p0 = 0.1
        self.kb = keyboard
        self.t = 0
        self.temps = []
        self.temps_len = 30
        self.bigrams = bigrams
        self.skipgrams = skipgrams

        self.init_temp_list()

    def get_acceptance_prob(self):
        # replace with heap get
        return exp(-(self.kb.cur_fitness - self.kb.fitness) / max(self.temps))

    def get_temp(self, r):
        self.t = (self.t - (self.kb.cur_fitness - self.kb.fitness)) / log(r)
        self.temps.append(self.t)

    def init_temp_list(self):
        # init keyboard fitness
        self.kb.get_fitness(self.bigrams, self.skipgrams)

        for _ in range(self.temps_len):
            self.kb.mutate()

            new_fit = self.kb.get_fitness(self.bigrams, self.skipgrams)

            if new_fit < self.kb.fitness:
                self.kb.accept()
            else:
                self.kb.reject()

            t = (-abs(new_fit - self.kb.fitness)) / log(self.p0)
            self.temps.append(t)

        # we only maintain the max temp from the initial search bit
        self.temps = [max(self.temps)]

    def run(self):
        K = 100
        M = 100

        for k in range(K):
            # inner loop, make an M length markov chain
            # a process similar to reannealing I suppose? I've seen this a few times
            c = 0
            self.t = 0

            for m in range(M):
                # mutate and accept new layout if it's better or random chance
                self.kb.mutate()

                if self.kb.get_fitness(self.bigrams, self.skipgrams) < self.kb.fitness:
                    # print(self.kb.fitness, "=>", new_fit)
                    # print(self.kb)
                    self.kb.accept()
                else:
                    # [0,1) per the paper
                    r = uniform(0, 1)
                    a = self.get_acceptance_prob()
                    print(a)

                    if r > a:
                        self.get_temp(r)
                        c += 1

                        self.kb.accept()
                    else:
                        self.kb.reject()

            # c is how many times a bad solution is accepted
            # reducing temp based on this helps the problem be more adaptive
            if c > 0:
                self.t /= c
                self.temps.remove(max(self.temps))
                self.temps.append(self.t / c)


valid = "yclmkzfu,;" + "isrtgpneao" + "qvwdjbh/.x"

bigrams = get_grams("res/bigrams.txt", valid)
skipgrams = get_grams("res/1-skip.txt", valid)
layout = Keyboard(["yclmkzfu,;", "isrtgpneao", "qvwdjbh/.x"], staggered=True)

A = Annealer(layout, bigrams, skipgrams)
A.run()
