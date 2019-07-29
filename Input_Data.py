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
               '1_1_08_06', '1_1_10_14', '1_1_12_10', '1_1_16_08', '1_6_08_06', '1_6_10_14', '1_6_12_10', '1_6_16_08',
               '1_7_08_06', '1_7_10_14', '1_7_12_10', '1_7_16_08', '1_8_08_06', '1_8_10_14', '1_8_12_10', '1_8_16_08',
               '1_9_08_06', '1_9_10_14', '1_9_12_10', '1_9_16_08', '2_1_08_06', '2_1_10_14', '2_1_12_10', '2_1_16_08',
               '2_6_08_06', '2_6_10_14', '2_6_12_10', '2_6_16_08', '2_7_08_06', '2_7_10_14', '2_7_12_10', '2_7_16_08',
               '2_8_08_06', '2_8_10_14', '2_8_12_10', '2_8_16_08', '2_9_08_06', '2_9_10_14', '2_9_12_10', '2_9_16_08']
df = pd.DataFrame(columns=all_columns, data=[])

################ get test data #### 166 * N^3 x [1,7] ############
# initialize counter
counter = 0

list_directory_sedml = sorted(os.listdir(sedml_base_path))
for iSEDML in list_directory_sedml:

    iSEDML = 'bachmann2011'

    mod_SEDML = '{' + iSEDML + '}'
    if mod_SEDML in new_list or mod_SEDML == '{kolodkin2010_figure2b}':

        list_directory_sbml = sorted(os.listdir(sedml_base_path + '/' + iSEDML + '/sbml_models'))
        if mod_SEDML != '{kolodkin2010_figure2b}':
            iSBML = list_directory_sbml[0]

            # same as down

        else:
            for iSBML in list_directory_sbml:

                #### get type of kinetic
                all_kinetics = getKineticLaw(iSEDML,iSBML)

                ### save data
                #model = '{' + iSEDML + '}_{' + iSBML + '}'
                num_x = stat_par_rec_file['num_x'][iModel]
                num_r = stat_par_rec_file['num_r'][iModel]
                num_p = stat_par_rec_file['num_p'][iModel]
                p_n = all_kinetics[0]
                p_l = all_kinetics[1]
                p_q = all_kinetics[2]
                p_p = all_kinetics[3]
                p_e = all_kinetics[4]
                p_L = all_kinetics[5]           # <==> Michaelis Menten ?
                p_Q = all_kinetics[6]           # <==
                p_P = all_kinetics[7]           #  ==
                p_E = all_kinetics[8]           #  ==> Hill ?
                p_o = all_kinetics[9]
                all_data = [num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

                # save all_data in data frame
                df.append({}, ignore_index=True)
                df.loc[counter].num_x = num_x

                counter = counter + 1

############ save data frames as .tsv file ###############
final_df = all_models[0]
for iDataFrame in range(1, len(all_models)):
    final_df = pd.concat([final_df, all_models[iDataFrame]], axis=1)
final_df = final_df.iloc[:32]

# reindex
par_list = []
for iPar in range(0, len(all_data)):
    par_list.append(all_data[iPar].split('.')[0])
final_df.index = par_list

# save data frame to .tsv
# final_df.to_csv(path_or_buf=tsv_save_path + '/Input_Data.tsv', sep='\t', index=False)

