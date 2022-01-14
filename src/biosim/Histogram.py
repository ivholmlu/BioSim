"""
File to incoorperate histogram plotting in simulation.simulate
"""
import numpy as np
import matplotlib.pyplot as plt

def update(n_year, year):

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(0, n_year)
    ax.set_ylim(0, 1)

    line = ax.plot(np.arange(n_year),
                   np.full(n_year, np.nan), 'b-')[0]

    ydata = line.get_ydata()
    ydata[year] = np.random.random()
    line.set_ydata(ydata)
    plt.pause(1e-6)