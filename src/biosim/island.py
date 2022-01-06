from .landscape import Lowland

class Island():
    def __init__(self, list_of_animals=None):
        self.island = Lowland(list_of_animals)

    # Én syklus for ett landområde
    def cycle(self):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene
        self.island.init_fitness()
        self.island.sort_fitness()
        self.island.feed()
        self.island.procreate()
        self.island.aging()
        self.island.weight_cut()
        self.island.deceased()
        self.island.replenish()

