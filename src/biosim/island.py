from .landscape import Lowland, Highland, Desert, Water
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
        for init_pop in list_of_animals:
            coord = init_pop['loc']
            pop = init_pop['pop']
            self.cells[coord].append_population(pop)


    def cycle(self, n=1):
        for _ in range(n):
            for coord in self.cells.keys():
                if self.cells[coord].habitable is True:
                    self.cells[coord].replenish()
                    self.cells[coord].calculate_fitness()
                    self.cells[coord].sort_fitness()
                    self.cells[coord].feed()
                    self.cells[coord].procreate()

                    # coord_now = list(coord)
                    # neighbour_cell = [(coord_now[0] + 1, coord_now[1]), (coord_now[0], coord_now[1] + 1),
                    #                   (coord_now[0] - 1, coord_now[1]), (coord_now[0], coord_now[1] - 1)]

                    neighbour_cell = self.get_neighbours(coord)
                    emigrants = self.cells[coord].emigrants()
                    for animal in emigrants:
                        new_loc = random.choice(neighbour_cell)
                        if self.cells[new_loc].habitable is True:
                            self.cells[new_loc].insert_migrant(animal)
                        else:
                            self.cells[coord].stay_in_cell(animal)

            for coord in self.cells.keys():
                if self.cells[coord].habitable is True:
                    self.cells[coord].add_migrants()
                    self.cells[coord].aging_and_weight_loss()
                    self.cells[coord].deceased()

    @staticmethod
    def get_neighbours(coord_now):
        coord_now = list(coord_now)
        return [(coord_now[0] + 1, coord_now[1]), (coord_now[0], coord_now[1] + 1),
                (coord_now[0] - 1, coord_now[1]), (coord_now[0], coord_now[1] - 1)]
