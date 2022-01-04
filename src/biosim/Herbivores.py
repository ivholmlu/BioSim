"""
Class for herbivores. Will later on be merged into class for animals.
There will herbivores be a subclass


"""


class Herbivores:

    def __init__(self, age, weight, amount):
        self.amount = amount
        self.age = age
        self.weight = weight
        self.pop = []



    def create_population(self):
        pop = [{'pop': 'Herbivore',
                       'age': self.age,
                       'weight': self.weight}
                      for _ in range(self.amount)]




