from changeValues import *
import amici
import amici.plotting
import matplotlib.pyplot as plt
import numpy as np

model_name = 'aguda1999_fig5c'
excplicit_model = 'model0_aguda1'

model = changeValues(model_name, excplicit_model)

# set timepoints for which we want to simulate the model
model.setTimepoints(np.linspace(0, 500, 1000))

# Create solver instance
solver = model.getSolver()

# Run simulation using default model parameters and solver options
sim_data = amici.runAmiciSimulation(model, solver)

# np.set_printoptions(threshold=8, edgeitems=2)
#for key, value in sim_data.items():
#    print('%12s: ' % key, value)

# plot sim_data
amici.plotting.plotStateTrajectories(sim_data)

# show plot
plt.show()