# script to compare state trajectories from JWS with trajectories of the simulation

# Attention:    boundary conditions are not being simualted by JWS!

from execute_loadModels import *
from JWS_changeValues import *
from colourDataFrame import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt
import libsbml
import libsedml
import time
import statistics
import pandas as pd
import os
import urllib.request


# set counter
counter = 0

# get all models
list_directory_sedml = sorted(os.listdir('../sbml2amici/amici_models'))

for iModel in list_directory_sedml:

    list_files = sorted(os.listdir('./sedml_models/' + iModel + '/sbml_models'))

    for iFile in list_files:

        # iModel = 'aguda1999_fig5c'
        # iFile = 'model0_aguda1'

        # iFile without .sbml extension
        iFile, extension = iFile.split('.', 1)

        # important paths
        json_save_path = './json_files/' + iModel + '/' + iFile
        sedml_path = './sedml_models/' + iModel + '/' + iModel +'.sedml'
        sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
        BioModels_path = './BioModelsDatabase_models'


        if os.path.exists(BioModels_path + '/' + iModel):
            print('Model is not part of JWS-database!')
        else:
            # parse correct name for url
            sbml_name, mod_iFile = iFile.split('_', 1)

            try:
                # Get whole model
                model = all_settings(iModel,iFile)

                # create folder
                if not os.path.exists('./json_files/' + iModel + '/' + iFile):
                    os.makedirs('./json_files/' + iModel + '/' + iFile)
            except:
                print('Model ' + iModel + ' extension is missing!')
                continue

            ######### jws simulation
            # Get time data with num_time_points == 100
            t_data = model.getTimepoints()
            sim_start_time = t_data[0]
            sim_end_time = t_data[len(t_data) - 1]
            sim_num_time_points = 101                                                                           #len(t_data)
            model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

            # Open sedml file
            sedml_model = libsedml.readSedML(sedml_path)

            # import all cahnges from SEDML
            list_of_strings = JWS_changeValues(iFile, sedml_model)

            # Get Url with all changes
            # <species 1>=<amount>
            # <parameter 1>=<value>, compartment == parameter (in this case)
            url = 'https://jjj.bio.vu.nl/rest/models/' + mod_iFile + '/time_evolution?time_end=' + str(sim_end_time) + ';species=all;'
            for iStr in list_of_strings:
                url = url + iStr

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

            # Open SBML file
            sbml_model = libsbml.readSBML(sbml_path)

            # Delete all trajectories for boundary conditions
            all_properties = sbml_model.getModel()
            for iSpec in range(0, all_properties.getNumSpecies()):
                all_species = all_properties.getSpecies(iSpec)
                if all_species.getBoundaryCondition() == True:
                    state_trajectory = state_trajectory.transpose()
                    state_trajectory = np.delete(state_trajectory, iSpec,0)
                    state_trajectory = state_trajectory.transpose()

            # Convert ndarray 'state-trajectory' to data frame
            df_state_trajectory = pd.DataFrame(columns=column_names, data=state_trajectory)


            ########## comparison
            error = 1e-3                                                                                                            # tighter conditions give back 'False' most of the time
            amount_col = len(column_names)
            first_col = column_names[0]
            amount_row = len(df_state_trajectory[first_col])
            df_single_error = pd.DataFrame(columns=column_names, data=np.zeros((amount_row, amount_col)))
            df_trajectory_error = pd.DataFrame(columns=column_names, data=np.zeros((1, amount_col)))
            df_whole_error = pd.DataFrame(columns=['trajectories_match'], data=np.zeros((1, 1)))

            # single error
            for iCol in column_names:
                for iRow in range(0, amount_row):
                    rel_error = abs((df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow])/df_state_trajectory[iCol][iRow])
                    abs_error = abs(df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow])
                    if rel_error <= error or abs_error <= error:
                        df_single_error[iCol][iRow] = True
                    else:
                        df_single_error[iCol][iRow] = False
            # df_error.style.applymap(colour)

            # trajectory error
            for iCol in column_names:
                if sum(df_single_error[iCol]) == amount_row:
                    df_trajectory_error[iCol][0] = True
                else:
                    df_trajectory_error[iCol][0] = False

            # whole error
            list = []
            for iCol in column_names:
                list.append(df_trajectory_error[iCol][0])
            if sum(list) == amount_col:
                df_whole_error['trajectories_match'][0] = True
            else:
                df_whole_error['trajectories_match'][0] = False

            # adjust counter
            if df_whole_error['trajectories_match'][0] == True:
                counter = counter +1

            ############ save outcome
            # df_single_error.to_csv(path_or_buf= json_save_path + '/single_error.csv', sep='\t', index=False)
            # df_trajectory_error.to_csv(path_or_buf= json_save_path + '/trajectory_error.csv', sep='\t', index=False)
            # df_whole_error.to_csv(path_or_buf= json_save_path + '/whole_error.csv', sep='\t', index=False)


# print number of all models with correct state trajectories
print(counter)