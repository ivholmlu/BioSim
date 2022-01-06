#%%
from biosim.mockup_simulation import BioSim

ini_herbs = [{'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]


for seed in range(123,126):
    sim = BioSim(ini_herbs, seed=seed)
    sim.run(200)