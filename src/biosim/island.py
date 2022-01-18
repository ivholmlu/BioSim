from .landscape import Lowland, Highland, Desert, Water
import random


class Island:
    def __init__(self, geogr=None):
        """
        Constructor for the island class, containing its different attributes.

        Parameters
        ----------
        geogr : list
            List of strings containing L, W, D, H to specify each cell values
            where each row is seperated by a newline (\n)
        """
        self.geogr = geogr.splitlines()
        self.t_geogr = geogr.replace('\n', '')
        self.rows = len(self.geogr)
        self.columns = len(self.geogr[0])
        self.cells = {(row, column): None for row in range(1, self.rows + 1)
                      for column in range(1, self.columns + 1)}

        self.assign()

    def assign(self):
        """
        Assigns each coordinate a landscape object depending on the geography depicted by geogr
            in the constructor. The method has 3 different if-tests to ensure that a valid map
            geography is being mapped.

        Return
        -------
        None
        """
        for current_row, next_row in zip(self.geogr, self.geogr[1:]):
            if len(next_row) != len(current_row):
                raise ValueError('Inconsistent row length. All rows must be of the same length.')

        for row in self.geogr[1:-1]:
            if self.geogr[0].count('W') != len(self.geogr[0]) or \
                    self.geogr[-1].count('W') != len(self.geogr[-1]):
                raise ValueError('Edges of the island must be water.')

            if row[0] != 'W' or row[-1] != 'W':
                raise ValueError('Edges of the island must be water.')

        for coord, landscape in zip(self.cells, self.t_geogr):
            if landscape == 'L':
                self.cells[coord] = Lowland()
            elif landscape == 'H':
                self.cells[coord] = Highland()
            elif landscape == 'D':
                self.cells[coord] = Desert()
            elif landscape == 'W':
                self.cells[coord] = Water()
            else:
                raise ValueError(f'"{landscape}" is an invalid landscape type.')
        #self.cells = {coord: landscape for coord, landscape in self.cells.items() if landscape != 'W'}

    def assign_animals(self, list_of_animals=None):
        """
        Assigns animals to specific coordinates provided by its input list_of_animals.

        Parameters
        ----------
        list_of_animals : list
            List containing dictionaries with animal objects containing its position of where
                its being assigned.

        Returns
        -------
        None
        """
        for animals in list_of_animals:
            coord = animals['loc']
            if coord not in self.cells.keys():
                raise ValueError('Inserted coordinate does not exist on the map.')

            if self.cells[coord].habitable is True:
                pop = animals['pop']
                self.cells[coord].append_population(pop)
            else:
                raise ValueError(f'Coordinate {coord} is an invalid place to assign animals')

    def cycle(self):
        """
        Function to simulate a cycle on island. Runs through every function in
        chronological order.

        Returns
        -------
        None
        """
        for coord in self.cells.keys():
            if self.cells[coord].habitable is True:
                self.cells[coord].replenish()
                self.cells[coord].calculate_fitness()
                self.cells[coord].sort_fitness()
                self.cells[coord].feed()
                self.cells[coord].procreate()

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
        """
        Iterates through each cell to get the specific amount of each species on the whole island.

        Returns
        -------
        dict
            Dictionary contains the amount of each species on the whole island.
        """
        dict_animals = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                dict_animals['Herbivore'] += len(self.cells[cell].herbivores)
                dict_animals['Carnivore'] += len(self.cells[cell].carnivores)
        return dict_animals

    def get_attributes(self):
        """
        Iterates through each cell to get every animals' attributes.

        Returns
        -------
        dict
            Dictionary contains a dictionary for each species with a list
            for each of their attributes
        """
        dict_attributes = {'Herbivores' : {'age' : [], 'weight' : [], 'fitness' : []},
                           'Carnivores' : {'age' : [], 'weight' : [], 'fitness' : []}}
        for cell in self.cells:
            if self.cells[cell].habitable is True:
                for herb in self.cells[cell].herbivores:
                    dict_attributes['Herbivores']['fitness'].append(herb.fitness)
                    dict_attributes['Herbivores']['weight'].append(herb.weight)
                    dict_attributes['Herbivores']['age'].append(herb.age)

                for carn in self.cells[cell].carnivores:
                    dict_attributes['Carnivores']['fitness'].append(carn.fitness)
                    dict_attributes['Carnivores']['weight'].append(carn.weight)
                    dict_attributes['Carnivores']['age'].append(carn.age)
        return dict_attributes

    def get_coord_animals(self):
        """
        Retrieves the current herbivore and carnivore population in each coordinate on the map.

        Returns
        -------
        dict
            Dictionary containing every coordinate on the map as a key with the value being a
            dictionary of herbivores and carnivores on that specific coordinate.
        """
        coord_animals = {}
        for coord, land in self.cells.items():
            coord_animals[coord] = {'Herbivores': len(land.herbivores),
                                    'Carnivores': len(land.carnivores)}
        return coord_animals

    @staticmethod
    def get_neighbours(coord_now):
        """
        Function to obtain a coordinates' neighbour coordinates

        Parameters
        ----------
        coord_now : tuple
            Tuple containing (row, column) specifying the current coordinate

        Returns
        -------
        list
            Returns a list of the four neighbouring cells as tuples.
        """
        coord_now = list(coord_now)
        return [(coord_now[0] + 1, coord_now[1]), (coord_now[0], coord_now[1] + 1),
                (coord_now[0] - 1, coord_now[1]), (coord_now[0], coord_now[1] - 1)]
