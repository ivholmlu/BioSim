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
                      for _ in range(50)]}]

ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(20)]}]


geogr = """\
           WWW
           WLW
           WWW"""

geogr = textwrap.dedent(geogr)

oy = Island(geogr)
oy.assign()
carnivore_dead = 0
herbivore_dead = 0

for seed in range(0, 1001):
    oy = Island(geogr)
    oy.assign()

    oy.assign_animals(ini_herbs)
    random.seed(seed)
    for year in range (1, 51):
        for cell in [(2,2)]:
            oy.cells[cell].init_fitness()
            oy.cells[cell].sort_fitness()
            oy.cycle1()
            oy.migrant_move()
            oy.cycle2()
        for cell in [(2, 2)]:
            oy.cells[cell].add_migrants()

        print(year, len(oy.cells[(2,2)].herbivores), len(oy.cells[(2,2)].carnivores),':',
                len(oy.cells[(2,3)].herbivores), len(oy.cells[(2,3)].carnivores))

    oy.assign_animals(ini_carns)
    for year in range (51, 300):
        for cell in [(2,2)]:
            oy.cells[cell].init_fitness()
            oy.cells[cell].sort_fitness()
            oy.cycle1()
            oy.migrant_move()
            oy.cycle2()
        for cell in [(2, 2)]:
            oy.cells[cell].add_migrants()

        print(year, len(oy.cells[(2, 2)].herbivores), len(oy.cells[(2, 2)].carnivores), ':',
              len(oy.cells[(2, 3)].herbivores), len(oy.cells[(2, 3)].carnivores))
    herbivore_alive = len(oy.cells[(2, 2)].herbivores) + len(oy.cells[(2, 3)].herbivores)
    carnivore_alive = len(oy.cells[(2, 3)].carnivores) + len(oy.cells[(2, 2)].carnivores)


    if herbivore_alive == 0:
        herbivore_dead += 1
    if carnivore_alive == 0:
        carnivore_dead += 1

print(herbivore_dead, carnivore_dead)






