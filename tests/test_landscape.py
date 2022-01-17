"""
Test for landscape class
"""
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.animals import Carnivores, Herbivores
import pytest
import numpy as np


def test_create_landscapes():
    lowland = Lowland()
    highland = Highland()
    desert = Desert()
    water = Water()
    assert lowland.current_fodder == 0 and highland.current_fodder == 0\
           and desert.current_fodder == 0 and water.current_fodder == 0  # The current fodder should always be set to 0
    # regardless of the landscape type. Only when .replenish() is
    # called, should .current_fodder == f_max

@pytest.mark.parametrize('f_max', [100, 240, 700])
def test_set_parameters(f_max):
    highland = Highland()
    highland.set_params({'f_max': f_max})
    highland.replenish()
    assert highland.f_max == highland.current_fodder

n = 50
m = 20

@pytest.mark.parametrize('herbivores, carnivores',
                         [([{'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(n)]}],
                           [{'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(m)]}])])
class TestPopulation:
    @pytest.fixture(autouse=True)
    def create_lowland(self):
        self.lowland = Lowland()

    @pytest.fixture
    def create_animals(self, herbivores, carnivores):
        self.herbivores = herbivores
        self.carnivores = carnivores

    @pytest.fixture
    def insert_animals(self, create_animals):
        self.lowland.append_population(self.herbivores[0]['pop'])
        self.lowland.append_population(self.carnivores[0]['pop'])

    @pytest.fixture
    def set_animal_params(self):
        yield

        Carnivores.set_params(Carnivores.param)
        Herbivores.set_params(Herbivores.param)

    def test_insert_animals(self, create_animals, insert_animals):
        """
        Test if the amount of inserted animals are as expected with the fixed value.
        """
        assert len(self.lowland.herbivores) == n and len(self.lowland.carnivores) == m

    def test_fitness_calculation(self, create_animals, insert_animals):
        """
        Test if every animals fitness get calculated after being inserted into the landscape.
        """
        self.lowland.calculate_fitness()
        carn_fitness = [carnivore.fitness for carnivore in self.lowland.carnivores]
        herb_fitness = [herbivore.fitness for herbivore in self.lowland.herbivores]

        assert all(np.array(herb_fitness) > 0) and all(np.array(carn_fitness) > 0)

    def test_animal_extinction(self, mocker, create_animals, insert_animals):
        """
        Tests the certainty of death of every animal in the land by setting a fixed probability.
        """
        mocker.patch('random.random', return_value=0)

        self.lowland.calculate_fitness()
        self.lowland.deceased()

        assert len(self.lowland.herbivores) == 0 and len(self.lowland.carnivores) == 0


    def test_feeding(self, create_animals, insert_animals):
        """
        Tests that fodder available goes down as herbivores starts eating, as well as the total herbivore population
        decreases due to the carnivores eating.
        """
        self.lowland.replenish()
        self.lowland.calculate_fitness()
        self.lowland.sort_fitness()

        fodder0 = self.lowland.current_fodder
        tot_herbivores0 = len(self.lowland.herbivores)

        self.lowland.feed()

        fodder1 = self.lowland.current_fodder
        tot_herbivores1 = len(self.lowland.herbivores)

        assert fodder1 < fodder0 and tot_herbivores1 < tot_herbivores0

    def test_procreation(self, create_animals, insert_animals, mocker):
        """
        Test to assure that all the animals will procreate and the population size increases.
        """
        mocker.patch('random.random', return_value=0)
        self.lowland.replenish()
        self.lowland.calculate_fitness()
        self.lowland.sort_fitness()

        for animal in self.lowland.carnivores+self.lowland.herbivores:
            animal.fitness = 0.999
            animal.weight = 40

        tot_herbivores0 = len(self.lowland.herbivores)
        tot_carnivores0 = len(self.lowland.carnivores)

        self.lowland.procreate()

        tot_herbivores1 = len(self.lowland.herbivores)
        tot_carnivores1 = len(self.lowland.carnivores)

        assert tot_herbivores1 > tot_herbivores0 and tot_carnivores1 > tot_carnivores0

    @pytest.mark.parametrize('set_params', [{'f_max': 450, 'xi': 1.9, 'gamma': 0.3, 'omega': 0.75}])
    def test_set_parameters(self, set_params):
        lowland = Lowland()
        highland = Highland()
        desert = Desert()
        water = Water()




