"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass
"""
import math
import random

class animals:

    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
            'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
            'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
            'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
            'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, dict=None):
        self.age = dict['age']
        self.weight = dict['weight']
        self.fitness = 0
        self.alive = True
        self.baby = {'age': 0, 'weight': 0.0}

    def fitness_flux(self, a_half=param['a_half'], w_half=param['w_half'],
                     phi_age=param['phi_age'], phi_weight=param['phi_weight']):
        q_age = 1 / (1 + math.exp(phi_age * (self.age - a_half)))
        q_weight = 1 / (1 + math.exp(-phi_weight * (self.weight - w_half)))
        self.fitness = q_age * q_weight

    def weight_gain(self, gain=0, beta=param['beta']):
        self.weight += beta * gain
        self.fitness_flux()

    def birth(self, N, gamma=param['gamma'], w_birth=param['w_birth'],
              sigma_birth=param['sigma_birth'], xi=param['xi']):
        phi = self.fitness
        p = min(1, gamma * phi * (N - 1))
        baby = random.gauss(w_birth, sigma_birth)

        if self.weight > baby:
            if random.random() < p:
                self.weight -= baby * xi
                if self.weight >= 0:
                    self.baby['weight'] = baby
                    return type(self)(self.baby)
                else:
                    self.weight += baby * xi

        self.fitness_flux()

    def migration(self):
        pass

    def ages(self):
        self.age += 1
        self.fitness_flux()

    def weight_loss(self, eta=param['eta']):
        self.weight -= self.weight * eta
        self.fitness_flux()

    def death(self, omega=param['omega']):
        if self.weight == 0:
            self.alive = False
        else:
            p = omega * (1 - self.fitness)
            if random.random() < p:
                self.alive = False

class Herbivores(animals):

    def __init__(self):

        self.param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                 'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}


class Carnivores(animals):

    def __init__(self):

        self.param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                 'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
                 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}





# Vi får bekymre oss for dette på et senere tidspunkt
#@classmethod
    #def set_params(cls, new_params):
     #   for key in new_params.keys():
      #      if key not in new_params.keys():
       #         raise KeyError('Invalid parameter name: ' + key)
        #    else:
         #       cls.param[key] = new_params[key]

        #return cls.param
