from .animals import Herbivores, Carnivores
import itertools
import random

class Lowland:  # senere Lowland(Landscape):
    def __init__(self, list_animals=None, f_max=800):  # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.f_max = f_max
        self.list_animals = list_animals
        self.pop = self.list_animals[0]['pop']
        self.current_fodder = self.f_max
        self.carnivores = []
        self.herbivores = []
        self.babies = None

        # må finne bedre måte å implementere dyrebestanden inn

    def add_population(self):
        for animal in self.pop:
            if animal['species'] == 'Herbivore':
                self.herbivores.append(Herbivores(animal))
            else:
                self.carnivores.append(Carnivores(animal))

        # z = [self.herbivores.append(Herbivores(x)) if x.species == 'Herbivore'
        #        else self.carnivores.append(Carnivores(x)) for x in self.pop]

    def init_fitness(self):
        fitness0 = [animal.fitness_flux() for animal in self.carnivores+self.herbivores]

    def sort_fitness(self):
        self.herbivores.sort(key=lambda animal: animal.fitness, reverse=True)
        self.carnivores.sort(key=lambda animal: animal.fitness, reverse=True)

    def feed(self):  # fordeler mat, mater faktisk dyrene.
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
        self.babies = [baby for parent in self.herbivores if (baby := parent.birth(num_pop_herb))]
        self.herbivores += self.babies
        #Carnivores
        self.babies = [baby for parent in self.carnivores if(baby := parent.birth(num_pop_carn))]
        self.carnivores += self.babies

    def aging(self):
        for animal in self.population:
            animal.ages()

    def weight_cut(self):
        new_weight = [animal.weight_loss() for animal in self.population]

    def deceased(self):
        for animal in self.population:
            animal.death()
        self.population = [animal for animal in self.population if animal.alive
                           is True]

    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        self.current_fodder = self.f_max

    def get_population(self):
        return len(self.population)