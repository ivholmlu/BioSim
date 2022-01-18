"""
Example of making a movie of the simulation, rendering the data of every year simulated.
"""
from biosim.simulation import BioSim
import textwrap

geogr = """\
           WWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHLLLLWWLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLW
           WWHHLLLLLLLWWLLLLLLLW
           WWWWWWWWHWWWWLLLLLLLW
           WHHHHHLLLLWWLLLLLLLWW
           WHHHHHHHHHWWLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHHDDDDDWWLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDDLWWWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WHHHHHDDDDDLLLLLLLWWW
           WHHHHDDDDDDLLLLWWWWWW
           WWHHHHDDDDDLLLWWWWWWW
           WWWHHHHLLLLLLLWWWWWWW
           WWWHHHHHHWWWWWWWWWWWW
           WWWWWWWWWWWWWWWWWWWWW"""

island_map = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

sim = BioSim(island_map, ini_herbs+ini_carns, seed=15838511, vis_years=1, img_dir='./movie')
sim.simulate(51)
sim.add_population(ini_carns)
sim.simulate(51)
sim.make_movie('mp4')






