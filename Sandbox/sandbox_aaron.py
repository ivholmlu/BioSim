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
        oy.cells[cell].calculate_fitness()
        oy.cells[cell].sort_fitness()
        oy.cells[cell].feed()
        oy.cells[cell].procreate()
        oy.migrant_move()
        oy.cells[cell].add_migrants()
        oy.cells[cell].aging_and_weight_loss()
        oy.cells[cell].deceased()
        oy.cells[(2,2)].add_migrants()
        oy.cells[(2,3)].add_migrants()
        oy.cells[(2, 4)].add_migrants()

oy.assign_animals(ini_carns)

for _ in range(50,301):
    for cell in [(2,3), (2,2), (2,4)]:
        oy.cells[cell].replenish()
        oy.cells[cell].calculate_fitness()
        oy.cells[cell].sort_fitness()
        oy.cells[cell].feed()
        oy.cells[cell].procreate()
        oy.migrant_move()
        oy.cells[cell].add_migrants()
        oy.cells[cell].aging_and_weight_loss()
        oy.cells[cell].deceased()
        oy.cells[(2, 2)].add_migrants()
        oy.cells[(2, 3)].add_migrants()
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
import textwrap
import random

counter = 0

for sim, seed in enumerate(range(8315981, 8315981+100), 1):
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

    lowl = Lowland()
    lowl.append_population(ini_herbs[0]['pop'])

    for i in range(1,51):
        lowl.replenish()
        lowl.calculate_fitness()
        lowl.sort_fitness()
        lowl.feed()
        lowl.procreate()
        lowl.aging_and_weight_loss()
        lowl.deceased()

    lowl.append_population(ini_carns[0]['pop'])

    for i in range(250):
        lowl.replenish()
        lowl.calculate_fitness()
        lowl.sort_fitness()
        lowl.feed()
        lowl.procreate()
        lowl.aging_and_weight_loss()
        lowl.deceased()

    if len(lowl.carnivores) > 0:
        counter += 1
        print(f'Simulation #{sim}. Number of simulations where carnivores lived {counter}.')