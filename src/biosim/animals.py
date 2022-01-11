"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass
"""
import math
import random


class Animals:
    param = None

    def __init__(self, attr=None):
        self.species = attr['species']
        self.age = attr['age']
        self.weight = attr['weight']
        self.fitness = 0
        self.alive = True
        self.baby = {'age': 0, 'weight': 0.0, 'species': self.species}
        self.migrant = False

    def fitness_flux(self):
        q_age = 1 / (1 + math.exp(self.param['phi_age'] *
                                  (self.age - self.param['a_half'])))
        q_weight = 1 / (1 + math.exp(-self.param['phi_weight'] *
                                     (self.weight - self.param['w_half'])))
        self.fitness = q_age * q_weight

    def weight_gain(self, gain=0.0):
        self.weight += self.param['beta'] * gain
        self.fitness_flux()

    def birth(self, N):
        phi = self.fitness
        p = min(1, self.param['gamma'] * phi * (N - 1))
        baby = random.gauss(self.param['w_birth'], self.param['sigma_birth'])
        zeta_lim = self.param['zeta'] * (self.param['w_birth'] + self.param['sigma_birth'])

        if baby < zeta_lim < self.weight and random.random() < p:  # La til zeta_lim! DET FIKSER ALT
            self.weight -= baby * self.param['xi']
            if self.weight >= 0:
                self.baby['weight'] = baby
                return type(self)(self.baby)
            else:
                self.weight += baby * self.param['xi']

        self.fitness_flux()

    def migration(self):
        if random.random() < self.fitness * self.param['mu']:
            return True

    def ages(self):
        self.age += 1
        self.fitness_flux()

    def weight_loss(self):
        self.weight -= self.weight * self.param['eta']
        self.fitness_flux()

    def death(self):
        if self.weight <= 0:
            self.alive = False
        else:
            p = self.param['omega'] * (1 - self.fitness)
            if random.random() < p:
                self.alive = False


class Herbivores(Animals):

    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
             'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
             'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
             'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
             'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}


class Carnivores(Animals):
    eaten = 0
    param = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
             'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
             'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
             'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
             'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

# Vi får bekymre oss for dette på et senere tidspunkt
# @classmethod
# def set_params(cls, new_params):
#   for key in new_params.keys():
#      if key not in new_params.keys():
#         raise KeyError('Invalid parameter name: ' + key)
#    else:
#       cls.param[key] = new_params[key]

# return cls.param
