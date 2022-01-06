import pytest
from biosim.animals import Herbivores

test_animal = {'age': 40, 'weight': 25}


def test_aging():
    num_years = 10
    animal = Herbivores(test_animal)
    for _ in range(num_years):
        animal.ages()
    assert animal.age == num_years + test_animal['age']


def test_herbivores_creation():
    """
    Creation has age set to 0
    """
    herb = Herbivores(test_animal)
    assert herb.age == test_animal['age']


@pytest.mark.parametrize('age_p, weight_p, expected_fitness', [(40.0, 10.0, 0.250),
                                                               (40.0, 3, 0.165906),
                                                               (30, 25, 0.815553)])
def test_fitness_flux(age_p, weight_p, expected_fitness):
    """
    Testing the fitness function with the formula.
    If both values (?) at 0.50 in value the result should be 0.25
    """
    herb = Herbivores(test_animal)
    herb.age = age_p
    herb.weight = weight_p
    herb.fitness_flux()
    assert herb.fitness == pytest.approx(expected_fitness)


def test_certain_death():
    """
    test_certain_death has omega=1 creating certain death for the herbivores
    since the fitness = 0 at creation
    """
    herb = Herbivores(test_animal)
    herb.death(omega=1)
    herb.fitness = 0
    assert herb.alive is False


def test_weight_loss():
    """
    test_weight_loss has set weight and eta parameters
    Checks if it gives right return on eight after calculations
    """
    herb = Herbivores(test_animal)
    initial_weight = herb.weight
    herb.weight_loss()
    assert herb.weight == initial_weight - initial_weight * Herbivores.param['eta']
