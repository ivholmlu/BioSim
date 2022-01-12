import pytest
from biosim.animals import Herbivores, Carnivores


test_animal1 = {'age': 40, 'weight': 25}

#@pytest.mark.parametrize('a, b', [({'age': 0, 'weight' : 5}, {'age' : 22, 'weight':31})])

test1 = [{'age': 0, 'weight': 5}, {'age': 0, 'weight': 5}]
test2 = [{'age': 22, 'weight': 33}, {'age': 22, 'weight': 33}]
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

    def test_age(self):
        num_years = 10
        for _ in range(num_years):
            self.herb.ages()
            self.carn.ages()
        assert self.herb.age == self.param[0]['age'] + num_years #Dette bør kanskje skrives om?



"""
@pytest.mark.parametrize('age_p, weight_p, expected_fitness', [(40.0, 10.0, 0.250),
                                                               (40.0, 3, 0.165906),
                                                               (30, 25, 0.815553)])
def test_fitness_flux(age_p, weight_p, expected_fitness):

    herb = Herbivores(test_animal1)
    herb.age = age_p
    herb.weight = weight_p
    herb.fitness_flux()
    assert herb.fitness == pytest.approx(expected_fitness)


@pytest.mark.parametrize("weight, gain",
                        [(0, 10),
                         (20, 50),
                         (22, 10)])
class Test_weight:

    def test_weight_gain_Herbivores(self, weight, gain):
        test_animal = {'age' : 0, 'weight' : weight, 'species' : 'Herbivores'}
        animal = Herbivores(test_animal)
        animal.weight_gain(gain)
        assert animal.weight == weight + gain * animal.param['beta']

    def test_weight_gain_Carnivores(self, weight, gain):
        test_animal = {'age' : 0, 'weight' : weight, 'species' : 'Herbivores'}
        animal = Carnivores(test_animal)
        animal.weight_gain(gain)
        assert animal.weight == weight + gain * animal.param['beta']

    def test_weight_loss_Herbivores(self, weight, gain):
        test_animal = {'age': 0, 'weight': weight, 'species': 'Herbivores'}
        animal = Herbivores(test_animal)
        animal.weight_loss()
        assert animal.weight == weight - weight * animal.param['eta']

    def test_weight_loss_Carnivores(self, weight, gain):
        test_animal = {'age': 0, 'weight': weight, 'species': 'Carnivores'}
        animal = Carnivores(test_animal)
        animal.weight_loss()
        assert animal.weight == weight - weight * animal.param['eta']





@pytest.mark.parametrize("age, num_years, expected_age",
                         [(40, 1, 41),
                          (0, 3, 3)])
#Sliter med å få dictionary inn i parametriseringen.
#Funket ikke å skrive inn med dictionary selv om man bruke testclass
def test_aging(age, num_years, expected_age):
    test_animal1['age'] = age
    animal = Herbivores(test_animal1)
    for _ in range(num_years):
        animal.ages()
    assert animal.age == expected_age





@pytest.mark.parametrize('test_animal, num_years, expected',
                        [('test_animal1', 10, 50),
                        ('test_animal2', 3, 3),
                        ('test_animal2', 0, 0)])

def test_aging(test_animal, num_years, expected):
    animal = Herbivores(test_animal)
    for _ in range(num_years):
        animal.ages()
    assert animal.age == expected

def test_herbivores_creation():
    
    Creation has age set to 0
    
    herb = Herbivores(test_animal)
    assert herb.age == test_animal['age']


@pytest.mark.parametrize('age_p, weight_p, expected_fitness', [(40.0, 10.0, 0.250),
                                                               (40.0, 3, 0.165906),
                                                               (30, 25, 0.815553)])
def test_fitness_flux(age_p, weight_p, expected_fitness):
    
    Testing the fitness function with the formula.
    If both values (?) at 0.50 in value the result should be 0.25
    
    herb = Herbivores(test_animal)
    herb.age = age_p
    herb.weight = weight_p
    herb.fitness_flux()
    assert herb.fitness == pytest.approx(expected_fitness)


def test_certain_death():
    
    test_certain_death has omega=1 creating certain death for the herbivores
    since the fitness = 0 at creation
    
    herb = Herbivores(test_animal)
    herb.death(omega=1)
    herb.fitness = 0
    assert herb.alive is False


def test_weight_loss():
    
    test_weight_loss has set weight and eta parameters
    Checks if it gives right return on eight after calculations
    
    herb = Herbivores(test_animal)
    initial_weight = herb.weight
    herb.weight_loss()
    assert herb.weight == initial_weight - initial_weight * Herbivores.param['eta']
"""