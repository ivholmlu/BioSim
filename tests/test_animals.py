from biosim.animals import Herbivores
test_animal = {'age' : 0, 'weight' : 10}

def test_aging():

    num_years = 10
    animal = Herbivores(test_animal)
    for _ in range(num_years):
        animal.aging()
    assert animal.age == num_years



