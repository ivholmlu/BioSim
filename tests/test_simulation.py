"""
Test file to test simulation for biosim
"""
import pytest
SEEED = 100
from biosim.simulation import BioSim
import textwrap
geogr = """\
           WWWWW
           WLLLW
           WLHLW
           WDDHW
           WWWWW"""

geogr = textwrap.dedent(geogr)

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(200)]}]
ini_carns = [{'loc': (2, 3),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(50)]}]

num_years = 10
seed = 100


def test_simulation():
    """
    Test that Biosim runs without problems
    Runs the simulation for num_years
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


@pytest.mark.parametrize('landscape, f_max',[('H', {'f_max': 100}), ('L', {'f_max': 300}), ('D', {'f_max': 40})])
def test_set_param_f_max(landscape, f_max):
    """
    Test to check that set parameters work for all existing landscapes and that
    non existing landscapes return ValueError
    """
    sim = BioSim(geogr, ini_herbs + ini_carns)
    sim.set_landscape_parameters(landscape, f_max)
    with pytest.raises(ValueError):
        sim.set_landscape_parameters('S', {'f_max' : 100})



