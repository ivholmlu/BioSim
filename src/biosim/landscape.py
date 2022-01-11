from .animals import Herbivores, Carnivores
import itertools
import random


class Landscape:
    def replenish(self):
        self.current_fodder = self.f_max

    def __init__(self):  # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.current_fodder = self.f_max
        self.carnivores = []
        self.herbivores = []

    f_max = 0

    def append_immigrant(self, animal):
        if animal.species == 'Herbivore':
            self.herbivores.append(animal)
        elif animal.species == 'Carnivore':
            self.carnivores.append(animal)

    def append_population(self, ext_population=None):
        init_pop = [self.herbivores.append(Herbivores(animal)) if animal['species'] == 'Herbivore'
                    else self.carnivores.append(Carnivores(animal)) for animal in ext_population]

    def init_fitness(self):
        fitness0 = [animal.fitness_flux() for animal in self.carnivores + self.herbivores]

    def sort_fitness(self):
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=True)
        # Vi sorterer kun herbivores ut ifra fitness

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
            attempts = 0

            for i, herbivore in enumerate(self.herbivores, 1):
                attempts = i
                if 0 < carnivore.fitness - herbivore.fitness < delta_phi_max:
                    if random.random() < ((carnivore.fitness - herbivore.fitness) / delta_phi_max):
                        herbivore.alive = False
                        carnivore.eaten += herbivore.weight

                if carnivore.eaten < carnivore.param['F'] or attempts < len(self.herbivores):
                    continue
                else:
                    if carnivore.eaten >= carnivore.param['F']:
                        carnivore.weight_gain(carnivore.param['F'])
                    else:
                        carnivore.weight_gain(carnivore.eaten)
                    break

            carnivore.eaten = 0

    def procreate(self):
        num_pop_herb = len(self.herbivores)
        num_pop_carn = len(self.carnivores)
        # Herbivores
        baby_herb = [baby for parent in self.herbivores if (baby := parent.birth(num_pop_herb))]
        self.herbivores += baby_herb

        # Carnivores
        baby_carn = [baby for parent in self.carnivores if (baby := parent.birth(num_pop_carn))]
        self.carnivores += baby_carn

    def emigrant(self):
        for animal in self.herbivores + self.carnivores:
            animal.migration()
        emigrants = [animal for animal in self.herbivores + self.carnivores if animal.migration
                     is True]
        return emigrants

    def aging(self):
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.ages()

    def weight_cut(self):
        new_weight = [animal.weight_loss() for animal in itertools.chain(self.carnivores, self.herbivores)]

    def deceased(self):
        for animal in itertools.chain(self.carnivores, self.herbivores):
            animal.death()
        self.carnivores = [carnivore for carnivore in self.carnivores if carnivore.alive
                           is True]
        self.herbivores = [herbivore for herbivore in self.herbivores if herbivore.alive
                           is True]

    def get_population(self):
        return len(self.carnivores + self.herbivores)


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
