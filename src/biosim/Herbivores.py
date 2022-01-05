"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass


"""
import math
import random

class Herbivores:
    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
            'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
            'w-half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
            'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, dict=None):
        self.age = dict['age']
        self.weight = dict['weight']
        self.fitness = 0
        self.alive = True
        self.give_birth = False
        self.baby = {'age': 0, 'weight': 0}

    def aging(self):
        self.age += 1

    def weight_gain(self, beta=param['beta'], gain=0):
        self.weight += beta * gain

    def weight_loss(self, eta=param['eta']):
        self.weight -= self.weight * eta

    def fitness_flux(self, phi=param['phi'], a_half=param['a_half'], w_half=param['w_half']):
        q_age = 1 / (1 + math.exp(phi * (self.age - a_half)))
        q_weight = 1 / (1 + math.exp(-phi * (self.weight - w_half)))
        self.fitness = q_age * q_weight
        return self.fitness

    def birth(self, N, gamma = param['gamma'], w_birth = param['w_birth'],
              sigma_birth = param['sigma_birth'], zeta = param['zeta']):
        phi = self.fitness
        p = min(1, gamma*phi*(N-1))
        a = random.random()
        baby = random.gauss(w_birth, sigma_birth)

        if self.weight > baby:
            if a < p:
                self.weight -= baby * zeta
                if self.weight > 0:
                    self.give_birth = True
                else:
                    self.weight += baby * zeta

    def death(self, omega=param['omega']):
        if self.weight == 0:
            self.alive = False

        else:
            p = omega * (1 - self.fitness)
            a = random.random() # husk å bytte navn på variabelen
            if a < p:
                self.alive = False
