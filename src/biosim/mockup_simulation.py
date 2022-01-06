from biosim.island import Island
import random

class BioSim:
    def __init__(self, ini_pop=None, seed=123):
        self.ini_pop = ini_pop
        self.seed = seed
        random.seed(self.seed)
        self.island = Island(ini_pop)

    def run(self, runs=1):
        for _ in range(runs):
            self.island.cycle()
        print(self.seed, self.island.tiles.get_population())