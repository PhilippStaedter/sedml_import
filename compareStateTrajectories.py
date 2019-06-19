# script to compare state trajectories from JWS with trajectories of the simulation

from execute_loadModels import *
from colourDataFrame import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt
import libsbml
import time
import statistics
import pandas as pd
import os
import urllib.request


iModel = 'bachmann2011'
iFile = 'bachmann'

# create folder
if not os.path.exists('./json_files/' + iModel + '/' + iFile):
    os.makedirs('./json_files/' + iModel + '/' + iFile)

# important paths
json_save_path = './json_files/' + iModel + '/' + iFile

# Get whole model
model = all_settings(iModel,iFile)


######### jws simulation
# Get time data with num_time_points == 100
t_data = model.getTimepoints()
sim_start_time = t_data[0]
sim_end_time = t_data[len(t_data) - 1]
sim_num_time_points = 101                                                                           #len(t_data)
model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

# Get Url
url = 'https://jjj.bio.vu.nl/rest/models/' + iFile + '/time_evolution?time_end=' + str(sim_end_time) + ';species=all'

# Save .json file
urllib.request.urlretrieve(url, json_save_path + '/' + iFile + '.json')

# write as .csv file
json_2_csv = pd.read_json(json_save_path + '/' + iFile + '.json')
json_2_csv.to_csv(json_save_path + '/' + iFile + '.csv', sep='\t', index=False)

# open new .csv file
tsv_file = pd.read_csv(json_save_path + '/' + iFile + '.csv', sep='\t')

# columns names of .tsv file
column_names = list(tsv_file.columns)
column_names.remove('time')
del tsv_file['time']


########## model simulation
# Create solver instance
solver = model.getSolver()

# Simulate model
sim_data = amici.runAmiciSimulation(model, solver)

# np.set_printoptions(threshold=8, edgeitems=2)
for key, value in sim_data.items():
    print('%12s: ' % key, value)

# Get state trajectory
state_trajectory = sim_data['x']

# Convert ndarray 'state-trajectory' to data frame
df_state_trajectory = pd.DataFrame(columns=column_names, data=state_trajectory)


########## comparison
error = 1e-7
amount_col = len(column_names)
first_col = column_names[0]
amount_row = len(df_state_trajectory[first_col])
df_error = pd.DataFrame(columns=column_names, data=np.zeros((amount_row, amount_col)))

for iCol in column_names:
    for iRow in range(0, amount_row):
        if abs(df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow]) <= error:
            df_error[iCol][iRow] = True
        else:
            df_error[iCol][iRow] = False
df_error.style.applymap(colour)
