"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass


"""
import math
import random

class Herbivores:

    herb = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
            'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
            'w-half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
            'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, dict=None):
        self.age = dict['age']
        self.weight = dict['weight']
        self.fitness = 0
        self.alive = True

    def age(self):
        self.age += 1
        return self.age

    def weight_flux(self):
        self.weight += herb['beta'] * herb['F']
        return self.weight

    def weight_loss(self):
        self.weight -= self.weight * herb['eta']

    def fitness_flux(self):
        q_age = 1 / (1 + math.exp(herb['phi'] * (self.age - herb['a_half'])))
        q_weight = 1 / (1 + math.exp(-herb['phi'] * (self.weight - herb['w_half'])))
        self.fitness = q_age * q_weight
        return self.fitness

    def death(self):
        if self.weight == 0:
            self.alive = False

        else:
            p = herb['omega'] * (1 - self.fitness)
            a = random.random()
            if a < p:
                self.alive = False













