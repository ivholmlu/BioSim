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
           WDHLW
           WWWWW"""
Island2 = textwrap.dedent(Island2)

Island3 = """\
           WWW
           WDW
           WWW"""
Island3 = textwrap.dedent(Island3)



class Test_island_cycle_and_creation:

    @pytest.fixture(autouse=True)
    def create_island(self):
        """
        Create an island to be used in Test_island_cycle_and_creation Test class
        """
        self.island = Island(Island2)
        self.island.assign()

    def test_island_cycle_call(self, mocker):
        """
        Test if aging in island cycle runs for excpected amount of time
        """

        num_years = 10
        mocker.spy(self.island, "cycle")
        for _ in range(num_years):
            self.island.cycle()

        assert self.island.cycle.call_count == num_years

    def test_assign_animals(self):
        """
        Test if assign animals have been assigned to their respective cell and correct
        amount is assigned
        """
        self.island.assign_animals(ini_herbs)
        assert len(self.island.cells[loc].herbivores) == amount_herbivores

    def test_assign(self):
        """
        Test assign function. Checks if island.assign in create_map has
        assigned loc = (2,2) to its correct object.
        """

        assert type(self.island.cells[(2, 2)]) == type(Desert())

    def test_get_animals_per_species(self):
        """
        Test that get_animals_per_species dict has the right amount of herbivores
        """
        self.island.assign_animals(ini_herbs)
        dict_animals = self.island.get_animals_per_species()
        assert dict_animals['Herbivore'] == amount_herbivores

    def test_get_coord_animals(self):
    """

    """
        self.island.assign_animals(ini_herbs)
        coord_animals = self.island.get_coord_animals()
        assert coord_animals[(2,2)]['Herbivores'] == amount_herbivores

    def test_get_attributes(self):

        self.island.assign_animals(ini_herbs+ini_carns)
        dict_attributes = self.island.get_attributes()
        assert dict_attributes['Herbivores']['age'] == [5 for i in range(amount_herbivores)]
        assert dict_attributes['Carnivores']['age'] == [5 for i in range(amount_carnivores)]
def test_get_neighbours():
    """
    Test if get neighbour function returns the correct coordinates for a
    specific cells neighbour
    """
    assert Island.get_neighbours((2, 2)) == [(3, 2), (2, 3), (1, 2), (2, 1)]

@pytest.mark.parametrize('Invalid_cells', [(-3, 1), (1,1)])
def test_assign_animals_to_invalid_cell(Invalid_cells):
    map = 'WWW\nWLW\nWWW'
    island = Island(map)
    island.assign()
    with pytest.raises(ValueError):
        island.assign_animals([{'loc': Invalid_cells,
                                'pop': [{'species': 'Herbivore',
                                         'age': 5,
                                         'weight': 20}
                                        for _ in range(1000)]}])

def test_no_migration_to_water():
    map = 'WWW\nWLW\nWWW'
    island = Island(map)
    island.assign_animals([{'loc': (2,2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1000)]}])
    island.cycle()
    neighbours = island.get_neighbours((2,2))
    for neighbour in neighbours:
        assert len(island.cells[neighbour].herbivores) == 0

def test_migration(mocker):
    """
    Test if all neighbour cell are migrated to after one cycle. Placing many animals to ensure
    migration
    """
    island = Island(Island1)
    island.assign()
    island.assign_animals([{'loc': (3, 3),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1000)]}]) #Vanskelig å implementere med mocker ettersom
    #cycle er avhengig av flere ledd med random.random()?

    island.cycle()
    neighbour_cells = island.get_neighbours((3, 3))
    for cell in neighbour_cells:
        assert island.cells[cell].get_population() > 0

@pytest.mark.parametrize('landscapes', ['D', 'L', 'H'])
class TestMap:
    def test_map_boundaries_top_bottom(self, landscapes):
        map = f'WWW\nWDW\nWW{landscapes}'
        with pytest.raises(ValueError):
            island = Island(map)

    def test_map_boundaries_sides(self, landscapes):
        map = f'WWW\nWD{landscapes}\nWWW'
        with pytest.raises(ValueError):
            island = Island(map)


def test_map_unequal_lengths():
    map = 'WWW\nWDWW\nWWW'
    with pytest.raises(ValueError):
        island = Island(map)

def test_map_invalid_landscape():
    map = 'WWW\nWXW\nWWW'
    with pytest.raises(ValueError):
        island = Island(map)

def test_right_landscape_in_cell():
    map = 'WWW\nWLW\nWWW'
    island = Island(map)










