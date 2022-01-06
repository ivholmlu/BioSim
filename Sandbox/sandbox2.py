#%%
import random
from biosim.landscape import Lowland
from biosim.island import Island

random.seed(61361137)

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
c = Island(ini_herbs)

for _ in range(200):
    a.cycle()



#%%
n = 0
for i, j in enumerate(a.population, 1):
    print(i, j.fitness)

print(n)

#%%
ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
c = Lowland(ini_herbs)

for _ in range(200):
    c.init_fitness()
    c.sort_fitness()
    c.feed()
    c.procreate()
    c.aging()
    c.weight_cut()
    c.deceased()
    c.replenish()
print(len(c.population))