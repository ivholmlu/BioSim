from biosim.Herbivores import Herbivores
# class Landscape:
    #  pass

class Lowland:  # senere Lowland(Landscape):
    def __init__(self, list_animals=None, f_max=300): # vha. set_lanscape_parameters så skal vi få inn f_max.
        self.f_max = f_max
        self.list_animals = list_animals
        self.current_fodder = self.f_max

    def feed(self):  # fordeler mat, mater faktisk dyrene.
        for animal in self.list_animals:
            if self.current_fodder >= animal.param['F']:
                animal.weight_gain(animal.param['F'])
                self.current_fodder -= animal.param['F']

            elif self.current_fodder < animal.param['F']:
                animal.weight_gain(self.current_fodder)
                self.current_fodder -= self.current_fodder

            elif self.current_fodder == 0:
                break


    def replenish(self):  # fyller på mat for hvert år som går, kan være i overklassen.
        self.current_fodder = self.f_max
