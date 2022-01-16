"""
Test file to test island module in biosim
"""
import pytest
import textwrap
from biosim.island import Island
from biosim.landscape import Lowland, Highland, Desert, Water
m = 50
n = 20
herb_loc = (2, 2)
carn_loc = (2, 2)

ini_herbs = [{'loc': herb_loc,
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(m)]}]

ini_carns = [{'loc': carn_loc,
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(n)]}]

Island1 = """\
           WWWWW
           WLLLW
           WLLLW
           WLLLW 
           WWWWW"""
Island1 = textwrap.dedent(Island1)

Island2 = """\
           WWWWW
           WDHVW
           WWWWW"""
Island2 = textwrap.dedent(Island2)
Island3 = """\
           WWW
           WDW
           WWW"""
Island3 = textwrap.dedent(Island3)



def test_assign_animals():
    island = Island(Island1)
    island.assign()
    island.assign_animals(ini_herbs)
    assert len(island.cells[herb_loc].herbivores) == m

def test_assign():
    island = Island(Island3)
    island.assign()
    assert type(island.cells[(2, 2)])== type(Desert())

def test_get_animals_per_species():
    island = Island(Island1)
    island.assign()
    island.assign_animals(ini_herbs)
    dict_animals = island.get_animals_per_species()
    assert dict_animals['Herbivore'] == m






