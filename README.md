# BioSim

This Python package provides the package biosim.

## Contents

- src: Source code that excecutes the simulation
- examples: Examples to show how to use and BioSim's capabilities
- tests : Directory that uses pytest to ensure functionality and creates a filter catching bugs
- docs : Contains the files to create the Sphinx documentation


### Motivation behind BioSim and its capabilities

BioSim was made during the INF200 project at NMBU 2022.
The task has allowed us to understand object oriented programming or OOP in
a much better way. During the january block this BioSim package was created.

#### Capabilities 

The Biosim package can create an island containing a specified amount of cells.
The cells are all assigned with user-defined landscape objects where the user can 
assign animals. The animals can be herbivores or carnivores. The simulation module with
biosim can visualize the yearly cycle on the island and the user can define amount of years
and other parameters to control the vizualisation.

### How to use:

1. The Biosim is run by calling on the biosim module.
2. import biosim.simulation.Biosim to use the simulation class.
3. This class is what is used to generate the simulation and vizualisation of the island.
4. To check what the different parameters do check the documentation, or look at one of the 
    examples provided in the package.


