from .landscape import Lowland

class Island():
    def __init__(self, list_of_animals=None):
        self.tiles = Lowland(list_of_animals)

    # Én syklus for ett landområde
    def cycle(self):
        # Kan videre forbedres ved å implementere .sort_fitness() i hver av funksjonene
        self.tiles.init_fitness()
        self.tiles.sort_fitness()
        self.tiles.feed()
        self.tiles.procreate()
        self.tiles.aging()
        self.tiles.weight_cut()
        self.tiles.deceased()
        self.tiles.replenish()

