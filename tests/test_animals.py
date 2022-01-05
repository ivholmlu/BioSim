from biosim.animals import Herbivores


test_animal = {'age' : 0, 'weight' : 10}





#    @pytest.fixture(autouse = True)
#    def create_Herb(self):

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





