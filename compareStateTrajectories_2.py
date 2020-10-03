# script 2 to compare state trajectories from JWS with trajectories of the simulation
# => compares state trajectories

# Attention:    boundary conditions are not being simulated by JWS!

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
import json
import itertools
import time


def compStaTraj_JWS_2():
    # upper and lower boundaries for the absolute and relative errors
    AbsError_1 = range(-20,10)
    RelError_2 = range(-20,10)

    # create folder for all results
    folder_path = './FigS1_preselection'
    if not os.path.exists(folder_path):
        print('Error: The folder FigS1_preselection should have been created by now!')
        sys.exit()

    # loop over all created folders containing the simulation data from JWS' built-in routine and Amici
    list_simulation_data = sorted(os.listdir(folder_path))
    for iSimDataGroup in list_simulation_data:
        # get all hyperparameters
        _, __, solAlg, nonLinSol, linSol, absTol, relTol = iSimDataGroup.split('_')

        # iterate over all error combinations
        for iAbsError in range(0, len(AbsError_1)):
            for iRelError in range(0, len(RelError_2)):

                if iAbsError != iRelError:
                    continue

                # set errors
                abs_error = float('1e' + str(AbsError_1[iAbsError]))
                rel_error = float('1e' + str(RelError_2[iRelError]))

                # int2str
                abs_str = '{:.0e}'.format(float(abs_error))
                rel_str = '{:.0e}'.format(float(rel_error))

                print(f"TOLERANCES: abs={abs_str} rel={rel_str}")

                # set counter
                counter = 0

                # measure time needed for all models
                start_time = time.time()

                # iterate over all models
                list_models_with_simulationData = sorted(os.listdir(folder_path + '/' + iSimDataGroup))
                for iMod in range(0, len(list_models_with_simulationData)):
                    iModel = list_models_with_simulationData[iMod]
                    #iModel = 'vanheerden2014_fig4-user'

                    list_files = sorted(os.listdir(folder_path + '/' + iSimDataGroup + '/' + iModel))
                    for iFile in list_files:
                        print(f"    {iModel} :: {iFile}")

                        # important paths
                        old_json_save_path = folder_path + '/' + iSimDataGroup + '/' + iModel + '/' + iFile
                        new_json_save_path = folder_path + '/' + f'all_results_{solAlg}_{nonLinSol}_{linSol}_{absTol}_{relTol}' \
                                             + '/' + 'json_files_' + abs_str + '_' + rel_str + '/' + iModel + '/' + iFile
                        BioModels_path = './BioModelsDatabase_models'

                        if os.path.exists(BioModels_path + '/' + iModel):
                            print('Model is still not part of JWS-database!')
                        else:

                            # create folder
                            if not os.path.exists(new_json_save_path):
                                os.makedirs(new_json_save_path)

                            # open jws_simulation .csv file
                            tsv_file = pd.read_csv(old_json_save_path + '/' + iFile + '_JWS_simulation.csv', sep='\t')

                            # open model_simulation .csv file
                            df_state_trajectory = pd.read_csv(old_json_save_path + '/' + iFile + '_model_simulation.csv', sep='\t')

                            # columns names of .tsv file
                            column_names = list(tsv_file.columns)
                            column_names.remove('time')
                            del tsv_file['time']

                            # comparison
                            amount_col = len(column_names)
                            first_col = column_names[0]
                            amount_row = len(df_state_trajectory[first_col])
                            df_single_error = pd.DataFrame(columns=column_names, data=np.zeros((amount_row, amount_col)))
                            df_trajectory_error = pd.DataFrame(columns=column_names, data=np.zeros((1, amount_col)))
                            df_whole_error = pd.DataFrame(columns=['trajectories_match'], data=np.zeros((1, 1)))

                            # single error
                            for iCol in column_names:
                                for iRow in range(0, amount_row):
                                    rel_tol = abs((df_state_trajectory.at[iRow, iCol] - tsv_file.at[iRow,iCol]) / df_state_trajectory.at[iRow, iCol])
                                    abs_tol = abs(df_state_trajectory.at[iRow, iCol] - tsv_file.at[iRow,iCol])
                                    if rel_tol <= rel_error or abs_tol <= abs_error:
                                        df_single_error.at[iRow, iCol] = 1
                                    else:
                                        df_single_error.at[iRow, iCol] = 0

                            # trajectory error
                            for iCol in column_names:
                                if sum(df_single_error[iCol]) == amount_row:
                                    df_trajectory_error.at[0, iCol] = 1
                                else:
                                    df_trajectory_error.at[0, iCol] = 0

                            # whole error
                            error_list = []
                            for iCol in column_names:
                                error_list.append(df_trajectory_error.at[0, iCol])
                            if sum(error_list) == amount_col:
                                df_whole_error.at[0, 'trajectories_match'] = 1
                            else:
                                df_whole_error.at[0, 'trajectories_match'] = 0

                            # adjust counter
                            if df_whole_error.at[0, 'trajectories_match'] == 1:
                                print('matching state trajectory!')
                                counter = counter + 1

                            # save outcome
                            df_single_error.to_csv(path_or_buf=new_json_save_path + '/single_error.csv', sep='\t', index=False)
                            df_trajectory_error.to_csv(path_or_buf=new_json_save_path + '/trajectory_error.csv', sep='\t', index=False)
                            df_whole_error.to_csv(path_or_buf=new_json_save_path + '/whole_error.csv', sep='\t', index=False)

            # print number of all models with correct state trajectories and display running time
            print('Amount of models with correct state trajectories: ' + str(counter))
            print('time needed: ' + str(time.time() - start_time))


# call function
compStaTraj_JWS_2()
