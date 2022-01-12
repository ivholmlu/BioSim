"""
Test for landscape class
"""
import pytest
import numpy as np
from biosim.landscape import Lowland, Highland, Desert, Water


def test_lowland_create():
    lowland = Lowland()
    assert lowland.current_fodder == 0  # The current fodder should always be set to 0
    # regardless of the landscape type. Only when .replenish() is
    # called, shall .current_fodder == f_max


n = 50
m = 20


@pytest.mark.parametrize('herbivores, carnivores',
                         [([{'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(n)]}],
                           [{'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20} for _ in range(m)]}])])
class TestPopulation:
    @pytest.fixture(autouse=True)
    def create_lowland(self):
        self.lowland = Lowland()

    @pytest.fixture(autouse=True)
    def create_animals(self, herbivores, carnivores):
        self.herbivores = herbivores
        self.carnivores = carnivores

    @pytest.fixture
    def insert_animals(self):
        self.lowland.append_population(self.herbivores[0]['pop'])
        self.lowland.append_population(self.carnivores[0]['pop'])

    def test_insert_animals(self):
        self.lowland.append_population(self.herbivores[0]['pop'])
        self.lowland.append_population(self.carnivores[0]['pop'])

        assert len(self.lowland.herbivores) == n and len(self.lowland.carnivores) == m

    def test_fitness_calculation(self, insert_animals):
        self.lowland.init_fitness()
        carn_fitness = [True for carnivore in self.lowland.carnivores if carnivore.fitness > 0]
        herb_fitness = [True for herbivore in self.lowland.herbivores if herbivore.fitness > 0]

        assert True in carn_fitness and herb_fitness
