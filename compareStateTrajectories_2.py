# script 2 to compare state trajectories from JWS with trajectories of the simulation
# => compares state trajectories

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


# set errors
abs_error = 1e-4  # tighter conditions give back 'False' most of the time
rel_error = 1e-4

# int2str
abs_str = '{:.0e}'.format(float(abs_error))
rel_str = '{:.0e}'.format(float(rel_error))

# parse numbers
abs_number = abs_str.split('0')[1]                                                  # for two digital numbers at the end (e.g. 1e-12), one must split at '-'
rel_number = rel_str.split('0')[1]

# create folder for all .csv files of the results
if not os.path.exists('./json_files_' + abs_number + '_' + rel_number):
    os.makedirs('./json_files_' + abs_number + '_' + rel_number)

# set counter
counter = 0

# get name of jws reference
url = "https://jjj.bio.vu.nl/rest/models/?format=json"
view_source = requests.get(url)
json_string = view_source.text
json_dictionary = json.loads(json_string)

# get all models
list_directory_amici = sorted(os.listdir('../sbml2amici/amici_models'))
# del list_directory_amici[0:31]                                                                                          # delete until model with error to avoid repeating all

# iterate over all models again
for iMod in range(0, len(list_directory_amici)):

    iModel = list_directory_amici[iMod]
    # iModel = 'bachmann2011'
    list_files = sorted(os.listdir('./sedml_models/' + iModel + '/sbml_models'))

    for iFile in list_files:

        # iFile without .sbml extension
        iFile, extension = iFile.split('.', 1)

        # important paths
        old_json_save_path = './json_files/' + iModel + '/' + iFile
        new_json_save_path = './json_files_' + abs_number + '_' + rel_number + '/' + iModel + '/' + iFile
        sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'
        sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
        BioModels_path = './BioModelsDatabase_models'


        if os.path.exists(BioModels_path + '/' + iModel):
            print('Model is still not part of JWS-database!')                                                                       # error 1
        else:

            if not os.path.exists(old_json_save_path):
                print('Model ' + iModel + '_' + iFile + ' crashed some other way!')                                                 # error 2
            else:

                # create folder
                if not os.path.exists('./json_files_' + abs_number + '_' + rel_number + '/' + iModel + '/' + iFile):
                    os.makedirs('./json_files_' + abs_number + '_' + rel_number + '/' + iModel + '/' + iFile)

                # open jws_simulation .csv file
                tsv_file = pd.read_csv(old_json_save_path + '/' + iFile + '_JWS_simulation.csv', sep='\t')

                # open model_simulation .csv file
                df_state_trajectory = pd.read_csv(old_json_save_path + '/' + iFile + '_model_simulation.csv', sep='\t')

                # columns names of .tsv file
                column_names = list(tsv_file.columns)
                column_names.remove('time')
                del tsv_file['time']


                ########## comparison
                amount_col = len(column_names)
                first_col = column_names[0]
                amount_row = len(df_state_trajectory[first_col])
                df_single_error = pd.DataFrame(columns=column_names, data=np.zeros((amount_row, amount_col)))
                df_trajectory_error = pd.DataFrame(columns=column_names, data=np.zeros((1, amount_col)))
                df_whole_error = pd.DataFrame(columns=['trajectories_match'], data=np.zeros((1, 1)))

                # single error
                for iCol in column_names:
                    for iRow in range(0, amount_row):
                        rel_tol = abs((df_state_trajectory[iCol][iRow] - tsv_file[iCol][iRow]) / df_state_trajectory[iCol][iRow])
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
                    counter = counter + 1

                ############ save outcome
                df_single_error.to_csv(path_or_buf=new_json_save_path + '/single_error.csv', sep='\t', index=False)
                df_trajectory_error.to_csv(path_or_buf=new_json_save_path + '/trajectory_error.csv', sep='\t', index=False)
                df_whole_error.to_csv(path_or_buf=new_json_save_path + '/whole_error.csv', sep='\t', index=False)

# print number of all models with correct state trajectories
print(counter)
