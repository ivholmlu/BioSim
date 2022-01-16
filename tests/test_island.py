"""
Test file to test island module in biosim
"""
import pytest
import textwrap
from biosim.island import Island
from biosim.landscape import Lowland, Highland, Desert, Water
m = 50
n = 20
herb_loc = (2, 2)
carn_loc = (2, 2)

ini_herbs = [{'loc': herb_loc,
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(m)]}]

ini_carns = [{'loc': carn_loc,
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(n)]}]

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
        self.island.assign_animals([{'loc': herb_loc,
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(m)]}])

    def test_assign_animals(self):
        """
        Test if assign animals have been assigned to their respective cell
        """

        assert len(self.island.cells[herb_loc].herbivores) == m

    def test_assign(self):

        assert type(self.island.cells[(2, 2)]) == type(Desert())

    def test_get_animals_per_species(self):

        dict_animals = self.island.get_animals_per_species()
        assert dict_animals['Herbivore'] == m

    def test_get_coord_animals(self):

        coord_animals = self.island.get_coord_animals()
        assert coord_animals[(herb_loc)]['Herbivores'] == m

def test_get_neighbours():
    assert Island.get_neighbours((2, 2)) == [(3, 2), (2, 3), (1, 2), (2, 1)]




