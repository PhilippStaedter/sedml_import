# script to get the input and output vector for the predictor model

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *
from KineticLaw import *

# important paths
stat_par_rec_path = '../sbml2amici/stat_reac_par.tsv'
output_data_path = '../bachelor_thesis/SolverAlgorithm/Test_Data.tsv'
sedml_base_path = './sedml_models'
tsv_save_path = '../bachelor_thesis/SolverAlgorithm'

# open .tsv file
stat_par_rec_file = pd.read_csv(stat_par_rec_path, sep='\t')

# change model names
new_list = []
for iFile in range(0, len(stat_par_rec_file['id'])):
    new_id = stat_par_rec_file['id'][iFile].split('_{')[0]
    if new_id == '{kolodkin2010_figure2b}':
        new_id = '{kolodkin2010_figure2b}_' + str(iFile - 7)                                                            # need '-7' because in stat_rec_par file no averaging has been done
    new_list.append(new_id)
stat_par_rec_file['id'] = new_list

# rearrange data
iModel = 0
while iModel < len(stat_par_rec_file['id']):
    if not iModel == len(stat_par_rec_file['id']) - 1:
        if stat_par_rec_file['id'][iModel] == stat_par_rec_file['id'][iModel + 1]:
            if stat_par_rec_file['id'][iModel + 1] == '{levchenko2000_fig2-user}' and stat_par_rec_file['states'][iModel + 1] == 22:
                iModel = iModel + 1
            else:
                stat_par_rec_file = stat_par_rec_file.drop(iModel + 1, axis=0)
                stat_par_rec_file = stat_par_rec_file.reset_index(drop=True)
        else:
            iModel = iModel + 1

    else:
        if stat_par_rec_file['id'][iModel] == stat_par_rec_file['id'][iModel - 1]:
            stat_par_rec_file = stat_par_rec_file.drop(iModel - 1, axis=0)
        else:
            iModel = iModel + 1

# all later column names
model_names = stat_par_rec_file['id']

######### create data frame for all models #############
all_columns = ['model', 'error_rate', 'num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o', 'combinations', 'value']
'''
all_columns = ['model', 'error_rate', 'num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o',
               '1_1_08_06', '1_1_10_14', '1_1_12_10', '1_1_16_08', '1_6_08_06', '1_6_10_14', '1_6_12_10', '1_6_16_08',
               '1_7_08_06', '1_7_10_14', '1_7_12_10', '1_7_16_08', '1_8_08_06', '1_8_10_14', '1_8_12_10', '1_8_16_08',
               '1_9_08_06', '1_9_10_14', '1_9_12_10', '1_9_16_08', '2_1_08_06', '2_1_10_14', '2_1_12_10', '2_1_16_08',
               '2_6_08_06', '2_6_10_14', '2_6_12_10', '2_6_16_08', '2_7_08_06', '2_7_10_14', '2_7_12_10', '2_7_16_08',
               '2_8_08_06', '2_8_10_14', '2_8_12_10', '2_8_16_08', '2_9_08_06', '2_9_10_14', '2_9_12_10', '2_9_16_08']
'''
new_df = pd.DataFrame(columns=all_columns, data=[])
#df = pd.DataFrame(columns=all_columns, data=[])
#df['model'] = model_names

################ get INPUT data ################
# open output data file
output_data_file = pd.read_csv(output_data_path, sep='\t')

# set counter
counter = 0
error_counter = 0

# error file
total_error_file = pd.DataFrame(columns=['model', 'error'], data=[])

list_directory_sedml = sorted(os.listdir(sedml_base_path))
#list_directory_sedml = list_directory_sedml[92:]
for iSEDML in list_directory_sedml:

    #iSEDML = 'teusink1998_fig3candd-user'

    mod_SEDML = '{' + iSEDML + '}'
    print(mod_SEDML)
    if mod_SEDML in list(model_names) or mod_SEDML == '{kolodkin2010_figure2b}':

        # new data frame
        df = pd.DataFrame(columns=all_columns, data=[])

        # Append additional row in .tsv file
        df = df.append({}, ignore_index=True)

        list_directory_sbml = sorted(os.listdir(sedml_base_path + '/' + iSEDML + '/sbml_models'))
        if mod_SEDML != '{kolodkin2010_figure2b}' and mod_SEDML != '{levchenko2000_fig2-user}':
            iSBML = list_directory_sbml[0]

            #### get type of kinetic
            all_kinetics, error_file = getKineticLaw(iSEDML, iSBML)

            ### save data
            for iModel in range(0, len(model_names)):
                if stat_par_rec_file['id'][iModel] == mod_SEDML:
                    num_x = stat_par_rec_file['states'][iModel]
                    num_r = stat_par_rec_file['reactions'][iModel]
                    num_p = stat_par_rec_file['parameters'][iModel]

            p_n = all_kinetics[0]
            p_l = all_kinetics[1]
            p_q = all_kinetics[2]
            p_p = all_kinetics[3]
            p_e = all_kinetics[4]
            p_L = all_kinetics[5]  # <==> Michaelis Menten ?
            p_Q = all_kinetics[6]  # <==
            p_P = all_kinetics[7]  # ==
            p_E = all_kinetics[8]  # ==> Hill ?
            p_o = all_kinetics[9]
            error_rate = all_kinetics[10]
            all_data = [error_rate, num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

            # save all_data in data frame
            df['model'][counter] = mod_SEDML
            df['error_rate'][counter] = error_rate
            df['num_x'][counter] = num_x
            df['num_r'][counter] = num_r
            df['num_p'][counter] = num_p
            df['p_n'][counter] = p_n
            df['p_l'][counter] = p_l
            df['p_q'][counter] = p_q
            df['p_p'][counter] = p_p
            df['p_e'][counter] = p_e
            df['p_L'][counter] = p_L
            df['p_Q'][counter] = p_Q
            df['p_P'][counter] = p_P
            df['p_E'][counter] = p_E
            df['p_o'][counter] = p_o

            # duplicate the newly created row 40 times for all different combinations
            df = pd.concat([df] * len(output_data_file['combinations']), ignore_index=True)
            for iComb in range(0, len(output_data_file['combinations'])):
                df.loc[counter].combinations = output_data_file['combinations'][iComb]

                # assign right value to right place
                for iModel_output in range(1, len(output_data_file.columns)):  # column 'combinations' is unnecessary
                    for iModel_input in range(0, len(df['model'])):
                        if output_data_file.columns[iModel_output] == df['model'][iModel_input]:
                            #df.loc[counter].value = output_data_file[output_data_file.columns[iModel_output]][iComb]
                            #break
                            
                            if output_data_file[output_data_file.columns[iModel_output]][iComb] > 0:
                                df.loc[counter].value = 1
                                break
                            else:
                                df.loc[counter].value = 0
                                break
                            
                        break
                counter = counter + 1

            # reset counter
            counter = 0

            # append df to new_df
            new_df = new_df.append(df, ignore_index=True)
            total_error_file = total_error_file.append(error_file, ignore_index=True)

        elif mod_SEDML == '{kolodkin2010_figure2b}':
            kolodkin_list = ['{kolodkin2010_figure2b}_89', '{kolodkin2010_figure2b}_90', '{kolodkin2010_figure2b}_91',
                             '{kolodkin2010_figure2b}_92', '{kolodkin2010_figure2b}_93', '{kolodkin2010_figure2b}_94']
            for iKolodkin in range(0, len(list_directory_sbml)):

                # new data frame
                df = pd.DataFrame(columns=all_columns, data=[])

                # Append additional row in .tsv file
                df = df.append({}, ignore_index=True)

                iSBML = list_directory_sbml[iKolodkin]

                #### get type of kinetic
                all_kinetics, error_file = getKineticLaw(iSEDML, iSBML)

                ### save data
                for iModel in range(0, len(model_names)):
                    if stat_par_rec_file['id'][iModel] == kolodkin_list[iKolodkin]:
                        num_x = stat_par_rec_file['states'][iModel]
                        num_r = stat_par_rec_file['reactions'][iModel]
                        num_p = stat_par_rec_file['parameters'][iModel]

                p_n = all_kinetics[0]
                p_l = all_kinetics[1]
                p_q = all_kinetics[2]
                p_p = all_kinetics[3]
                p_e = all_kinetics[4]
                p_L = all_kinetics[5]  # <==> Michaelis Menten ?
                p_Q = all_kinetics[6]  # <==
                p_P = all_kinetics[7]  # ==
                p_E = all_kinetics[8]  # ==> Hill ?
                p_o = all_kinetics[9]
                error_rate = all_kinetics[10]
                all_data = [error_rate, num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

                # save all_data in data frame
                df['model'][counter] = kolodkin_list[iKolodkin]
                df['error_rate'][counter] = error_rate
                df['num_x'][counter] = num_x
                df['num_r'][counter] = num_r
                df['num_p'][counter] = num_p
                df['p_n'][counter] = p_n
                df['p_l'][counter] = p_l
                df['p_q'][counter] = p_q
                df['p_p'][counter] = p_p
                df['p_e'][counter] = p_e
                df['p_L'][counter] = p_L
                df['p_Q'][counter] = p_Q
                df['p_P'][counter] = p_P
                df['p_E'][counter] = p_E
                df['p_o'][counter] = p_o

                '''
                # save all_data in data frame
                for iModel in range(0, len(model_names)):
                    if df['model'][iModel] == kolodkin_list[iKolodkin]:
                        df['error_rate'][iModel] = error_rate
                        df['num_x'][iModel] = num_x
                        df['num_r'][iModel] = num_r
                        df['num_p'][iModel] = num_p
                        df['p_n'][iModel] = p_n
                        df['p_l'][iModel] = p_l
                        df['p_q'][iModel] = p_q
                        df['p_p'][iModel] = p_p
                        df['p_e'][iModel] = p_e
                        df['p_L'][iModel] = p_L
                        df['p_Q'][iModel] = p_Q
                        df['p_P'][iModel] = p_P
                        df['p_E'][iModel] = p_E
                        df['p_o'][iModel] = p_o
                '''

                # duplicate the newly created row 40 times for all different combinations
                df = pd.concat([df] * len(output_data_file['combinations']), ignore_index=True)
                for iComb in range(0, len(output_data_file['combinations'])):
                    df.loc[counter].combinations = output_data_file['combinations'][iComb]

                    # assign right value to right place
                    for iModel_output in range(1, len(output_data_file.columns)):                                       # column 'combinations' is unnecessary
                        for iModel_input in range(0, len(df['model'])):
                            if output_data_file.columns[iModel_output] == df['model'][iModel_input]:
                                #df.loc[counter].value = output_data_file[output_data_file.columns[iModel_output]][iComb]
                                #break

                                if output_data_file[output_data_file.columns[iModel_output]][iComb] > 0:
                                    df.loc[counter].value = 1
                                    break
                                else:
                                    df.loc[counter].value = 0
                                    break

                            break
                    counter = counter + 1

                # reset counter
                counter = 0

                # append df to new_df
                new_df = new_df.append(df, ignore_index=True)
                total_error_file = total_error_file.append(error_file, ignore_index=True)

        elif mod_SEDML == '{levchenko2000_fig2-user}':
            levchenko_list = ['{levchenko2000_fig2-user}', '{levchenko2000_fig2-user}']

            for iLevchenko in range(0, len(list_directory_sbml) - 5):

                # new data frame
                df = pd.DataFrame(columns=all_columns, data=[])

                # Append additional row in .tsv file
                df = df.append({}, ignore_index=True)

                iSBML = list_directory_sbml[iLevchenko + 5]

                #### get type of kinetic
                all_kinetics, error_file = getKineticLaw(iSEDML, iSBML)

                ### save data
                for iModel in range(0, len(model_names)):
                    if stat_par_rec_file['id'][iModel] == levchenko_list[iLevchenko]:
                        if iLevchenko == 0:
                            num_x = stat_par_rec_file['states'][iModel]
                            num_r = stat_par_rec_file['reactions'][iModel]
                            num_p = stat_par_rec_file['parameters'][iModel]
                            break
                        else:
                            num_x = stat_par_rec_file['states'][iModel]
                            num_r = stat_par_rec_file['reactions'][iModel]
                            num_p = stat_par_rec_file['parameters'][iModel]

                p_n = all_kinetics[0]
                p_l = all_kinetics[1]
                p_q = all_kinetics[2]
                p_p = all_kinetics[3]
                p_e = all_kinetics[4]
                p_L = all_kinetics[5]  # <==> Michaelis Menten ?
                p_Q = all_kinetics[6]  # <==
                p_P = all_kinetics[7]  # ==
                p_E = all_kinetics[8]  # ==> Hill ?
                p_o = all_kinetics[9]
                error_rate = all_kinetics[10]
                all_data = [error_rate, num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

                # save all_data in data frame
                df['model'][counter] = levchenko_list[iLevchenko]
                df['error_rate'][counter] = error_rate
                df['num_x'][counter] = num_x
                df['num_r'][counter] = num_r
                df['num_p'][counter] = num_p
                df['p_n'][counter] = p_n
                df['p_l'][counter] = p_l
                df['p_q'][counter] = p_q
                df['p_p'][counter] = p_p
                df['p_e'][counter] = p_e
                df['p_L'][counter] = p_L
                df['p_Q'][counter] = p_Q
                df['p_P'][counter] = p_P
                df['p_E'][counter] = p_E
                df['p_o'][counter] = p_o

                '''
                # save all_data in data frame
                for iModel in range(0, len(model_names)):
                    if df['model'][iModel] == kolodkin_list[iKolodkin]:
                        df['error_rate'][iModel] = error_rate
                        df['num_x'][iModel] = num_x
                        df['num_r'][iModel] = num_r
                        df['num_p'][iModel] = num_p
                        df['p_n'][iModel] = p_n
                        df['p_l'][iModel] = p_l
                        df['p_q'][iModel] = p_q
                        df['p_p'][iModel] = p_p
                        df['p_e'][iModel] = p_e
                        df['p_L'][iModel] = p_L
                        df['p_Q'][iModel] = p_Q
                        df['p_P'][iModel] = p_P
                        df['p_E'][iModel] = p_E
                        df['p_o'][iModel] = p_o
                '''

                # duplicate the newly created row 40 times for all different combinations
                df = pd.concat([df] * len(output_data_file['combinations']), ignore_index=True)
                for iComb in range(0, len(output_data_file['combinations'])):
                    df.loc[counter].combinations = output_data_file['combinations'][iComb]

                    # assign right value to right place
                    for iModel_output in range(1, len(output_data_file.columns)):                                       # column 'combinations' is unnecessary
                        for iModel_input in range(0, len(df['model'])):
                            if output_data_file.columns[iModel_output] == df['model'][iModel_input] and output_data_file.columns[iModel_output + 1] == '{levchenko2000_fig2-user}.1':
                                if iLevchenko == 0:
                                    #df.loc[counter].value = output_data_file[output_data_file.columns[iModel_output]][iComb]
                                    #break

                                    if output_data_file[output_data_file.columns[iModel_output]][iComb] > 0:
                                        df.loc[counter].value = 1
                                        break
                                    else:
                                        df.loc[counter].value = 0
                                        break

                                elif iLevchenko == 1:
                                    #df.loc[counter].value = output_data_file[output_data_file.columns[iModel_output + 1]][iComb]
                                    #break

                                    if output_data_file[output_data_file.columns[iModel_output + 1]][iComb] > 0:
                                        df.loc[counter].value = 1
                                        break
                                    else:
                                        df.loc[counter].value = 0
                                        break

                    counter = counter + 1

                # reset counter
                counter = 0

                # append df to new_df
                new_df = new_df.append(df, ignore_index=True)
                total_error_file = total_error_file.append(error_file, ignore_index=True)


'''
############# get OUTPUT data ############
# open output data file
output_data_file = pd.read_csv(output_data_path, sep='\t')

# new counter
counter = 0

# assign right data to right place
for iModel_output in range(1, len(output_data_file.columns)):                                                           # column 'combinations' is unnecessary
    for iModel_input in range(0, len(df['model'])):
        if output_data_file.columns[iModel_output] == df['model'][iModel_input]:
            for iComb in range(0, len(output_data_file[output_data_file.columns[0]])):
                if output_data_file[output_data_file.columns[iModel_output]][iComb] > 0:
                    df.loc[counter][output_data_file[output_data_file.columns[0]][iComb]] = 1
                else:
                    df.loc[counter][output_data_file[output_data_file.columns[0]][iComb]] = 0
            counter = counter + 1
'''


############ save data frames as .tsv file ###############
new_df.to_csv(path_or_buf=tsv_save_path + '/Input_Output_Data_0_1_updated.tsv', sep='\t', index=False)
total_error_file.to_csv(tsv_save_path + '/Error_file.tsv', sep='\t', index=False)


