from biosim.animals import Herbivores

test_animal = {'age': 0, 'weight': 0}

# @pytest.fixture(autouse = True)
# def create_Herb(self):

def test_aging():
    num_years = 10
    animal = Herbivores(test_animal)
    for _ in range(num_years):
        animal.aging()
    assert animal.age == num_years


def test_herbivores_creation():
    """
    Creation has age set to 0
    """
    Herb = Herbivores(test_animal)
    assert Herb.age == 0

def test_fitness_flux_at_half():
    """
    Testing the fitness function with the formula.
    If both values (?) at 0.50 in value the result should be 0.25
    """
    #Sette verdier inn som parameter når pytest er i bruk
    herb = Herbivores(test_animal)
    herb.age = 40.0
    herb.weight = 10.0
    herb.fitness_flux(phi_age=1, phi_weight=1)
    herb.fitness_flux()
    assert herb.fitness == 0.250

def test_fitness_flux():
    """
    Test fitness_flux with other values.
    values are checked up against CAS in geogebra
    """
    pass



def test_certain_death():
    """
    test_certain_death has omega=1 creating certain death for the herbivores
    since the fitness = 0 at creation
    """
    herb = Herbivores(test_animal)
    herb.death(omega = 1)
    herb.fitness = 0 #Fikse denne når vi går over til @pytest
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





