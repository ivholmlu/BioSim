"""
Animal module
"""
import math
import random


class Animals:
    """
    Animal class, used to create animal objects
    """
    param = None
    species = None

    def __init__(self, attr=None):
        """
        Constructor for animal class

        Parameters
        ------
        attr : dict
            Dictionary containing aga and/or weight for an animal
        """
        self.fitness = 0
        self.alive = True
        self.baby = {'age': 0, 'weight': 0.0}

        if attr is not None:
            if not attr['age'] >= 0:
                raise ValueError('Age must be equal or greater than 0.')
            if not attr['weight'] > 0:
                raise ValueError('Weight must strictly be greater than 0')
            else:
                self.age = attr['age']
                self.weight = attr['weight']

    def fitness_flux(self):
        """
        Function to calculate an animals fitness

        Returns
        -------

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
            Number of individuals of the same species within the cell

        Returns
        -------

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
        The animals age attribute increase by 1.

        Returns
        -------

        """
        self.age += 1
        self.fitness_flux()

    def weight_loss(self):
        """
        Calculates weight loss for each year.

        Returns
        -------

        """
        self.weight -= self.weight * self.param['eta']
        self.fitness_flux()

    def death(self):
        """
        Determines whether or not an animal is going to die.

        Returns
        -------

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
        Sets new parameter for animal objects.

        Parameters
        ----------
        new_params: dict
            Dictionary containing new parameters for animal object. Sets parameters
            to either  of the subclasses Carnivores or Herbivores to see valid parameters.

        Returns
        -------

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
                if not new_params['DeltaPhiMax'] > 0:
                    raise ValueError('DeltaPhiMax must be strictly greater than 0.')

            if 'eta' in new_params.keys():
                if not new_params['eta'] <= 1:
                    raise ValueError('eta must be less or equal to 1.')

    @classmethod
    def get_params(cls):
        """
        Returns the current parameters set to the animal in a dictionary.

        Returns
        -------
        dict
            Returns the current parameters set to the animal object.
        """
        return cls.param


class Herbivores(Animals):
    """
    Herbivore subclass with inherited properties from the parent class.
    """
    param = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
             'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.6,
             'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
             'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
             'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': 0.0}


class Carnivores(Animals):
    """
    Carnivore subclass with inherited properties from the parent class.
    """
    eaten = 0
    param = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
             'eta': 0.125, 'a_half': 40.0, 'phi_age': 0.3,
             'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
             'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
             'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}
