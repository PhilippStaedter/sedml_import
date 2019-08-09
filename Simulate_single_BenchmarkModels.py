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
import time

iModel = 'Blasi_CellSystems2016'
iFile = 'model_Blasi_CellSystems2016'

path = '../sbml2amici/amici_Benchmark_models'
model_output_dir = path + '/' + iModel + '/' + iFile

# load specific model
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(iFile)

# Create Model instance
model = model_module.getModel()

# set timepoints for which we want to simulate the model
model.setTimepoints(np.linspace(0, 10, 18))

# Create solver instance
solver = model.getSolver()


# Run simulation using default model parameters and solver options
start_time = time.time()
sim_data = amici.runAmiciSimulation(model, solver)
end_time = time.time()

# np.set_printoptions(threshold=8, edgeitems=2)
for key, value in sim_data.items():
    print('%12s: ' % key, value)

# plot sim_data
aplt.plotStateTrajectories(sim_data)
#aplt.plotObservableTrajectories(sim_data)

# show plot
plt.show()

# internal time
print(sim_data['cpu_time'])
print(end_time - start_time)

a=4