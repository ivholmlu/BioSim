# class Landscape:
    #  pass

class Lowland:  # senere Lowland(Landscape):
    def __init__(self, f_max=300, list_animals=None):
        self.f_max = f_max
        self.list_animals = list_animals
        self.current_fodder = self.f_max
        self.n_animals = len(self.list_animals)

    def avail_fodder(self, n_animals):  # fordeler mat
        for animal in n_animals:
            pass
        pass

    def replenish(self):  # fyller på mat for hvert år som går
        current_fodder = self.current_fodder
        pass

