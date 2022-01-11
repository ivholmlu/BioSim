from biosim.animals import Herbivores, Carnivores
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.island import Island
import random
import time
import textwrap



ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1000)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]


geogr = """\
           WWWW
           WLLW
           WWWW"""

geogr = textwrap.dedent(geogr)

oy = Island(geogr)
oy.assign()
oy.assign_animals(ini_herbs)
oy.assign_animals(ini_carns)
for _ in range (1):
    for cell in [(2, 2), (2, 3)]:
        oy.cells[cell].init_fitness()
        oy.cells[cell].sort_fitness()

        oy.migrant_move()
        d = len(oy.cells[cell].herbivores)
        e = len(oy.cells[cell].carnivores)
        print(d, e)
        oy.cells[cell].add_migrants()

        b = len(oy.cells[cell].herbivores)
        c = len(oy.cells[cell].carnivores)
        print(b, c)









#%%
"""
random.seed(123)

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carn = [{'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

lh = Lowland(ini_herbs)
num_years = 100
lh.append_population(ini_herbs)
lh.init_fitness()
for _ in range(10):
    lh.replenish()
    lh.feed()
    lh.procreate()
    lh.aging()
    lh.weight_cut()
    lh.deceased()

lh.append_population(ini_carn)

for x, _  in enumerate(range(10)):
    lh.replenish()
    lh.feed()
    lh.procreate()
    lh.aging()
    lh.weight_cut()
    lh.deceased()
    print(lh.get_population())
    try:
        print(x, lh.herbivores[0].fitness)
        print(x, lh.carnivores[0].fitness)
    except:
        pass


"""
"""
for _ in range(num_years):
    lh.replenish()
    lh.feed()
    lh.procreate()
    lh.weight_cut()
    lh.deceased()

lh.get_population()
"""
