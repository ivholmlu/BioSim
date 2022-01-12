#%%
from biosim.island import Island
import textwrap
import random

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]


geogr = """\
           WWWWW
           WLLLW
           WWWWW"""
geogr = textwrap.dedent(geogr)



random.seed(89611) # 123, # 132456, # 89611

oy = Island(geogr)
oy.assign()
oy.assign_animals(ini_herbs)
oy.assign_animals(ini_carns)

for _ in range(210):
    for cell in [(2,3), (2,2), (2,4)]:
        oy.cells[cell].replenish()
        oy.cells[cell].init_fitness()
        oy.cells[cell].sort_fitness()
        oy.cells[cell].feed()
        oy.cells[cell].procreate()
        oy.migrant_move()
        oy.cells[cell].add_migrants()
        oy.cells[cell].aging()
        oy.cells[cell].weight_cut()
        oy.cells[cell].deceased()
        oy.cells[(2,2)].add_migrants()
        oy.cells[(2,3)].add_migrants()
        oy.cells[(2, 4)].add_migrants()

#%%
from biosim.island import Island
import textwrap
import random

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]

geogr = """\
           WWWW
           WLLW
           WWWW"""

random.seed(123)

geogr = textwrap.dedent(geogr)

oy = Island(geogr)
oy.assign()
oy.assign_animals(ini_herbs)
oy.assign_animals(ini_carns)


oy.cells[(2, 2)].init_fitness()
oy.cells[(2, 2)].sort_fitness()

oy.migrant_move()
d = len(oy.cells[(2, 2)].herbivores)
e = len(oy.cells[(2, 2)].carnivores)
print(d, e)
oy.cells[(2, 3)].add_migrants()

# %%












