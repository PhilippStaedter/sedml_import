# execute script loadModels.py + simulate model
from loadModels import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt

# insert specific model properties as strings, e.g.:
model_name = 'bachmann2011'                                                         # needs automatisation
explicit_model = 'bachmann'

# run function
model = load_specific_model(model_name, explicit_model)


# set timepoints for which we want to simulate the model
model.setTimepoints(np.linspace(0, 240, 1000))                                      # needs automatisation

# Create solver instance
solver = model.getSolver()

# Run simulation using default model parameters and solver options
sim_data = amici.runAmiciSimulation(model, solver)

# np.set_printoptions(threshold=8, edgeitems=2)
for key, value in sim_data.items():
    print('%12s: ' % key, value)

# plot sim_data
amici.plotting.plotStateTrajectories(sim_data)
# amici.plotting.plotObservableTrajectories(sim_data)

# save plot
plt.savefig('../sbml2amici/Figures/Bachmann2011.png')                               # needs automatisation

# show plot
plt.show()
