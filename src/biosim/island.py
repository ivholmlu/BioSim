from .landscape import Lowland, Highland, Desert, Water
import textwrap
import itertools
import random

class Island():
    def __init__(self, geogr=None):
        self.geogr = geogr.splitlines()
        self.t_geogr = geogr.replace('\n', '')
        n_rows = len(self.geogr)
        m_columns = len(self.geogr[0])
        self.cells = {(row, column): None for row in range(1, n_rows + 1) for column in range(1, m_columns + 1)}

    def assign(self):
        for coord, landscape in zip(self.cells, self.t_geogr):
            if landscape == 'L':
                self.cells[coord] = Lowland()
            elif landscape == 'H':
                self.cells[coord] = Highland()
            elif landscape == 'D':
                self.cells[coord] = Desert()
            else:
                self.cells[coord] = Water()

    def assign_animals(self, list_of_animals=None):
        coord = list_of_animals[0]['loc']
        pop = list_of_animals[0]['pop']
        self.cells[coord].append_population(pop)

    def migrant_move(self):
        # Idé: Kanskje framfor å gå gjennom keys, heller gå gjennom .items slik at vi får ut både koordinat
        # og landtype!
        for coord, land in self.cells.items(): # Creates list over neighbour cells.
            current_cord = list(coord)
            neighbour_cell = [(current_cord[0] + 1, current_cord[1]), (current_cord[0], current_cord[1] + 1),
                              (current_cord[0] - 1, current_cord[1]), (current_cord[0], current_cord[1] - 1)]
            emigrants = land.emigrants()
            for animal in emigrants:
                new_loc = random.choice(neighbour_cell)
                if self.cells[new_loc].habitable is True:
                    self.cells[new_loc].insert_migrant(animal)
                else:
                    self.cells[coord].stay(animal)

    def cycle(self, n=1):
        for _ in range(n):
            for land in self.cells.values():
                land.replenish()
                land.calculate_fitness()
                land.sort_fitness()
                land.feed()
                land.procreate()
                land.migrant_move()
                land.aging_and_weight_loss()
                land.deceased()

            for land in self.cells.values():
                land.add_migrants()
