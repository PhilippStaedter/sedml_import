# script 2 to compare state trajectories from BioModels with trajectories of the simulation created by COPASI
# => creates two important .tsv files

# Attention:    boundary conditions are not being simulated by COPASI!
# all trajectories simulated by COPASI were simulated with absolute and relative tolerances 1e-14 & 1e-14,
# except three models where 1e-12 & 1e-12 had to be used.

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


def compStaTraj_BioModels_2():
    # upper and lower boundaries for the absolute and relative errors
    AbsError_1 = range(-20, 10)
    RelError_2 = range(-20, 10)

    # create folder for all results
    folder_path = './FigS1_preselection'
    if not os.path.exists(folder_path):
        print('Error: The folder FigS1_preselection should have been created by now!')
        sys.exit()

    # filter for those that contain 'COPASI_'
    del_counter = 0
    list_simulation_data = sorted(os.listdir(folder_path))
    for iItem in range(0, len(list_simulation_data)):
        if not 'COPASI_' in list_simulation_data[iItem - del_counter]:
            del list_simulation_data[iItem - del_counter]
            del_counter += 1

    for iSimDataGroup in list_simulation_data:
        # get all hyperparameters
        _, __, solAlg, nonLinSol, linSol, absTol, relTol = iSimDataGroup.split('_')

        # iterate over all error combinations
        for iAbsError in range(0, len(AbsError_1)):
            for iRelError in range(0, len(RelError_2)):

                if iAbsError != iRelError:
                    continue

                # set errors
                abs_error = float('1e' + str(AbsError_1[iAbsError]))  # tighter conditions give back 'False' most of the time
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
                list_directory_bio = sorted(os.listdir(folder_path + '/' + iSimDataGroup))
                for iMod in range(0, len(list_directory_bio)):
                    iModel = list_directory_bio[iMod]
                    # iModel = 'Bungay2003'

                    # important paths
                    old_bio_save_path = folder_path + '/' + iSimDataGroup + '/' + iModel
                    new_bio_save_path = folder_path + '/' + f'all_results_COPASI_{solAlg}_{nonLinSol}_{linSol}_{absTol}_{relTol}' \
                                         + '/' + 'json_files_' + abs_str + '_' + rel_str + '/' + iModel

                    if not os.path.exists(old_bio_save_path):
                        print('Model ' + iModel + ' crashed some other way!')
                    else:

                        # create folder
                        if not os.path.exists(new_bio_save_path):
                            os.makedirs(new_bio_save_path)

                        # open COPASI_simulation .tsv file
                        tsv_file = pd.read_csv(f"{old_bio_save_path}/{iModel}_COPASI_simulation.tsv", sep='\t')

                        # open model_simulation .tsv file
                        df_state_trajectory = pd.read_csv(f"{old_bio_save_path}/{iModel}_model_simulation.tsv", sep='\t')

                        # columns names of COPASI file
                        column_names = list(tsv_file.columns)

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
                                rel_tol = abs((df_state_trajectory.at[iRow, iCol] - tsv_file.at[iRow, iCol]) /
                                              df_state_trajectory.at[iRow, iCol])
                                abs_tol = abs(df_state_trajectory.at[iRow, iCol] - tsv_file.at[iRow, iCol])
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
                        df_single_error.to_csv(path_or_buf=new_bio_save_path + '/single_error.csv', sep='\t', index=False)
                        df_trajectory_error.to_csv(path_or_buf=new_bio_save_path + '/trajectory_error.csv', sep='\t', index=False)
                        df_whole_error.to_csv(path_or_buf=new_bio_save_path + '/whole_error.csv', sep='\t', index=False)

            # print number of all models with correct state trajectories
            print('Amount of models with correct state trajectories: ' + str(counter))
            print('time needed: ' + str(time.time() - start_time))


# call function
compStaTraj_BioModels_2()
