"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

from biosim.animals import Carnivores, Herbivores
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.island import Island
from biosim.Graphics import Graphics
import matplotlib.pyplot as plt
import numpy as np
import random
import csv
import os


class BioSim:
    def __init__(self, island_map, ini_pop, seed=None,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        if seed is not None:
            random.seed(seed)
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = Island(island_map)
        self.vis_years = vis_years
        self.img_years = img_years
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.hist_specs = hist_specs

        self.heat_map1 = np.zeros((self.island.rows + 1, self.island.columns + 1))
        self.heat_map2 = np.zeros((self.island.rows + 1, self.island.columns + 1))

        self._graphics = Graphics(img_dir, img_base, img_fmt, self.island_map,
                                  self.heat_map1, self.heat_map2)
        self.years = 0
        self.final_year = None
        self.log_data = []
        self.log_filename = log_file


    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dictionary with valid parameter specification for species
        """
        if species == 'Herbivore':
            Herbivores.set_params(params)
        elif species == 'Carnivore':
            Carnivores.set_params(params)
        else:
            raise ValueError('The island only has two species: Herbivores and Carnivores')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == 'W':
            Water.set_params(params)
        elif landscape == 'D':
            Desert.set_params(params)
        elif landscape == 'L':
            Lowland.set_params(params)
        elif landscape == 'H':
            Highland.set_params(params)
        else:
            raise ValueError('Code letter for landscape must be one of the following: W, D, L or H.')

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self.island.assign_animals(self.ini_pop)
        self.final_year = num_years + self.years
        self._graphics.setup(self.final_year, self.vis_years, self.ymax_animals, self.cmax_animals, self.hist_specs)

        if self.img_years is None:
            self.img_years = self.vis_years

        try:
            if self.img_years % self.vis_years != 0:
                raise ValueError('img_years ust be multiple of vis_steps')
        except ZeroDivisionError:
            pass

        while self.years < self.final_year:
            self.island.cycle()
            histogram_dict = self.get_attributes
            total_herbivores = len(histogram_dict['Herbivores']['fitness'])
            total_carnivores = len(histogram_dict['Carnivores']['fitness'])

            if self.vis_years != 0:
                self._graphics.update_line_graph(self.years, total_herbivores, total_carnivores)

            if self.vis_years == 0:
                plt.close()

            if self.vis_years != 0 and self.years % self.vis_years == 0:
                animal_coords = self.island.get_coord_animals()
                for coord, n_animals in animal_coords.items():
                    x = list(coord)[0]
                    y = list(coord)[1]
                    self.heat_map1[x, y] = n_animals['Herbivores']
                    self.heat_map2[x, y] = n_animals['Carnivores']

                self._graphics.update(self.years, self.heat_map1, self.heat_map2, total_herbivores, total_carnivores,
                                      histogram_dict['Herbivores']['fitness'],
                                      histogram_dict['Carnivores']['fitness'],
                                      histogram_dict['Herbivores']['age'],
                                      histogram_dict['Carnivores']['age'],
                                      histogram_dict['Herbivores']['weight'],
                                      histogram_dict['Carnivores']['weight'])
                plt.pause(0.001)

            self.years += 1

            if self.log_filename is not None:
                self.write_log_data(self.log_filename, self.log_data)

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        self.island.assign_animals(population)

    def make_movie(self, img_fmt=None):
        """Create MPEG4 movie from visualization images saved."""
        self._graphics.make_movie(img_fmt)

    @property
    def num_animals(self):
        """Total number of animals on island."""
        ani_dict = self.island.get_animals_per_species()
        return ani_dict['Herbivore'] + ani_dict['Carnivore']

    @staticmethod
    def coord_animals(self):
        return self.island.get_coord_animals()

    @property
    def year(self):
        return self.years

    @property
    def get_attributes(self):
        return self.island.get_attributes()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.get_animals_per_species()

    @staticmethod
    def write_log_data(log_filename, log_data):
        """
        Writes a .csv file containing the input data.

        Parameters
        ----------
        log_filename: str
            Sets the name for the .csv file
        log_data: list
            Takes in a list of nested

        Returns
        -------

        """
        header = ['year', 'herbivore', 'carnivore']
        with open(log_filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(log_data)

