# script to get the input vector for the predictor model

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *
import libsedml

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
all_models = []
for iCount in range(0, len(stat_par_rec_file['id'])):
    all_models.append(pd.DataFrame())

################ get test data #### 166 * N^3 x [1,7] ############
for iModel in range(0, len(stat_par_rec_file['id'])):

    #### get type of kinetic
    # get more useful model name
    sbml_name,_ = stat_par_rec_file['id'][iModel].split('}')
    _,sbml_name = sbml_name.split('{')

    iSEDML = 'bachmann2011'
    iSBML = 'bachmann'

    if not os.path.exists('./BioModelsDatabase_models/' + iSEDML):
        # read in sbml file
        sbml_file = libsedml.readSedML(sedml_base_path + '/' + iSEDML + '/' + iSEDML + '.sedml')

        # get kinetic law
        all_kinetics = getKineticLaw(iSEDML, iSBML)
    else:
        'BioModels models do not have sedml files!'
        continue


    ### save data
    model = '{' + iSEDML + '}_{' + iSBML + '}'
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
    all_columns = ['num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o']

    # save t_intern in data frame + change index
    all_models[iModel][model_names[iModel]] = pd.Series(all_data)


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

