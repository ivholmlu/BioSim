import pytest
from biosim.animals import Herbivores, Carnivores
import math
from scipy import stats

seed = 44
ALPHA = 0.01

test1 = {'age': 0, 'weight': 5}
test2 = {'age': 22, 'weight': 33}
test3 = {'age': 3, 'weight': 8}


@pytest.mark.parametrize('parameters', [test1, test2, test3])
class Test_Creation_And_Func:
    @pytest.fixture(autouse=True)
    def create_objects(self, parameters):
        self.herb = Herbivores(parameters)
        self.carn = Carnivores(parameters)

    def test_eq_age(self):
        assert self.carn.age == self.herb.age

    def test_eq_aging(self):
        self.herb.ages()
        self.carn.ages()
        assert self.herb.age == self.carn.age

    def test_ages(self):
        num_years = 5
        expected = num_years + self.herb.age
        [(self.herb.ages(), self.carn.ages()) for _ in range(num_years)]
        assert self.herb.age and self.carn.age == expected

    def test_weight_gain_herb(self):
        gain = 20
        animals = [self.herb, self.carn]
        for animal in animals:
            expected = gain*animal.param['beta'] + animal.weight
            animal.weight_gain(gain)
            assert animal.weight == expected

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

    def test_certain_death_herb(self):
        self.herb.param['omega'] = 1
        self.herb.fitness = 0
        for _ in range(50):
            self.herb.death()
            assert not self.herb.alive

    def test_certain_death_carn(self):
        self.carn.param['omega'] = 1
        self.carn.fitness = 0
        for _ in range(50):
            self.carn.death()
            assert not self.carn.alive

    def test_zero_weigth_death(self):
        self.carn.weight = 0
        self.herb.weight = 0
        (self.carn.death(), self.herb.death())
        assert not self.herb.alive == True
        assert not self.carn.alive == True


    def test_birth_herbivores(self):
        """
        Setting parameter to ensure 100% chance for birth
        Test if baby has weight above zero which means that the animal object
        has given birth
        """
        self.herb.fitness = 1
        self.herb.weight = 100
        self.herb.param['gamma'] = 1
        self.herb.birth(100)

        assert self.herb.baby['weight'] > 0.0


    def test_birth_carnivores(self):

        self.carn.fitness = 1
        self.carn.weight = 100
        self.carn.param['gamma'] = 1
        self.carn.birth(100)

        assert self.carn.baby['weight'] > 0

    def test_birth_distribution(self):
        """
        The weight for newborn babies should fall within the bell curve for the
        normal distribution. This test checks with alpha certainty that it does.
        Add parameters to ensure 100% birth rate
        This test only check if the baby is within 2 STD from the mean weight
        It will fail about 1/20 times
        """
        self.carn.fitness = 1
        self.carn.weight = 100
        self.carn.param['gamma'] = 1
        self.carn.birth(100)
        weight = self.carn.baby['weight']
        mean = self.carn.param['w_birth']
        std = self.carn.param['sigma_birth']
        lower_limit = mean - 2*std
        upper_limit = mean + 2*std
        assert weight < upper_limit and weight > lower_limit

    def test_birth_distr(self):
        """
        Test is inspired from Hans Plessers bacteria death distribution test
        """
        #Seed øverst i syntaksen
        num, N = 100000, 10000
        self.carn.fitness = 1
        self.carn.weight = 100
        self.carn.param['gamma'] = 1
        weight = self.carn.baby['weight']
        mean = self.carn.param['w_birth']
        std = self.carn.param['sigma_birth']
        for _ in range(num):
            self.carn.birth(N)
            weight = self.carn.baby['weight']
            Z = (weight - mean) / math.sqrt(std)
            Z_value_prob = 2* stats.norm.cdf((-abs(Z))) #Tosidig test
            assert Z_value_prob > ALPHA

























@pytest.mark.parametrize('expected_fitness, weigth_age_parameters', [
                                                             (0.250, {'age': 40, 'weight': 10}),
                                                             (0.165906, {'age': 40, 'weight': 3}),
                                                             (0.815553, {'age': 30, 'weight': 25})])
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
