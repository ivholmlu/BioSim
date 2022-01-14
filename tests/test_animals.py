import pytest
from biosim.animals import Herbivores, Carnivores
import math
from scipy import stats

seed = 41
ALPHA = 0.01

@pytest.mark.parametrize('test_animal', [{'age': 0, 'weight': 5},
                                             {'age': 22, 'weight': 33},
                                             {'age': 3, 'weight': 8}])
class TestCreationAndFunc:

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_eq_age_creation(self, test_animal, species):
        """
        Test if 2 objects with same parameters have the same weight and age
        after creation.
        """
        obj1 = species(test_animal)
        obj2 = species(test_animal)

        assert obj1.age == obj2.age and obj1.weight == obj2.weight

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_eq_aging(self, test_animal, species):
        """
        Test if two objects have increased the same after num_years
        and have gained the expected age
        """
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        start_age = obj1.age
        num_years = 10
        expected = start_age + num_years
        for _ in range(num_years):
            obj1.ages()
            obj2.ages()
        assert obj1.age == obj2.age and (obj1.age and obj2.age) == expected


    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_weight_gain(self, species, test_animal):
        """
        Test if the weight is gained as intended. Food eaten multiplied with parameter beta
        """
        obj1 = species(test_animal)
        gain = 20
        expected = gain*obj1.param['beta'] + obj1.weight
        obj1.weight_gain(gain)
        assert obj1.weight == expected

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_weight_loss(self, species, test_animal):
        """
        Test if weight loss every year is lost with the formula:
        new body weight =current body weight - (current body weight * eta)
        """
        obj1 = species(test_animal)
        expected = obj1.weight - obj1.weight * obj1.param['eta']
        obj1.weight_loss()
        assert obj1.weight == expected

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_certain_death(self, species, test_animal):
        """
        Creates a certain death scenario for all N animals. Checks if all objects alive attributes
        have been set to False
        """
        N = 50
        obj1 = species(test_animal)
        obj1.param['omega'] = 1
        obj1.fitness = 0
        for _ in range(N):
            obj1.death()
            assert not obj1.alive

    @pytest.mark.parametrize('species', [Herbivores, Carnivores]) # MULIGENS KOMBINERE DENNE OG DEN OVENFOR?
    def test_zero_weigth_death(self, species, test_animal):
        """
        Test if animals attribute alive attribute is set to zero when weight = 0
        """
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        obj1.weight = 0
        obj2.weight = 0
        for _ in range(50):
            (obj1.death(), obj2.death())
            assert obj1.alive is False
            assert obj2.alive is False

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_birth_herbivores(self, species, test_animal):
        """
        Setting parameter to ensure 100% chance for birth
        Test if baby has weight above zero which means that the animal object
        has given birth
        """
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        obj1.fitness = 1
        obj1.weight = 100
        obj1.param['gamma'] = 1
        obj1.birth(100)

        assert obj1.baby['weight'] > 0.0

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_migration(self, species, test_animal):
        """
        Setting parameters to ensure migration for all cases. Checks if the migration attribute
        is changed to True.
        """
        obj1 = species()
        obj1.fitness = 1
        obj1.param['mu'] = 1
        assert obj1.migration() is True

    @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_birth_distr(self, species, test_animal):
        """
        Test is inspired from Hans Plessers bacteria death distribution test
        The test checks if the Z-value from the birth disstribution is lower than the ALPHA value.
        """
        obj1 = species(test_animal)

        #Seed øverst i syntaksen
        num = 10
        N = 10
        obj1.fitness = 1
        obj1.weight = 100
        obj1.param['gamma'] = 1
        mean = obj1.param['w_birth']
        std = obj1.param['sigma_birth']
        for _ in range(num):
            obj1.birth(N)
            weight = obj1.baby['weight']
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


class TestSetWrongParameters:

    def test_invalid_key(self):
        Herb = Herbivores()
        Herb.set_params({'not_a_key': 0})
        self.assertRaises(KeyError, lambda: my_dict['some_key'])

"""

    def test_birth_distribution(self):
        """"""
        The weight for newborn babies should fall within the bell curve for the
        normal distribution. This test checks with alpha certainty that it does.
        Add parameters to ensure 100% birth rate
        This test only check if the baby is within 2 STD from the mean weight
        It will fail about 1/20 times
        """"""
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
        
        
        @pytest.mark.parametrize('species', [Herbivores, Carnivores])
    def test_ages(self, species, test_animal):
        
        obj1 = species(test_animal)
        obj2 = species(test_animal)
        num_years = 5
        expected = num_years + obj1.age
        [(obj1.ages(), obj2.ages()) for _ in range(num_years)]
        assert obj1.age and obj2.age == expected
"""
