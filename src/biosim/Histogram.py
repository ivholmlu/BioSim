"""
File to incoorperate histogram plotting in simulation.simulate
"""
import numpy as np
import matplotlib.pyplot as plt

class Histogram:

    def __init__(self):
        self.line = None

    def setup(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_year)
        ax.set_ylim(0, 1)

        self.line = ax.plot(np.arange(n_year),
                       np.full(n_year, np.nan), 'b-')[0]

    def update(self, year, Herbivore):

        ydata = self.line.get_ydata()
        ydata[year] = Herbivore
        self.line.set_ydata(ydata)
        plt.pause(1e-6)