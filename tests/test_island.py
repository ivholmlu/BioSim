"""
Test file to test island module in biosim
"""
import pytest
import textwrap
from biosim.island import Island
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

Island1 = """
           WWWWW
           WLLLW
           WLLLW
           WLLLW 
           WWWWW"""
Island1 = textwrap.dedent(Island1)

Island2 = """
           WWWWW
           WDHVW
           WWWWW"""
Island2 = textwrap.dedent(Island2)


def test_assign_animals():
    island = Island(Island1)
    island.assign(ini_carns)
    island.assign(ini_herbs)



