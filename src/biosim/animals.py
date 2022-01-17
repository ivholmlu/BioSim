"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass
"""
import math
import random


class Animals:
    param = None
    species = None

    def __init__(self, attr=None):
        """
        Constructor for animal class

        Parameters
        ------
        attr : dict
            Dictionary containig aga and/or weight for an animal
        """
        self.fitness = 0
        self.alive = True
        self.baby = {'age': 0, 'weight': 0.0, 'species': self.species}

        if attr is not None:
            self.age = attr['age']
            self.weight = attr['weight']

    def fitness_flux(self):
        """
        Function to calculate an animals fitness

        Returns
        -------
        None
        """
        q_age = 1 / (1 + math.exp(self.param['phi_age'] *
                                  (self.age - self.param['a_half'])))
        q_weight = 1 / (1 + math.exp(-self.param['phi_weight'] *
                                     (self.weight - self.param['w_half'])))
        self.fitness = q_age * q_weight

    def weight_gain(self, gain=0.0):
        """
        Calculates the weight gained from food

        Returns
        -------
        None
        """
        self.weight += self.param['beta'] * gain
        self.fitness_flux()

    def birth(self, n=0):
        """
        Calculates the probability for giving birth and add a weight
        to the baby attribute if a birth is given.

        Parameters
        ----------
        n : int
            Number of individuals of the same species within the same cell

        Returns
        -------
        None
        """
        phi = self.fitness
        p = min(1, self.param['gamma'] * phi * (n - 1))
        baby = random.gauss(self.param['w_birth'], self.param['sigma_birth'])
        zeta_lim = self.param['zeta'] * (self.param['w_birth'] + self.param['sigma_birth'])

        if baby < zeta_lim < self.weight and random.random() < p:
            self.weight -= baby * self.param['xi']
            if self.weight >= 0:
                self.baby['weight'] = baby
                return type(self)(self.baby)
            else:
                self.weight += baby * self.param['xi']

        self.fitness_flux()

    def migration(self):
        """
        Checks if the animal will migrate or not

        Returns
        -------
        bool
            Decides if the animals migrate or stay in the cell
        """


        if random.random() < self.fitness * self.param['mu']:
            return True

    def ages(self):
        """
        The animals age attribute increase by 1

        Returns
        -------
        None
        """
        self.age += 1
        self.fitness_flux()

    def weight_loss(self):
        """
        Calculates weight loss for each year

        Returns
        -------
        None
        """
        self.weight -= self.weight * self.param['eta']
        self.fitness_flux()

    def death(self):
        """
        Calculates if an animal dies or not during the year

        Returns
        -------
        None
        """
        if self.alive is True:
            if self.weight <= 0:
                self.alive = False
            else:
                p = self.param['omega'] * (1 - self.fitness)
                if random.random() < p:
                    self.alive = False

    @classmethod
    def set_params(cls, new_params):
        """
        Set new parameter for animal objects

        Parameters
        ----------
        new_param: dict
            Dictionary containing new parameters for animal object

        Returns
        -------
        None
        """
        pos_params = [key for key in cls.param.keys() if key != 'DeltaPhiMax']
        for key in new_params.keys():
            if key not in cls.param.keys():
                raise ValueError(f'{key} is an invalid parameter.')

            if key in pos_params:
                if not 0 <= new_params[key]:
                    raise ValueError(f'{key} greater than or equal to 0.')
                cls.param[key] = new_params[key]

            if 'DeltaPhiMax' in new_params.keys():
                if type(cls) is Carnivores:
                    if not new_params['DeltaPhiMax'] > 0:
                        raise ValueError('DeltaPhiMax must be strictly greater than 0.')

            if 'eta' in new_params.keys():
                if not new_params['eta'] <= 1:
                    raise ValueError('eta must be less or equal to 1.')

    @classmethod
    def get_params(cls):
        """
        Returns the animal parameters in a dictionary

        Returns
        -------
        dict
            The current param the animal object has
        """
        return cls.param


class Herbivores(Animals):
    """
    Subclass for animals.
    """
    species = 'Herbivore'
    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
             'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
             'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
             'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
             'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': 0.0}


class Carnivores(Animals):
    """
    Subclass for animals
    """
    eaten = 0
    species = 'Carnivore'
    param = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
             'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
             'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
             'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
             'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}
