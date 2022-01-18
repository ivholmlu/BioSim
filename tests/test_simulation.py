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
seed = 100
def test_simulation():
    """
    Test that Biosim runs without problems and runs the simulation for num_years as defined above.
    """
    sim = BioSim(geogr, ini_herbs + ini_carns, seed=seed, vis_years=10)
    sim.simulate(num_years)

def test_no_plot_simulation():
    """
    Test to check that the plot window does not appear when vis_years is set to 0.
    """
    sim = BioSim(geogr, ini_herbs, seed=seed, vis_years=0)
    sim.simulate(50)
    sim.add_population(ini_carns)
    sim.simulate(50)





