#%%
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

