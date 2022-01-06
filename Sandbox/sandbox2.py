#%%
import random
from biosim.landscape import Lowland
random.seed(123)

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

a = Lowland(ini_herbs, 378)
a.add_population()

for _ in range(50):
    a.init_fitness()
    a.sort_fitness()
    a.feed()
    a.procreate()
    a.aging()
    a.weight_cut()
    a.deceased()
    a.replenish()

print(len(a.population))