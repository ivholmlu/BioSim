from .landscape import Lowland, Highland, Desert, Water
import textwrap
import itertools

class Island():
    def __init__(self, geogr=None):
        self.geogr = geogr.replace('\n', '')
        length = int(len(self.geogr)**0.5)
        self.cells = {(x, y): None for x in range(1, length + 1) for y in range(1, length + 1)}

    def assign(self):
        for cell, geogr in zip(self.cells, self.geogr):
            if geogr is 'L':
                self.cells[cell] = Lowland()
            elif geogr is 'H':
                self.cells[cell] = Highland()
            elif geogr is 'D':
                self.cells[cell] = Desert()
            else:
                self.cells[cell] = Water()

    def assign_animal(self, list_of_animals=None):
        coord = list_of_animals[0]['loc']
        pop = list_of_animals[0]['pop']
        self.cells[coord].append_population(pop)

    # Én syklus for ett landområde
    def cycle(self):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene
        self.cells.replenish()
        self.cells.init_fitness()
        self.cells.sort_fitness()
        self.cells.feed()
        self.cells.procreate()
        self.cells.aging()
        self.cells.weight_cut()
        self.cells.deceased()


