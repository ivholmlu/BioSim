from biosim.test_simu import BioSim
from biosim.landscape import Lowland
from biosim.island import Island
import textwrap
import random
import matplotlib.pyplot as plt

random.seed(15838511)

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

a = Island(island_map)

ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'g',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]

a.assign_animals(ini_herbs)

#%%
from biosim.test_simu import BioSim
from biosim.landscape import Lowland
from biosim.island import Island
import textwrap
import random
import matplotlib.pyplot as plt
b = Lowland()
ini_herbs = [{'loc': (41, 3),
              'pop': [{'species': 'Humans',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
b.append_population(ini_herbs[0]['pop'])
