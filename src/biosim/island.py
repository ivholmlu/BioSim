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
        for coord, geogr in zip(self.cells, self.t_geogr):
            if geogr == 'L':
                self.cells[coord] = Lowland()
            elif geogr == 'H':
                self.cells[coord] = Highland()
            elif geogr == 'D':
                self.cells[coord] = Desert()
            else:
                self.cells[coord] = Water()

    def assign_animals(self, list_of_animals=None):
        coord = list_of_animals[0]['loc']
        pop = list_of_animals[0]['pop']
        self.cells[coord].append_population(pop)

    def migrant_move(self):
        for coord in self.cells.keys(): # Creates list over neighbour cells.
            coord = list(coord)
            neighbour_cell = [(coord[0] + 1, coord[1]), (coord[0], coord[1] + 1),
                              (coord[0] - 1, coord[1]), (coord[0], coord[1] - 1)]
            coord = tuple(coord)
            emigrants = self.cells[coord].emigrants()
            for animal in emigrants:
                new_loc = random.choice(neighbour_cell)
                if self.cells[new_loc].habitable is True:
                    self.cells[new_loc].insert_migrant(animal)
                else:
                    self.cells[coord].stay(animal)

    # Én syklus for ett landområde
    def cycle1(self, n=1):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene

        for coord in self.cells.keys():
            current_cell = self.cells[coord]
            current_cell.replenish()
            current_cell.init_fitness()
            current_cell.sort_fitness()
            current_cell.feed()
            current_cell.procreate()
            current_cell.migrant_move()
            current_cell.aging()
            current_cell.weight_cut()
            current_cell.deceased()


