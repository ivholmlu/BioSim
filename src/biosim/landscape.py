from .animals import Herbivores, Carnivores
import itertools
import random

class Landscape:

    def __init__(self, list_animals=None):  # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.f_max = 0
        self.list_animals = list_animals
        self.pop = self.list_animals[0]['pop']
        self.current_fodder = self.f_max
        self.carnivores = []
        self.herbivores = []

    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        self.current_fodder = self.f_max

    def append_population(self, ext_population=None):
        if ext_population is None:
            init_pop = [self.herbivores.append(Herbivores(animal)) if animal['species'] == 'Herbivore'
                        else self.carnivores.append(Carnivores(animal)) for animal in self.pop]
        else:
            nu_pop = ext_population[0]['pop']
            append_pop = [self.herbivores.append(Herbivores(animal)) if animal['species'] == 'Herbivore'
                          else self.carnivores.append(Carnivores(animal)) for animal in nu_pop]

    def init_fitness(self):
        fitness0 = [animal.fitness_flux() for animal in self.carnivores+self.herbivores]

    def sort_fitness(self):
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=True)
        # Vi sorterer kun herbivores ut ifra fitness

    def feed(self):  # Rewrite the feeding method. Perhaps make two separate feeding methods for each type?
        # At least rewrite the carnivore feeding logic.
        for herbivore in self.herbivores:
            if herbivore.species == 'Herbivore':
                if self.current_fodder >= herbivore.param['F']:
                    herbivore.weight_gain(herbivore.param['F'])
                    self.current_fodder -= herbivore.param['F']

                elif self.current_fodder < herbivore.param['F']:
                    herbivore.weight_gain(self.current_fodder)
                    self.current_fodder -= self.current_fodder

                elif self.current_fodder == 0:
                    break
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=False)

        for carnivore in self.carnivores:
            phi_carn = carnivore.fitness
            delta_phi_max = carnivore.param['DeltaPhiMax']

            while carnivore.fed < carnivore.param['F']:
                for herbivore in self.herbivores:
                    phi_herb = herbivore.fitness
                    if 0 < phi_carn - phi_herb < delta_phi_max:
                        p = phi_carn - phi_herb / delta_phi_max
                        if random.random() < p:
                            herbivore.alive = False
                            carnivore.fed += herbivore.weight
                            carnivore.weight_gain(carnivore.fed)
                    elif phi_carn - phi_herb > delta_phi_max:
                        herbivore.alive = False
                        carnivore.fed += herbivore.weight
                        carnivore.weight_gain(carnivore.fed)

            carnivore.weight_gain(carnivore.fed)

    def procreate(self):
        num_pop_herb = len(self.herbivores)
        num_pop_carn = len(self.carnivores)
        #Herbivores
        baby_herb = [baby for parent in self.herbivores if (baby := parent.birth(num_pop_herb))]
        self.herbivores += baby_herb

        #Carnivores
        baby_carn = [baby for parent in self.carnivores if(baby := parent.birth(num_pop_carn))]
        self.carnivores += baby_carn

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
        return len(self.carnivores+self.herbivores)

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

