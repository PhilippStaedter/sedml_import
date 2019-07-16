# script for a predictor model to test and predict best simulation parameters

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *


# important paths
tsv_save_path = '../bachelor_thesis/SolverAlgorithm'
total_models_path = '../bachelor_thesis/SolverAlgorithm/Total'
first_tsv_path = '../bachelor_thesis/SolverAlgorithm/Total/1_1_08_06.tsv'

# open one random file and average it to get list of all model names
first_tsv = pd.read_csv(first_tsv_path, sep='\t')
first_tsv = averaging(first_tsv)
model_names = first_tsv['id']

######### create data frame for all models #############
all_models = []
for iCount in range(0, len(model_names)):
    all_models.append(pd.DataFrame())

# open all .tsv files
all_tsv_files = []
solAlg_files = sorted(os.listdir(total_models_path))
for iFile in range(0, len(solAlg_files)):
    next_file = pd.read_csv(total_models_path + '/' + solAlg_files[iFile], sep='\t')
    next_file = averaging(next_file)
    all_tsv_files.append(next_file)


################ get test data #### 166 * [0,1]^32 ############
for iModel in range(0, len(model_names)):

    t_intern = []
    # open all .tsv tolerance files
    solAlg_files = sorted(os.listdir(total_models_path))
    for iFile in range(0, len(solAlg_files)):

        # read in specific model
        for iMdl in range(0, len(all_tsv_files[iFile]['id'])):
            if all_tsv_files[iFile]['id'][iMdl] == model_names[iModel]:
                t_intern.append(all_tsv_files[iFile]['t_intern_ms'][iMdl])

    # get smallest simulation time
    lowlist = sorted(t_intern)
    for iNumber in range(0, len(lowlist)):
        if lowlist[0] == 0:
            del lowlist[0]
        else:
            break
    lowNum = lowlist[0]

    # norm all other simulation times by the smallest one
    for iNum in range(0, len(t_intern)):
        if t_intern[iNum] != 0:
            t_intern[iNum] = lowNum/t_intern[iNum]
        else:
            t_intern[iNum] = 0

    # save t_intern in data frame + change index
    all_models[iModel][model_names[iModel]]= pd.Series(t_intern)


############ save data frames as .tsv file ###############
final_df = all_models[0]
for iDataFrame in range(1, len(all_models)):
    final_df = pd.concat([final_df, all_models[iDataFrame]], axis=1)
final_df = final_df.iloc[:32]

# reindex
par_list = []
for iPar in range(0, len(solAlg_files)):
    par_list.append(solAlg_files[iPar].split('.')[0])
final_df.index = par_list

# save data frame to .tsv
final_df.to_csv(path_or_buf=tsv_save_path + '/Test_Data.tsv', sep='\t', index=True)