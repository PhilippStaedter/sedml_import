# script to get the input vector for the predictor model

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
        new_id = '{kolodkin2010_figure2b}_' + str(iFile)
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
all_columns = ['model', 'num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o',
               'c_1_1_08_06', 'c_1_1_10_14', 'c_1_1_12_10', 'c_1_1_16_08', 'c_1_6_08_06', 'c_1_6_10_14', 'c_1_6_12_10', 'c_1_6_16_08',
               'c_1_7_08_06', 'c_1_7_10_14', 'c_1_7_12_10', 'c_1_7_16_08', 'c_1_8_08_06', 'c_1_8_10_14', 'c_1_8_12_10', 'c_1_8_16_08',
               'c_1_9_08_06', 'c_1_9_10_14', 'c_1_9_12_10', 'c_1_9_16_08', 'c_2_1_08_06', 'c_2_1_10_14', 'c_2_1_12_10', 'c_2_1_16_08',
               'c_2_6_08_06', 'c_2_6_10_14', 'c_2_6_12_10', 'c_2_6_16_08', 'c_2_7_08_06', 'c_2_7_10_14', 'c_2_7_12_10', 'c_2_7_16_08',
               'c_2_8_08_06', 'c_2_8_10_14', 'c_2_8_12_10', 'c_2_8_16_08', 'c_2_9_08_06', 'c_2_9_10_14', 'c_2_9_12_10', 'c_2_9_16_08']
df = pd.DataFrame(columns=all_columns, data=[])
df['model'] = model_names

################ get INPUT data ################
list_directory_sedml = sorted(os.listdir(sedml_base_path))
for iSEDML in list_directory_sedml:

    iSEDML = 'chassagnole2002_fig4-user'

    mod_SEDML = '{' + iSEDML + '}'
    print(mod_SEDML)
    if mod_SEDML in list(model_names) or mod_SEDML == '{kolodkin2010_figure2b}':

        list_directory_sbml = sorted(os.listdir(sedml_base_path + '/' + iSEDML + '/sbml_models'))
        if mod_SEDML != '{kolodkin2010_figure2b}':
            iSBML = list_directory_sbml[0]

            #### get type of kinetic
            all_kinetics = getKineticLaw(iSEDML, iSBML)

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
            all_data = [num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

            # save all_data in data frame
            for iModel in range(0, len(model_names)):
                if df['model'][iModel] == mod_SEDML:
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

        else:
            kolodkin_list = ['{kolodkin2010_figure2b}_96', '{kolodkin2010_figure2b}_97', '{kolodkin2010_figure2b}_98',
                             '{kolodkin2010_figure2b}_99', '{kolodkin2010_figure2b}_100', '{kolodkin2010_figure2b}_101']
            for iKolodkin in range(0, len(list_directory_sbml)):

                iSBML = list_directory_sbml[iKolodkin]

                #### get type of kinetic
                all_kinetics = getKineticLaw(iSEDML, iSBML)

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
                all_data = [num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

                # save all_data in data frame
                for iModel in range(0, len(model_names)):
                    if df['model'][iModel] == kolodkin_list[iKolodkin]:
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


############# get OUTPUT data ############
# open output data file
output_data_file = pd.read_csv(output_data_path, sep='\t')

# new counter
counter = 0

# assign right data to right place
for iModel_output in range(0, len(output_data_file.column)):
    for iModel_input in range(0, len(df['model'])):
        if output_data_file.column[iModel_output] == df['model'][iModel_input]:
            df.loc[counter].c_1_1_08_06 = output_data_file.column[iModel_output][0]




############ save data frames as .tsv file ###############
# final_df.to_csv(path_or_buf=tsv_save_path + '/Input_Data.tsv', sep='\t', index=False)

