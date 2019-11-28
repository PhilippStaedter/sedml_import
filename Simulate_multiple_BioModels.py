import os
import numpy as np
import sys
import importlib
import amici
import amici.plotting as aplt
import matplotlib.pyplot as plt
import time
from setTime_BioModels import *


All_Models_with_proteins = [#'Lai2014', 'Levchenko2000a', 'Proctor2010a', 'Proctor2013a', 'Qi2013a', 'Ung2008']#,
                            #'ODea2007', 'Pritchard2002', 'Ueda2001', 'Eungdamrong2007', 'Froehlich2018', 'Holzhutter2004']
                            #'Hui2014', 'Liu2011', 'Ouzounoglou2014', 'Pathak2013', 'Pathak2013a', 'Singh2006']#,
                            'Sivakumar2011c', 'Bungay2003', 'Bungay2006', 'Bungay2006a', 'Sasagawa2005', 'Sengupta2015', 'Yang2007']#,

'''
('Aguilera - not yet imported'), ('Baker2013 - not yet imported'), ('Chance1943 - not yet imported'),
('Clarke2000 - not yet imported'), ('Ehrenstein - not yet imported'), ('Klipp2002 - not yet imported'),
('Lebeda2008a - not yet imported'), ('Barr2017 - not yet imported'), ('DellaPezze2014 - not yet imported'),
('Goldbeter1991 - not yet imported'), ('Heldt2018 - not yet imported'), ('Kholodenko2000 - not yet imported'),
('Mitchell2013 - not yet imported'),  ('Mueller2015 - not yet imported'), ('Muraro2014 - not yet imported'),
('Noguchi2013 - not yet imported'), ('Orton2009 - not yet imported'), ('SmithAE2002 - not yet imported'),
('Smallbone - only in MATLAB'), ('vanEunen2013 - maybe in MATLAB'), ('Leloup1999 - maybe in MATLAB'),]
'''

# create axes object
ax1 = plt.axes()

# different colours
colour = ['orange', 'cyan', 'violet', 'tan', 'blue', 'lavender', 'black']

# minimize all x-values and y-values
x_bound = []
y_bound = []
for iModel in range(0, len(All_Models_with_proteins)):
    sim_start_time, sim_end_time, sim_num_time_points, sim_trajectory_bound = timePointsBioModels(All_Models_with_proteins[iModel])
    x_bound.append(sim_end_time)
    y_bound.append(sim_trajectory_bound)
sim_start_time = 0
sim_num_time_points = 50
#min_x_bound = sorted(x_bound)[0]
#min_y_bound = sorted(y_bound)[0]
#median_x_bound = np.median(x_bound)
#median_y_bound = np.median(y_bound)
max_x_bound = sorted(x_bound, reverse=True)[0]
max_y_bound = sorted(y_bound, reverse=True)[0]


# plot all models in one axes object
for iModel in range(0, len(All_Models_with_proteins)):

    iFile = All_Models_with_proteins[iModel]

    path = '../sbml2amici/amici_models'
    model_output_dir = path + '/' + All_Models_with_proteins[iModel] + '/' + iFile

    # load specific model
    sys.path.insert(0, os.path.abspath(model_output_dir))
    model_module = importlib.import_module(iFile)

    # Create Model instance
    model = model_module.getModel()

    # set timepoints for which we want to simulate the model
    model.setTimepoints(np.linspace(sim_start_time, 1, sim_num_time_points))

    # Create solver instance
    solver = model.getSolver()


    # Run simulation using default model parameters and solver options
    start_time = time.time()
    sim_data = amici.runAmiciSimulation(model, solver)
    end_time = time.time()

    # np.set_printoptions(threshold=8, edgeitems=2)
    for key, value in sim_data.items():
        print('%12s: ' % key, value)

    # plot sim_data - alternative to 'amici.plotting'
    state_indices = range(sim_data['x'].shape[1])
    for ix in state_indices:
        # ax1.plot(sim_data['t'], sim_data['x'][:, ix - 1], color=colour[iModel])
        # /np.max(sim_data['t'])
        ax1.plot(sim_data['t']/np.max(sim_data['t']), sim_data['x'][:, ix - 1]/np.max(sim_data['x'][:, ix - 1]), color=colour[iModel], alpha=0.5)
    ax1.plot(sim_data['t']/np.max(sim_data['t']), sim_data['x'][:, len(state_indices) - 1]/np.max(sim_data['x'][:, len(state_indices) - 1]), color=colour[iModel], alpha=0.5, label=All_Models_with_proteins[iModel])
    #ax1.set_xlim(sim_start_time, median_x_bound)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel('$t$')
    ax1.set_ylabel('$x_i(t)$ (mmol/ml)')
    ax1.legend(bbox_to_anchor=(1, 0.5))
    ax1.set_title('State trajectories')
    #aplt.plotStateTrajectories(sim_data, state_indices=None, ax=ax1)
    #aplt.plotObservableTrajectories(sim_data)


# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(14.5, 9)

# save figure
plt.savefig('../ODE_protein/Figures/Fourth_scaled_both.pdf')

# show plot
plt.show()