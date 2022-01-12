import pytest
from biosim.animals import Herbivores, Carnivores


test_animal1 = {'age': 40, 'weight': 25}

#@pytest.mark.parametrize('a, b', [({'age': 0, 'weight' : 5}, {'age' : 22, 'weight':31})])

test1 = [{'age': 0, 'weight': 5}, {'age': 0, 'weight': 5}]
test2 = [{'age': 22, 'weight': 33}, {'age': 22, 'weight': 33}]
test3 = [{'age': 3, 'weight' : 8}, {'age': 3, 'weight' : 8}]
@pytest.mark.parametrize('a, b', [test1, test2])
class Test_creation:
    @pytest.fixture(autouse=True)
    def create_objects(self, a, b):
        self.param = [a, b]
        self.herb = Herbivores(a)
        self.carn = Carnivores(b)

    def test_eq_age(self):
        assert self.carn.age == self.herb.age

    def test_eq_aging(self):
        self.herb.ages()
        self.carn.ages()
        assert self.herb.age == self.carn.age

    def test_ages(self):
        num_years = 5
        expected = num_years + self.param[0]['age']
        for _ in range(num_years):
            self.herb.ages()
            self.carn.ages()
        assert self.herb.age and self.carn.age == expected
                 #Dette bør kanskje skrives om?

    def test_weight_gain_herb(self):
        gain = 20
        expected = gain*self.herb.param['beta'] + self.herb.weight
        self.herb.weight_gain(gain)
        assert self.herb.weight == expected

    def test_weight_gain_carn(self):
        gain = 20
        expected = gain*self.carn.param['beta'] + self.carn.weight
        self.carn.weight_gain(gain)
        assert self.carn.weight == expected

    def test_weight_loss_herb(self):
        expected = self.herb.weight - self.herb.weight * self.herb.param['eta']
        self.herb.weight_loss()
        assert self.herb.weight == expected

    def test_weight_loss_carn(self):
        expected = self.carn.weight - self.carn.weight * self.carn.param['eta']
        self.carn.weight_loss()
        assert self.carn.weight == expected

@pytest.mark.parametrize('expected_fitness, weigth_age_parameters'
                                                            , [(0.250, {'age': 40, 'weight':10}),
                                                               (0.165906, {'age': 40, 'weight':3}),
                                                               (0.815553, {'age': 30, 'weight':25})])
def test_fitness_flux(expected_fitness, weigth_age_parameters):
    """
    Tests if the fitness_flux function calculates right values.
    40 and 10 are the 'a_half' and 'w_half' parameters. If inserted for herbivores
    they will return 0.250
    The others are values calculated by Ivar using CAS from Geogebra and the formula
    """
    herb = Herbivores(weigth_age_parameters)
    herb.fitness_flux()
    assert herb.fitness == pytest.approx(expected_fitness)

"""


def test_certain_death():
    
    test_certain_death has omega=1 creating certain death for the herbivores
    since the fitness = 0 at creation
    
    herb = Herbivores(test_animal)
    herb.death(omega=1)
    herb.fitness = 0
    assert herb.alive is False

"""