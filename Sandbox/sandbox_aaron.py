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


for _ in range(50):
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

oy.assign_animals(ini_carns)

for _ in range(50,301):
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

print(oy.cells[(2,2)].get_population())
print(oy.cells[(2, 3)].get_population())
print(oy.cells[(2, 4)].get_population())

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

oy = Island(geogr)
oy.assign()
oy.assign_animals(ini_herbs)


for _ in range(50):
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

oy.assign_animals(ini_carns)

for _ in range(50,210):
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

# %%
from biosim.landscape import Lowland
import random

for seed in range(230, 250):
    random.seed(seed)
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
    a = Lowland()
    a.append_population(ini_herbs[0]['pop'])

    for i in range(50):
        a.replenish()
        a.init_fitness()
        a.sort_fitness()
        a.feed()
        a.procreate()
        a.aging()
        a.weight_cut()
        a.deceased()

    a.append_population(ini_carns[0]['pop'])

    for i in range(51,301):
        a.replenish()
        a.init_fitness()
        a.sort_fitness()
        a.feed()
        a.procreate()
        a.aging()
        a.weight_cut()
        a.deceased()
    print(len(a.herbivores), len(a.carnivores))

