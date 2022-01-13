import pytest
from biosim.animals import Herbivores, Carnivores
import math
from scipy import stats

seed = 44
ALPHA = 0.01

test1 = {'age': 0, 'weight': 5}
test2 = {'age': 22, 'weight': 33}
test3 = {'age': 3, 'weight': 8}

@pytest.mark.parametrize('test_animal', [{'age': 0, 'weight': 5},
                                             {'age': 22, 'weight': 33},
                                             {'age': 3, 'weight': 8}])

class TestCreationAndFunc:
    @pytest.mark.parametrize('species', [Herbivores, Carnivores])

    def test_eq_age_creation(self, test_animal, species):
        obj1 = species(test_animal)
        obj2 = species(test_animal)

        assert obj1.age == obj2.age

    def test_eq_aging(self, species, test_animal):
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        num_years = 10
        for _ in range(num_years):
            obj1.ages(test_animal)
            obj2.ages(test_animal)
        assert obj1.age == obj2.age

    def test_ages(self, species, test_animal):
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        num_years = 5
        expected = num_years + obj1.age
        [(obj1.ages(), obj2.ages()) for _ in range(num_years)]
        assert obj1.age and obj2.age == expected

    def test_weight_gain(self, species, test_animal):
        obj1 = species(test_animal)
        gain = 20
        expected = gain*obj1.param['beta'] + obj1.weight
        obj1.weight_gain(gain)
        assert obj1.weight == expected

    def test_weight_loss(self, species, test_animal):
        obj1 = species(test_animal)
        expected = obj1.weight - obj1.weight * obj1.param['eta']
        obj1.weight_loss()
        assert obj1.weight == expected

    def test_certain_death(self, species, test_animal):
        obj1 = species(test_animal)
        obj1.param['omega'] = 1
        obj1.fitness = 0
        for _ in range(50):
            obj1.death()
            assert not obj1.alive

    def test_zero_weigth_death(self, species, test_animal):
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        for _ in range(50):
            (obj1.death(), obj2.death())
            assert obj1.alive is False
            assert obj2.alive is False


    def test_birth_herbivores(self, species, test_animal):
        """
        Setting parameter to ensure 100% chance for birth
        Test if baby has weight above zero which means that the animal object
        has given birth
        """
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        obj1.fitness = 1
        obj1.herb.weight = 100
        obj1.param['gamma'] = 1
        obj1.birth(100)

        assert obj1.baby['weight'] > 0.0

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
        num, N = 10, 10000
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
