import pandas as pd
import os
import libsedml
import numpy as np
import libsbml
import sys
import importlib
import amici
import amici.plotting as aplt
import matplotlib.pyplot as plt

iModel = 'Lai2014'
iFile = iModel

path = '../sbml2amici/amici_models'
model_output_dir = path + '/' + iModel + '/' + iFile

# load specific model
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(iFile)

# Create Model instance
model = model_module.getModel()

# set timepoints for which we want to simulate the model
model.setTimepoints(np.linspace(0, 100, 10))

# Create solver instance
solver = model.getSolver()

# Run simulation using default model parameters and solver options
sim_data = amici.runAmiciSimulation(model, solver)

# np.set_printoptions(threshold=8, edgeitems=2)
for key, value in sim_data.items():
    print('%12s: ' % key, value)

# plot sim_data
aplt.plotStateTrajectories(sim_data)
# aplt.plotObservableTrajectories(sim_data)

# show plot
plt.show()

