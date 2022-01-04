# class Landscape:
    #  pass

import Herbivores

class Lowland:  # senere Lowland(Landscape):
    def __init__(self, f_max=300, list_animals=None): # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.f_max = f_max
        self.list_animals = list_animals
        self.current_fodder = self.f_max
        self.n_animals = len(self.list_animals)

    def avail_fodder(self):  # fordeler mat
        for animal in self.list_animals:
            if self.current_fodder >= animal.param['F']:
                self.current_fodder -= animal.param['F']
                animal.weight_flux(animal.param['F'])

            elif self.current_fodder < animal.param['F']:
                self.current_fodder -= self.current_fodder
                animal.weight_flux(self.current_fodder)

            elif self.current_fodder <= 0:
                break


    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        current_fodder = self.current_fodder
        pass

