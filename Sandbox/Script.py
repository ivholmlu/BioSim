from biosim.animals import Herbivores
from biosim.landscape import Lowland
import random

seed = random.seed(123)

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]
tot_animals = ini_herbs[0]['pop']

nu_herbs = [Herbivores(x) for x in tot_animals] # Liste med herbivore-objekter
L = Lowland(nu_herbs, 378)

# "A simulation"
for _ in range(100):
    # Stage 0 - calculating fitness, sorting by fitness
    [x.fitness_flux() for x in nu_herbs]
    L.sort_fitness()

    # Stage 1 - feeding, weight gain
    L.feed()
    L.sort_fitness()

    # Stage 2 - procreation
    n = len(nu_herbs)
    proc = [x.birth(n) for x in nu_herbs]

    for herbivore in nu_herbs:
        if herbivore.give_birth is True:
            nu_herbs.append(Herbivores(herbivore.baby))
    L.sort_fitness()

    # Stage 3 - Migration (skip for now)

    # Stage 4 - Aging
    [x.aging() for x in nu_herbs]
    L.sort_fitness()

    # Stage 5 - Weight loss
    [x.weight_loss() for x in nu_herbs]
    L.sort_fitness()

    # Stage 6 - Death
    [x.death() for x in nu_herbs]

    for herbivore in nu_herbs:
        if herbivore.alive is False:
            nu_herbs.remove(herbivore)


    L.replenish()

#%%
for i,j in enumerate(nu_herbs, 1):
    print(i, j.age, j.weight, j.fitness)