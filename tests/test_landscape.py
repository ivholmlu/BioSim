"""
Test for landscape class
"""
from biosim.landscape import Lowland, Highland, Desert, Water
from biosim.animals import Carnivores, Herbivores
import pytest
import numpy as np


def test_create_landscapes():
    """
    A test to check if the different landscapes are created, and to ensure the default value
    of fodder are inherited from the main class, which in this case is 0.
    """
    lowland = Lowland()
    highland = Highland()
    desert = Desert()
    water = Water()
    assert lowland.current_fodder == highland.current_fodder\
           == desert.current_fodder\
           == water.current_fodder == 0


@pytest.mark.parametrize('f_max, habitable', [[100, True], [23, False], [700, True]])
def test_set_parameters(f_max, habitable):
    """
    A test to check if set_params sets the parameters to the assigned landscape.
    """
    highland = Highland()
    highland.set_params({'f_max': f_max, 'habitable': habitable})
    highland.replenish()
    assert highland.f_max == highland.current_fodder and highland.habitable is habitable


@pytest.mark.parametrize('f_max', [-100, -3.21, -0.01])
def test_set_faulty_f_max(f_max):
    """
    A test to check if setting incompatible f_max value raises a ValueError.
    """
    with pytest.raises(ValueError):
        Desert.set_params({'f_max': f_max})


@pytest.mark.parametrize('habitable', ['False', 'True', None])
def test_set_faulty_habitable(habitable):
    """
    A test to check if setting an incompatible habitable value raises a ValueError.
    """
    with pytest.raises(ValueError):
        Highland.set_params({'habitable': habitable})


n = 50
m = 20


@pytest.mark.parametrize('herbivores, carnivores',
                         [([{'pop': [{'species': 'Herbivore',
                                      'age': 5, 'weight': 20} for _ in range(n)]}],
                           [{'pop': [{'species': 'Carnivore',
                                      'age': 7, 'weight': 22} for _ in range(m)]}])])
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

    def test_insert_animals(self, create_animals, insert_animals):
        """
        Test if the amount of inserted animals are as expected with the fixed value.
        """
        assert self.lowland.get_population() == n + m

    def test_fitness_calculation(self, create_animals, insert_animals):
        """
        Test if every animal's fitness get calculated after being inserted into the landscape.
        """
        self.lowland.calculate_fitness()
        carn_fitness = [carnivore.fitness for carnivore in self.lowland.carnivores]
        herb_fitness = [herbivore.fitness for herbivore in self.lowland.herbivores]

        assert all(np.array(herb_fitness) > 0) and all(np.array(carn_fitness) > 0)

    def test_animal_extinction(self, mocker, create_animals, insert_animals):
        """
        Tests the certainty of death of every animal in the land by setting a fixed probability.
        """
        mocker.patch('random.random', return_value=-1)

        self.lowland.calculate_fitness()
        self.lowland.deceased()

        assert len(self.lowland.herbivores) == 0 and len(self.lowland.carnivores) == 0

    def test_feeding(self, create_animals, insert_animals):
        """
        Tests that fodder available goes down as herbivores starts eating, as well as the total
        herbivore population decreases due to the carnivores eating.
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

    def test_age_and_weight_loss(self, create_animals, insert_animals, mocker):
        """
        Test to check if the amount of calls made to the ages and weight_loss is equal to the
        amount of animals in the landscape,
        as well as checking that the age and weight has increased.
        """
        mocker.spy(Carnivores, 'ages')
        mocker.spy(Carnivores, 'weight_loss')

        self.lowland.calculate_fitness()
        carn_weight_pre = [carnivore.weight for carnivore in self.lowland.carnivores]
        carn_age_pre = [carnivore.age for carnivore in self.lowland.carnivores]

        self.lowland.aging_and_weight_loss()

        carn_weight_post = [carnivore.weight for carnivore in self.lowland.carnivores]
        carn_age_post = [carnivore.age for carnivore in self.lowland.carnivores]

        assert all(np.array(carn_weight_post) < np.array(carn_weight_pre)) and \
               all(np.array(carn_age_post) > np.array(carn_age_pre))

        assert Carnivores.ages.call_count == Carnivores.weight_loss.call_count\
               == len(self.lowland.carnivores)

    def test_procreation(self, create_animals, insert_animals, mocker):
        """
        Test to assure that all the animals will procreate and the population size increases.
        """
        mocker.patch('random.random', return_value=0)
        self.lowland.replenish()
        self.lowland.calculate_fitness()
        self.lowland.sort_fitness()

        for animal in self.lowland.carnivores + self.lowland.herbivores:
            animal.fitness = 0.999
            animal.weight = 40

        tot_herbivores0 = len(self.lowland.herbivores)
        tot_carnivores0 = len(self.lowland.carnivores)

        self.lowland.procreate()

        tot_herbivores1 = len(self.lowland.herbivores)
        tot_carnivores1 = len(self.lowland.carnivores)

        assert tot_herbivores1 > tot_herbivores0 and tot_carnivores1 > tot_carnivores0


def test_reject_unrecognizable_animal():
    """
    Test to check if inserting an unspecified type of animal raises a ValueError.
    """
    highland = Highland()
    with pytest.raises(ValueError):
        unrecognizable_animal_type = [{'loc': (2, 7),
                                       'pop': [{'species': 'Omnivore',
                                                'age': 8, 'weight': 35} for _ in range(10)]}]
        highland.append_population(unrecognizable_animal_type[0]['pop'])


@pytest.mark.parametrize('f_max', [2.1, 8.3, 3.9, 9.0])
def test_limited_fodder(f_max):
    """
    Test to check if the fodder available is eaten up, which in these cases which is less than F
    (the desired amount for a herbivore to eat),
    leaving the next herbivore to eat with no food left.
    """
    test_herbivores = [{'loc': (2, 7),
                        'pop': [{'species': 'Herbivore',
                                 'age': 6, 'weight': 25} for _ in range(2)]}]

    Highland.set_params({'f_max': f_max})
    highland = Highland()
    set_f_max = highland.get_params()['f_max']

    highland.append_population(test_herbivores[0]['pop'])

    for herbivore in highland.herbivores:
        assert highland.current_fodder < herbivore.param['F']

    highland.replenish()
    highland.calculate_fitness()

    herbivore1 = highland.herbivores[0]
    herbivore2 = highland.herbivores[1]
    weight_pre_feeding1 = herbivore1.weight
    weight_pre_feeding2 = herbivore2.weight

    highland.feed()

    weight_post_feeding1 = herbivore1.weight
    weight_post_feeding2 = herbivore2.weight

    assert weight_post_feeding1 == weight_pre_feeding1 + herbivore1.param['beta'] * set_f_max \
           and weight_pre_feeding2 == weight_post_feeding2 and highland.current_fodder == 0
