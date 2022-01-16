from .animals import Herbivores, Carnivores
import itertools
import random


class Landscape:
    def __init__(self):
        self.current_fodder = 0
        self.carnivores = []
        self.herbivores = []
        self.migrants = []

    f_max = 0
    habitable = None

    def replenish(self):
        self.current_fodder = self.f_max

    def append_population(self, ext_population=None):
        [self.herbivores.append(Herbivores(animal))
         if (animal['species'] or animal.species) == 'Herbivore'
         else self.carnivores.append(Carnivores(animal)) for animal in ext_population]

    def calculate_fitness(self):
        for animal in itertools.chain(self.herbivores, self.carnivores):
            animal.fitness_flux()

    def sort_fitness(self):
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=True)

    def feed(self):
        for herbivore in self.herbivores:
            if self.current_fodder >= herbivore.param['F']:
                herbivore.weight_gain(herbivore.param['F'])
                self.current_fodder -= herbivore.param['F']

            elif self.current_fodder < herbivore.param['F']:
                herbivore.weight_gain(self.current_fodder)
                self.current_fodder -= self.current_fodder

            elif self.current_fodder == 0:
                break

        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=False)
        random.shuffle(self.carnivores)

        for carnivore in self.carnivores:
            delta_phi_max = carnivore.param['DeltaPhiMax']
            carnivore.eaten = 0

            for attempts, herbivore in enumerate(self.herbivores, 1):
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
                elif attempts == len(self.herbivores):
                    break

        self.herbivores = [herbivore for herbivore in self.herbivores if herbivore.alive is True]

    def procreate(self):
        baby_herb = [baby for parent in self.herbivores if (baby := parent.birth(len(self.herbivores)))
                     and parent.alive is True]
        self.herbivores += baby_herb

        baby_carn = [baby for parent in self.carnivores if (baby := parent.birth(len(self.carnivores)))
                     and parent.alive is True]
        self.carnivores += baby_carn

    def emigrants(self):
        emigrants = [animal for animal in itertools.chain(self.herbivores, self.carnivores)
                     if animal.migration() is True]
        self.herbivores = [herbivore for herbivore in self.herbivores
                           if herbivore not in emigrants]
        self.carnivores = [carnivore for carnivore in self.carnivores
                           if carnivore not in emigrants]
        return emigrants

    def insert_migrant(self, animal):
        self.migrants.append(animal)

    def add_migrants(self):
        for migrant in self.migrants:
            if type(migrant) is Carnivores:
                self.carnivores.append(migrant)
            elif type(migrant) is Herbivores:
                self.herbivores.append(migrant)

        self.migrants = []

    def stay_in_cell(self, animal):
        if type(animal) is Herbivores:
            self.herbivores.append(animal)
        elif type(animal) is Carnivores:
            self.carnivores.append(animal)

    def aging_and_weight_loss(self):
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.ages()
            animal.weight_loss()

    def deceased(self):
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.death()
        self.carnivores = [carnivore for carnivore in self.carnivores if carnivore.alive
                           is True]
        self.herbivores = [herbivore for herbivore in self.herbivores if herbivore.alive
                           is True]

    def get_population(self):
        return len(self.herbivores + self.carnivores)

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in ['habitable', 'f_max']:
                raise KeyError(f'{key} is an invalid parameter.')

            if 'habitable' in new_params:
                if not isinstance(new_params['key'], bool):
                    raise ValueError('habitable must be a boolean (True or False).')
                cls.habitable = new_params['habitable']

            if 'f_max' in new_params:
                if not 0 <= new_params['f_max']:
                    raise ValueError('f_max must be greater than or equal to 0.')
                cls.f_max = new_params['f_max']

    @classmethod
    def get_params(cls):
        return {'habitable': cls.habitable, 'f_max': cls.f_max}


class Lowland(Landscape):
    habitable = True
    f_max = 800


class Highland(Landscape):
    habitable = True
    f_max = 300


class Desert(Landscape):
    habitable = True
    f_max = 0


class Water(Landscape):
    habitable = False
