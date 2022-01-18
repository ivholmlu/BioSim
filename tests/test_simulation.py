"""
Test file to test simulation for biosim
"""
from biosim.simulation import BioSim

geogr = 'WWWWWWWWWWWWWWWWWWWWW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHLLLLWWLLLLLLLWW\nWWHHLLLLLLLWWLLLLLLLW\nWWHHLLLLLLLWWLLLLLLLW\nWWWWWWWWHWWWWLLLLLLLW\nWHHHHHLLLLWWLLLLLLLWW\nWHHHHHHHHHWWLLLLLLWWW\nWHHHHHDDDDDLLLLLLLWWW\nWHHHHHDDDDDLLLLLLLWWW\nWHHHHHDDDDDLLLLLLLWWW\nWHHHHHDDDDDWWLLLLLWWW\nWHHHHDDDDDDLLLLWWWWWW\nWWHHHHDDDDDDLWWWWWWWW\nWWHHHHDDDDDLLLWWWWWWW\nWHHHHHDDDDDLLLLLLLWWW\nWHHHHDDDDDDLLLLWWWWWW\nWWHHHHDDDDDLLLWWWWWWW\nWWWHHHHLLLLLLLWWWWWWW\nWWWHHHHHHWWWWWWWWWWWW\nWWWWWWWWWWWWWWWWWWWWW'
ini_herbs = [{'loc': (2, 7),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 7),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

num_years = 10
def test_simulation():
    """
    Test that Biosim runs without problems
    Runs the simulation for num_years
    Returns
    -------

    """
    sim = BioSim(geogr, ini_herbs + ini_carns, seed=100, vis_years=10)
    sim.simulate(num_years)



