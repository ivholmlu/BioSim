from .animals import Herbivores


class Lowland:  # senere Lowland(Landscape):
    def __init__(self, list_animals=None, f_max=300):  # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.f_max = f_max
        self.list_animals = list_animals
        self.current_fodder = self.f_max
        self.population = None
        self.babies = None

    def add_population(self):
        pop = self.list_animals[0]['pop']
        self.population = [Herbivores(animal) for animal in pop]

    def init_fitness(self):
        fitness0 = [animal.fitness_flux() for animal in self.population]

    def sort_fitness(self):
        self.population.sort(key=lambda animal: animal.fitness, reverse=True)

    def feed(self):  # fordeler mat, mater faktisk dyrene.
        for animal in self.population:
            if self.current_fodder >= animal.param['F']:
                animal.weight_gain(animal.param['F'])
                self.current_fodder -= animal.param['F']

            elif self.current_fodder < animal.param['F']:
                animal.weight_gain(self.current_fodder)
                self.current_fodder -= self.current_fodder

            elif self.current_fodder == 0:
                break

    def procreate(self):
        num_pop = len(self.population)
        self.babies = [baby for parent in self.population if (baby := parent.birth(num_pop))]
        self.population += self.babies

    def aging(self):
        for animal in self.population:
            animal.ages()

    def weight_cut(self):
        new_weight = [self.population.weight_loss(animal) for animal in
                      self.population if animal.alive is False]

    def deceased(self):
        for animal in self.population:
            animal.death()
        self.population = [animal for animal in self.population if animal.alive
                           is True]

    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        self.current_fodder = self.f_max