"""
Test file to test island module in biosim
"""
import pytest
import random
from biosim.island import Island
from biosim.landscape import Lowland, Highland, Desert, Water


amount_herbivores = 50
amount_carnivores = 20
loc = (2, 2)
SEED = 21
random.seed(SEED)

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


class TestIslandCycleAndCreation:

    @pytest.fixture(autouse=True)
    def create_island(self):
        """
        Create an island to be used in Test_island_cycle_and_creation Test class
        """
        self.island = Island('WWWWW\nWDHLW\nWWWWW')
        self.island.assign()

    def test_island_cycle_call(self, mocker):
        """
        Test if aging in island cycle runs for excpected amount of time
        """

        num_years = 10
        mocker.spy(self.island, "cycle")
        for _ in range(num_years):
            self.island.cycle()
        # noinspection PyUnresolvedReferences
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
        Test assign function. Checks if island assign function in create_map has
        assigned loc = (2,2) to its correct object.
        """

        assert type(self.island.cells[(2, 2)]) == type(Desert)

    def test_get_animals_per_species(self):
        """
        Test that get_animals_per_species dict has the right amount of herbivores
        """
        self.island.assign_animals(ini_herbs)
        dict_animals = self.island.get_animals_per_species()
        assert dict_animals['Herbivore'] == amount_herbivores

    def test_get_coord_animals(self):
        """
        Test that test_get_coord_animals returns right amount of animals from a cell
        """
        self.island.assign_animals(ini_herbs)
        coord_animals = self.island.get_coord_animals()
        assert coord_animals[(2, 2)]['Herbivores'] == amount_herbivores

    def test_get_attributes(self):
        """
        Test that test_get_attributes returns dictionary containing expected list of attributes
        """

        self.island.assign_animals(ini_herbs+ini_carns)
        dict_attributes = self.island.get_attributes()
        assert dict_attributes['Herbivores']['age'] == [5 for _ in range(amount_herbivores)]
        assert dict_attributes['Carnivores']['age'] == [5 for _ in range(amount_carnivores)]


def test_get_neighbours():
    """
    Test if get neighbour function returns the correct coordinates for a
    specific cells neighbour
    """
    assert Island.get_neighbours((2, 2)) == [(3, 2), (2, 3), (1, 2), (2, 1)]


@pytest.mark.parametrize('invalid_cells', [(-3, 1), (1, 1)])
def test_assign_animals_to_invalid_cell(invalid_cells):
    """
    Test that checks if ValueError are raised if animals are assigned to an inhabitable coord
    or an invalid coordinate
    """
    geogr = 'WWW\nWLW\nWWW'
    island = Island(geogr)
    island.assign()
    with pytest.raises(ValueError):
        island.assign_animals([{'loc': invalid_cells,
                                'pop': [{'species': 'Herbivore',
                                         'age': 5,
                                         'weight': 20}
                                        for _ in range(1000)]}])


def test_no_migration_to_water():
    """
    Test that no animals have migrated to any of the water neighbour cells
    """
    geogr = 'WWW\nWLW\nWWW'
    island = Island(geogr)
    island.assign_animals([{'loc': (2, 2),
                          'pop': [{'species': 'Herbivore',
                                   'age': 5,
                                   'weight': 20}
                                  for _ in range(1000)]}])
    island.cycle()
    neighbours = island.get_neighbours((2, 2))
    for neighbour in neighbours:
        assert len(island.cells[neighbour].herbivores) == 0


def test_migration():
    """
    Test if all neighbour cell are migrated to after one cycle. Placing many animals to ensure
    migration
    """
    island = Island('WWWWW\nWLLLW\nWLLLW\nWLLLW\nWWWWW')
    island.assign()
    island.assign_animals([{'loc': (3, 3),
                            'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(1000)]}])

    island.cycle()
    neighbour_cells = island.get_neighbours((3, 3))
    for cell in neighbour_cells:
        assert island.cells[cell].get_population() > 0


@pytest.mark.parametrize('landscapes', ['D', 'L', 'H'])
class TestMap:
    """
    Class to test creation of the map.
    """
    def test_map_boundaries_top_bottom(self, landscapes):
        """
        Test that invalid boundaries at top or bottom of the map raises ValueError

        Parameters
        ----------
        landscapes : list of strings

        """
        geogr = f'WWW\nWDW\nWW{landscapes}'
        with pytest.raises(ValueError):
            Island(geogr)

    def test_map_boundaries_sides(self, landscapes):
        """
        Test that invalid boundaries at the sides of the map raises ValueError
        Parameters
        ----------
        landscapes : list of strings

        """
        geogr = f'WWW\nWD{landscapes}\nWWW'
        with pytest.raises(ValueError):
            Island(geogr)


def test_map_unequal_rows_or_columns():
    """
    Test if unequal lengths or columns raises ValueError
    """
    geogr = 'WWW\nWDWW\nWWW'
    with pytest.raises(ValueError):
        Island(geogr)


def test_map_invalid_landscape():
    """
    Test if invalid landscape name raises ValueError
    """
    geogr = 'WWW\nWXW\nWWW'
    with pytest.raises(ValueError):
        Island(geogr)


@pytest.mark.parametrize('landscape, symbol', [(Lowland, 'L'), (Desert, 'D'), (Highland, 'H'), (Water, 'W')])
def test_right_landscape_in_cell(landscape, symbol):
    """
    Test that right landscape is assigned to the right cell
    """
    geogr = f'WWW\nW{symbol}W\nWWW'
    island = Island(geogr)

    assert type(island.cells[(2, 2)]) == landscape
