from biosim.animals import Herbivores
test_animal = {'age' : 0, 'weight' : 10,}



class test_aging_dicision():

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
        Herb = Herbivores()
        assert Herb.age == 0




