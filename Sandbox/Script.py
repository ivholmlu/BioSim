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
    # Stage 0 - initial fitness calculation
    [x.fitness_flux() for x in nu_herbs]
    nu_herbs.sort(key=lambda r: r.fitness, reverse=True)

    # Stage 1 - feeding, weight gain
    L.feed()

    # Stage 2 - procreation
    n = len(nu_herbs)
    proc = [x.birth(n) for x in nu_herbs]

        # Challenge - how are going to add a new baby if it returns True!
        # Suggestion, make born an attribute of Herbivores class,
            # in other words, making it a self-object
    for herbivore in nu_herbs:
        if herbivore.give_birth is True:
            nu_herbs.append(Herbivores(herbivore.baby))

    # Stage 3 - Migration (skip for now)

    # Stage 4 - Aging
    [x.aging() for x in nu_herbs]

    # Stage 5 - Weight loss
    [x.weight_loss() for x in nu_herbs]

    # Stage 6 - fitness calculation (again)
    [x.fitness_flux() for x in nu_herbs]
    nu_herbs.sort(key=lambda r: r.fitness, reverse=True)

    # Stage 7 - Death
    [x.death() for x in nu_herbs]

    for herbivore in nu_herbs:
        if herbivore.alive is False:
            nu_herbs.remove(herbivore)


    L.replenish()
