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
from setTime_BioModels import *

iModel = 'Proctor2010a'
iFile = iModel

path = '../sbml2amici/amici_models'
model_output_dir = path + '/' + iModel + '/' + iFile

# load specific model
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(iFile)

# Create Model instance
model = model_module.getModel()

# set timepoints for which we want to simulate the model
sim_start_time, sim_end_time, sim_num_time_points, y_bound = timePointsBioModels(iModel)
model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

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
# alternative to amici.plotting
ax1 = plt.axes()
state_indices = range(sim_data['x'].shape[1])
for ix in state_indices:
    ax1.plot(sim_data['t'], sim_data['x'][:, ix], color='orange' , label='$x_{%d}$' % ix)
    ax1.set_xlabel('$t$ (s)')
    ax1.set_ylabel('$x_i(t)$ (mmol/ml)')
    ax1.set_title('State trajectories')
#aplt.plotStateTrajectories(sim_data, state_indices=range(0,42))
#aplt.plotObservableTrajectories(sim_data)

# show plot
plt.show()

# internal time
#print(sim_data['cpu_time'])
#print(end_time - start_time)

#a=4
