from biosim.landscape import Lowland, Water
import matplotlib.pyplot as plt
from biosim.island import Island
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
a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]

for i in zip(a, b, c):
    print(i)

geogr = """\
           WWWW
           WLLW
           WWWW"""

geogr = textwrap.dedent(geogr)

oy = Island(geogr)

oy.assign()
oy.assign_animals(ini_herbs)
oy.assign_animals(ini_carns)
oy.migrant_move()




"""
import random
from biosim.landscape import Lowland
import matplotlib.pyplot as plt
random.seed(100)

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

a = Lowland(ini_herbs)
a.add_population()
years = []
years_pop = []
years_babies = []
for _ in range(100):
    a.init_fitness()
    a.sort_fitness()
    a.feed()
    a.procreate()
    a.aging()
    a.weight_cut()
    a.deceased()
    a.replenish()
    years.append(_)
    years_pop.append(len(a.population))
    years_babies.append(len(a.babies))

plt.plot(years, years_pop)
plt.plot(years, years_babies)
plt.title('Amount and birth each year')
plt.xlabel('year')
plt.ylabel('amount')
plt.legend(['weight', 'birth'])
plt.show()
print(len(a.population))

"""