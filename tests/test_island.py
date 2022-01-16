"""
Test file to test island module in biosim
"""
import pytest
import textwrap
from biosim.island import Island
from biosim.landscape import Lowland, Highland, Desert, Water
amount_herbivores = 50
amount_carnivores = 20
loc = (2, 2)

ini_herbs = [{'loc': loc,
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(amount_herbivores)]}]

ini_carns = [{'loc': loc,
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(amount_carnivores)]}]

Island1 = """\
           WWWWW
           WLLLW
           WLLLW
           WLLLW 
           WWWWW"""
Island1 = textwrap.dedent(Island1)

Island2 = """\
           WWWWW
           WDHVW
           WWWWW"""
Island2 = textwrap.dedent(Island2)

Island3 = """\
           WWW
           WDW
           WWW"""
Island3 = textwrap.dedent(Island3)


class Test_island_creation:
    #No animals can be assigned to a cell with water object
    @pytest.fixture(autouse = True)
    def create_island(self):
        """
        Create an island to be used in Test_island_creation Test class
        """
        self.island = Island(Island2)
        self.island.assign()
        self.island.assign_animals(ini_herbs)

    def test_assign_animals(self):
        """
        Test if assign animals have been assigned to their respective cell and correct
        amount is assigned
        """

        assert len(self.island.cells[loc].herbivores) == amount_herbivores

    def test_assign(self):

        assert type(self.island.cells[(2, 2)]) == type(Desert())

    def test_get_animals_per_species(self):

        dict_animals = self.island.get_animals_per_species()
        assert dict_animals['Herbivore'] == amount_herbivores

    def test_get_coord_animals(self):

        coord_animals = self.island.get_coord_animals()
        assert coord_animals[(loc)]['Herbivores'] == amount_herbivores

def test_get_neighbours():
    assert Island.get_neighbours((2, 2)) == [(3, 2), (2, 3), (1, 2), (2, 1)]




