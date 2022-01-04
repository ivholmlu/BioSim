# class Landscape:
    #  pass

import Herbivores

class Lowland:  # senere Lowland(Landscape):
    def __init__(self, f_max=300, list_animals=None):
        self.f_max = f_max
        self.list_animals = list_animals
        self.current_fodder = self.f_max
        self.n_animals = len(self.list_animals)

    def avail_fodder(self):  # fordeler mat
        for animal in self.list_animals:
            if self.current_fodder >= animal.herb['F']:
                self.current_fodder -= animal.herb['F']
                animal.weight_flux(animal.herb['F'])

            elif self.current_fodder < animal.herb['F']:
                self.current_fodder -= self.current_fodder
                animal.weight_flux(self.current_fodder)

            else:
                break


    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        current_fodder = self.current_fodder
        pass

