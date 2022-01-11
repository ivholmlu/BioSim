from .landscape import Lowland, Highland, Desert, Water
import textwrap
import itertools
import random

class Island():
    def __init__(self, geogr=None):
        self.geogr = geogr.splitlines()
        self.t_geogr = geogr.replace('\n', '')
        x = len(self.geogr)
        y = len(self.geogr[0])
        self.cells = {(row, column): None for row in range(1, x + 1) for column in range(1, y + 1)}

    def assign(self):
        for cell, geogr in zip(self.cells, self.t_geogr):
            if geogr == 'L':
                self.cells[cell] = Lowland()
            elif geogr == 'H':
                self.cells[cell] = Highland()
            elif geogr == 'D':
                self.cells[cell] = Desert()
            else:
                self.cells[cell] = Water()

    def assign_animals(self, list_of_animals=None):
        coord = list_of_animals[0]['loc']
        pop = list_of_animals[0]['pop']
        self.cells[coord].append_population(pop)

    def migrant_move(self):
        for cell in self.cells.keys(): #Creates list over neighbour cells.
            cell = list(cell)
            neighbour_cell = [(cell[0] + 1, cell[1]), (cell[0], cell[1] + 1),
                              (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1)]
            cell = tuple(cell)
            emigrants = self.cells[cell].emigrants()
            for animal in emigrants:
                new_loc = random.choice(neighbour_cell)
                if self.cells[new_loc].habitable is True:
                    self.cells[new_loc].insert_migrant(animal)







    # Én syklus for ett landområde
    def cycle1(self, n=None):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene
        for cell in self.cells.keys():
            current_cell = self.cells[cell]

            current_cell.replenish()
            current_cell.init_fitness()
            current_cell.sort_fitness()
            current_cell.feed()
            current_cell.procreate()
            # current_cell.emigrate()

    def cycle2(self, n=None):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene
        for cell in self.cells.keys():
            current_cell = self.cells[cell]

            # current_cell.migrate()
            current_cell.aging()
            current_cell.weight_cut()
            current_cell.deceased()


