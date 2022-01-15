"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU
from biosim.animals import Carnivores, Herbivores
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.island import Island

from biosim.Histogram import Histogram
import textwrap
import matplotlib.pyplot as plt
import numpy as np


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        self.island_map = island_map
        self.ini_pop = ini_pop
        self.island = Island(island_map)


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
    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == 'Herbivores':
            Herbivores.set_params(params)
        elif species == 'Carnivores':
            Carnivores.set_params(params)
        else:
            raise ValueError('The island only has two species: '
                  'Herbivores and Carnivores')


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
            raise ValueError('Code letter for landscape must be\n'
                  'either W, D, L or H')


    def simulate(self, num_years, island_map):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        island_map = textwrap.dedent(island_map)

        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]


        self.island.assign()
        self.island.assign_animals(self.ini_pop)
        f1 = plt.figure()


        ax1 = f1.add_subplot(2, 3, 1)

        ax1.imshow(map_rgb)
        ax1.set_xticks(range(len(map_rgb[0])))
        ax1.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax1.set_yticks(range(len(map_rgb)))
        ax1.set_yticklabels(range(1, 1 + len(map_rgb)))
        ax1.set_title('Map of Rossumoya')
        ax1.axis('off')

        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax1.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                          edgecolor='none',
                                          facecolor=rgb_value[name[0]]))


        ax2 = f1.add_subplot(2, 3, 3)
        ax2.set_xlim(0, num_years)
        ax2.set_ylim(0, 10000)
        ax2.set_title('Number of each species')
        line = ax2.plot(np.arange(num_years),
                        np.full(num_years, np.nan), 'b-')[0]

        line2 = ax2.plot(np.arange(num_years),
                         np.full(num_years, np.nan), 'r-')[0]

        axt = f1.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
        axt.axis('off')  # turn off coordinate system
        template = 'Count: {:5d}'
        txt = axt.text(0.5, 0.5, template.format(0),
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=axt.transAxes)  # relative coordinates

        #HISTOGRAM
        x3 = f1.add_subplot(5, 3, 13)
        bins_x3 = np.linspace(0, 1, num=20)
        x3.set_title('Fitness')

        x4 = f1.add_subplot(5, 3, 14)
        x4.set_title('Age')
        bins_x4 = np.linspace(0, 60, num=30)

        x5 = f1.add_subplot(5, 3, 15)
        x5.set_title('Weight')

        # Heatmap #1 - Herbivores
        x4 = f1.add_subplot(2, 3, 5)
        heat_map = np.zeros((self.island.rows+1, self.island.columns+1))
        heat_im = x4.imshow(heat_map, interpolation='nearest', vmin=0, vmax=300)
        plt.colorbar(heat_im, ax=x4, orientation='vertical')



        for year in range(0, num_years):
            x3.cla()
            x4.cla()
            x5.cla()
            x5.set_title('Weight')
            x4.set_title('Age')
            x3.set_title('Fitness')
            self.island.cycle()
            tot_animals = self.num_animals
            tot_carnivores = self.num_animals_per_species['Carnivore']
            tot_herbivores = self.num_animals_per_species['Herbivore']

            #Histogram
            x3.hist(self.get_animals_fitness,bins_x3, color='r', histtype='step', density='False')
            x4.hist(self.get_animals_age, bins_x4, color='r', histtype='step', density='False')
            x5.hist(self.get_animals_weight, bins_x4, color='r', histtype='step', density='False')

            #Animal graph
            ydata = line.get_ydata()
            ydata2 = line2.get_ydata()
            ydata[year] = tot_herbivores
            ydata2[year] = tot_carnivores
            line.set_ydata(ydata)
            line2.set_ydata(ydata2)

            #Counter
            txt.set_text(template.format(year))

            animal_coords = self.island.get_coord_animals()
            for coord, n_animals in animal_coords.items():
                x = list(coord)[0]
                y = list(coord)[1]
                heat_map[x, y] = n_animals['Herbivores']
            x4.imshow(heat_map, interpolation='nearest', vmin=0, vmax=300)



            plt.pause(0.001)
            # et eller annet plotting skjer under her

        plt.show()


    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def get_animals_fitness(self):
        return self.island.get_fitness()

    @property
    def get_animals_age(self):
        return self.island.get_age()

    @property
    def get_animals_weight(self):
        return self.island.get_weight()



    @property
    def num_animals(self):
        """Total number of animals on island."""
        ani_dict = self.island.get_animals_per_species()
        return ani_dict['Herbivore'] + ani_dict['Carnivore']

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.get_animals_per_species()

    @property
    def coord_animals(self):
        return self.island.get_coord_animals()

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass