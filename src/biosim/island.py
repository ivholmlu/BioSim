import numpy as np
from .landscape import Lowland, Highland, Desert, Water
import random

class Island():
    def __init__(self, geogr=None):
        self.geogr = geogr.splitlines()
        self.t_geogr = geogr.replace('\n', '')
        self.rows = len(self.geogr)
        self.columns = len(self.geogr[0])
        self.cells = {(row, column): None for row in range(1, self.rows + 1)
                      for column in range(1, self.columns + 1)}

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
        for ani_list in list_of_animals:
            coord = ani_list['loc']
            pop = ani_list['pop']
            self.cells[coord].append_population(pop)


    def cycle(self):
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

    def get_animals_per_species(self):
        dict_animals = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                dict_animals['Herbivore'] += len(self.cells[cell].herbivores)
                dict_animals['Carnivore'] += len(self.cells[cell].carnivores)
        return dict_animals

    def get_fitness(self):
        list_fitness = []
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                for animal in self.cells[cell].carnivores + self.cells[cell].herbivores:
                    list_fitness.append(round(animal.fitness, 2))
        return list_fitness

    def get_age(self):
        list_age = []
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                for animal in self.cells[cell].carnivores + self.cells[cell].herbivores:
                    list_age.append(animal.age)
        return list_age

    def get_weight(self):
        list_weight = []
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                for animal in self.cells[cell].carnivores + self.cells[cell].herbivores:
                    list_weight.append(animal.weight)
        return list_weight

    def get_coord_animals(self):
        coord_animals = {}
        for coord, land in self.cells.items():
            coord_animals[coord] = {'Herbivores': len(land.herbivores),
                                    'Carnivores': len(land.carnivores)}

        return coord_animals

    @staticmethod
    def get_neighbours(coord_now):
        coord_now = list(coord_now)
        return [(coord_now[0] + 1, coord_now[1]), (coord_now[0], coord_now[1] + 1),
                (coord_now[0] - 1, coord_now[1]), (coord_now[0], coord_now[1] - 1)]

