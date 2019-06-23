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
import requests
import json
import itertools


# create folder for all results
if not os.path.exists('./json_files'):
    os.makedirs('./json_files')

# set counter
counter = 0

# get name of jws reference
url = "https://jjj.bio.vu.nl/rest/models/?format=json"
view_source = requests.get(url)
json_string = view_source.text
json_dictionary = json.loads(json_string)

# get all models
list_directory_sedml = sorted(os.listdir('../sbml2amici/amici_models'))
del list_directory_sedml[0:153]                                                                                          # delete until model with error to avoid repeating all

for iMod in range(0, len(list_directory_sedml)):

    iModel = list_directory_sedml[iMod]
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

            # Open SBML file
            sbml_model = libsbml.readSBML(sbml_path)

            # get right model reference from sbml model
            parse_name_model = sbml_model.getModel().getId()
            for iCount in range(0, len(json_dictionary)):
                parse_name_jws = json_dictionary[iCount]['slug']
                if parse_name_model == parse_name_jws:
                    model_reference = json_dictionary[iCount]['slug']
                    break
            # elements in json_dictionary are only lower case --- the sbml model has upper case models
            try:
                model_reference
            except:
                wrong_model_name = ["".join(x) for _, x in itertools.groupby(parse_name_model, key=str.isdigit)]
                if wrong_model_name[0].islower() == False:
                    correct_model_letters = wrong_model_name[0].lower()
                    correct_model_name = correct_model_letters + wrong_model_name[1]
                    for iCount in range(0, len(json_dictionary)):
                        parse_name_jws = json_dictionary[iCount]['slug']
                        if correct_model_name == parse_name_jws:
                            model_reference = json_dictionary[iCount]['slug']
                            break
            # check if all_settings works
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
            url = 'https://jjj.bio.vu.nl/rest/models/' + model_reference + '/time_evolution?time_end=' + str(sim_end_time) + ';species=all;'

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

            # Delete all trajectories for boundary conditions
            delete_counter = 0
            all_properties = sbml_model.getModel()
            for iSpec in range(0, all_properties.getNumSpecies()):
                all_species = all_properties.getSpecies(iSpec)
                if all_species.getBoundaryCondition() == True:
                    state_trajectory = state_trajectory.transpose()
                    if delete_counter == 0:
                        state_trajectory = np.delete(state_trajectory, iSpec, 0)
                    else:
                        state_trajectory = np.delete(state_trajectory, iSpec - delete_counter, 0)
                    state_trajectory = state_trajectory.transpose()
                    delete_counter = delete_counter + 1

            # Convert ndarray 'state-trajectory' to data frame
            df_state_trajectory = pd.DataFrame(columns=column_names, data=state_trajectory)


            ########## comparison
            abs_error = 1e-4                                                                                                            # tighter conditions give back 'False' most of the time
            rel_error = 1e-4
            amount_col = len(column_names)
            first_col = column_names[0]
            amount_row = len(df_state_trajectory[first_col])
            df_single_error = pd.DataFrame(columns=column_names, data=np.zeros((amount_row, amount_col)))
            df_trajectory_error = pd.DataFrame(columns=column_names, data=np.zeros((1, amount_col)))
            df_whole_error = pd.DataFrame(columns=['trajectories_match'], data=np.zeros((1, 1)))

            # single error
            for iCol in column_names:
                for iRow in range(0, amount_row):
                    rel_tol = abs((df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow])/df_state_trajectory[iCol][iRow])
                    abs_tol = abs(df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow])
                    if rel_tol <= rel_error or abs_tol <= abs_error:
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
            error_list = []
            for iCol in column_names:
                error_list.append(df_trajectory_error[iCol][0])
            if sum(error_list) == amount_col:
                df_whole_error['trajectories_match'][0] = True
            else:
                df_whole_error['trajectories_match'][0] = False

            # adjust counter
            if df_whole_error['trajectories_match'][0] == True:
                counter = counter +1

            ############ save outcome
            df_single_error.to_csv(path_or_buf= json_save_path + '/single_error.csv', sep='\t', index=False)
            df_trajectory_error.to_csv(path_or_buf= json_save_path + '/trajectory_error.csv', sep='\t', index=False)
            df_whole_error.to_csv(path_or_buf= json_save_path + '/whole_error.csv', sep='\t', index=False)


# print number of all models with correct state trajectories
print(counter)