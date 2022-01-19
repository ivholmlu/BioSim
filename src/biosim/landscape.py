"""
Landscape module
"""
from .animals import Herbivores, Carnivores
import itertools
import random


class Landscape:
    """
    Landscape class, used to create landscape objects
    """
    def __init__(self):
        self.current_fodder = 0
        self.carnivores = []
        self.herbivores = []
        self.migrants = []

    f_max = 0
    habitable = None

    def replenish(self):
        """
        Refills landscapes fodder to f_max value
        """
        self.current_fodder = self.f_max

    def append_population(self, ext_population=None):
        """
        Adds a population to the landscape class
        Parameters
        ----------
        ext_population : list
            list of animal objects or dictionaries with animal object parameters
        """
        for animal in ext_population:
            if animal['species'] not in ['Herbivore', 'Carnivore']:
                raise ValueError('The island only contains carnivores and herbivores.')
            if type(animal) is Herbivores or animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivores(animal))
            elif type(animal) is Carnivores or animal['species'] == 'Carnivore':
                self.carnivores.append(Carnivores(animal))

    def calculate_fitness(self):
        """
        Initialise fitness calculation for all animals in landscape object.
        """
        for animal in itertools.chain(self.herbivores, self.carnivores):
            animal.fitness_flux()

    def sort_fitness(self):
        """
        Sort the herbivores after fitness. Highest fitness first

        Returns
        -------
        """
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=True)

    def feed(self):
        """
        Herbivores are fed first until there are no food left.
        Carnivores eat the herbivores starting with the least fit.
        Each carnivore tries to eat each herbivore once
        At the end, the dead herbivores are removed from list of herbivores

        Returns
        -------

        """

        for herbivore in self.herbivores:
            if self.current_fodder != 0:
                herbivore.weight_gain(min(self.current_fodder, herbivore.param['F']))
                self.current_fodder -= min((self.current_fodder, herbivore.param['F']))


        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=False)
        random.shuffle(self.carnivores)

        for carnivore in self.carnivores:
            delta_phi_max = carnivore.param['DeltaPhiMax']
            carnivore.eaten = 0

            for herbivore in self.herbivores:
                p = (carnivore.fitness - herbivore.fitness)/delta_phi_max
                prev_eaten = carnivore.eaten
                if random.random() < p and herbivore.alive is True:
                    herbivore.alive = False
                    carnivore.eaten += herbivore.weight
                    if carnivore.eaten > carnivore.param['F']:
                        carnivore.weight_gain(carnivore.param['F'] - prev_eaten)
                        break
                    else:
                        carnivore.weight_gain(herbivore.weight)


        self.herbivores = [herbivore for herbivore in self.herbivores if herbivore.alive is True]

    def procreate(self):
        """
        Functions that checks if all herbivores and carnivores have given birth or not.
        If a paren has given birth, the baby attribute is added to baby_herb.
        Returns
        -------

        """
        baby_herb = [baby for parent in self.herbivores
                     if (baby := parent.birth(len(self.herbivores))) and parent.alive is True]
        self.herbivores += baby_herb

        baby_carn = [baby for parent in self.carnivores
                     if (baby := parent.birth(len(self.carnivores))) and parent.alive is True]
        self.carnivores += baby_carn

    def emigrants(self):
        """
        Checks with each animal object in landscape if they want to emigrate or not.

        Returns
        -------
        list
            list of animal objects that has emigrated from the Landscape object

        """
        emigrants = [animal for animal in itertools.chain(self.herbivores, self.carnivores)
                     if animal.migration() is True]
        self.herbivores = [herbivore for herbivore in self.herbivores
                           if herbivore not in emigrants]
        self.carnivores = [carnivore for carnivore in self.carnivores
                           if carnivore not in emigrants]
        return emigrants

    def insert_migrant(self, animal):
        """
        Function takes the animal input and appends it to the migrants attribute
        Parameters
        ----------
        animal
            Animal object to append to migrants attribute

        Returns
        -------

        """
        self.migrants.append(animal)

    def add_migrants(self):
        """
        Add animal objects from migrants attribute and delegates them into
        their respective species attribute list
        Returns
        -------

        """
        for migrant in self.migrants:
            if type(migrant) is Carnivores:
                self.carnivores.append(migrant)
            elif type(migrant) is Herbivores:
                self.herbivores.append(migrant)

        self.migrants = []

    def stay_in_cell(self, animal):
        """
        Animal objects that did not migrate are appended back to their
        landscape object.

        Parameters
        ----------
        animal
            animal : animal class object

        Returns
        -------

        """
        if type(animal) is Herbivores:
            self.herbivores.append(animal)
        elif type(animal) is Carnivores:
            self.carnivores.append(animal)

    def aging_and_weight_loss(self):
        """
        Calculates weight loss and ensure aging for all animal objects
        in landscape object.
        Returns
        -------

        """
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.ages()
            animal.weight_loss()

    def deceased(self):
        """
        Run death function on all animal in landscape object.
        Iterate over each animal and only keep those who are alive.
        Returns
        -------

        """
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.death()
        self.carnivores = [carnivore for carnivore in self.carnivores if carnivore.alive
                           is True]
        self.herbivores = [herbivore for herbivore in self.herbivores if herbivore.alive
                           is True]

    def get_population(self):
        """
        Function that returns the amount of animals in landscape object.

        Returns
        -------
        int
            Amount of animals in landscape object.
        """
        return len(self.herbivores + self.carnivores)

    @classmethod
    def set_params(cls, new_params):
        """

        Parameters
        ----------
        new_params : dict
            Dictionary with new parameters to be set for landscape object

        Returns
        -------

        """
        for key in new_params:
            if key not in ['habitable', 'f_max']:
                raise ValueError(f'{key} is an invalid parameter.')

            if 'habitable' in new_params:
                if not isinstance(new_params['habitable'], bool):
                    raise ValueError('habitable must be a boolean (True or False).')
                cls.habitable = new_params['habitable']

            if 'f_max' in new_params:
                if not 0 <= new_params['f_max']:
                    raise ValueError('f_max must be greater than or equal to 0.')
                cls.f_max = new_params['f_max']

    @classmethod
    def get_params(cls):
        """
        Return current parameters for lanscape object
        Returns
        -------
        dict
            Dictionary containing landscape object current parameters
        """
        return {'habitable': cls.habitable, 'f_max': cls.f_max}


class Lowland(Landscape):
    """
    Subclass of Landscape
    """
    habitable = True
    f_max = 800


class Highland(Landscape):
    """
    Subclass of Landscape
    """
    habitable = True
    f_max = 300


class Desert(Landscape):
    """
    Subclass of Landscape
    """
    habitable = True
    f_max = 0


class Water(Landscape):
    """
    Subclass of Landscape
    """
    habitable = False
