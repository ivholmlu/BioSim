#%%
from biosim.island import Island
import textwrap
import random

geogr = """\
           WWWWWWWWWWWWWWWWWWWWWWWWW
           WHHHHHLLLLWWLLLLLLLWWWLWW
           WHHHHHLLLLWWLLLLLLLWWWLWW
           WHHHHHLLLLWWLLLLLLLWWWLWW
           WWHHLLLLLLLWWLLLLLLLLLLWW
           WWHHLLLLLLLWWLLLLLLLWWLWW
           WWWWWWWWHWWWWLLLLLLLWWLWW
           WHHHHHLLLLWWLLLLLLLWWWLWW
           WHHHHHHHHHWWLLLLLLWWWWLWW
           WHHHHHDDDDDLLLLLLLWWWWLWW
           WHHHHHDDDDDLLLLLLLWWWWLWW
           WHHHHHDDDDDLLLLLLLWWWWLWW
           WHHHHHDDDDDWWLLLLLWWWWLWW
           WHHHHDDDDDDLLLLLWWWWWWLLW
           WWHHHHDDDDDDLWWWWWWWWWLLW
           WWHHHHDDDDDLLLWWWWWWWWLWW
           WHHHHHDDDDDLLLLLLLWWWWLLW
           WHHHHDDDDDDLLLLWWWWWWWLWW
           WWHHHHDDDDDLLLWWWWWWWWLWW
           WWWHHHHLLLLLLLWWWWWWWWLWW
           WWWHHHHHHWWWWWWWWWWWWWLWW
           WWWWWWWWWWWWWWWWWWWWWWWWW"""

geogr = textwrap.dedent(geogr)

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
random.seed(120151)
oy = Island(geogr)
oy.assign()
oy.assign_animals(ini_herbs)

oy.cycle(50)

oy.assign_animals(ini_carns)

oy.cycle(250)

for coord, land in oy.cells.items():
    if land.habitable is True:
        herbivores = len(land.herbivores)
        carnivores = len(land.carnivores)
        print(coord, herbivores, carnivores)