# script to get the input vector for the predictor model

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *

# important paths
stat_par_rec_path = '../sbml2amici/stat_reac_par.tsv'

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
#model_names = stat_par_rec_file['id']

################ get test data #### 160 * [0,1]^32 ############
'''
iter_object = iter(range(0, len(stat_par_rec_file['id'])))
for iModel in iter_object:
    if not iModel == len(stat_par_rec_file['id']):
        if stat_par_rec_file['id'][iModel] == stat_par_rec_file['id'][iModel + 1]:
            stat_par_rec_file = stat_par_rec_file.drop(iModel + 1, axis=0)
            for j in range(0,1):
                i = next(iter_object)
    else:
        if stat_par_rec_file['id'][iModel] == stat_par_rec_file['id'][iModel - 1]:
            stat_par_rec_file = stat_par_rec_file.drop(iModel - 1, axis=0)
'''
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

#stat_par_rec_file.to_csv(path_or_buf='../sbml2amici/TEST_165.tsv', sep='\t', index=True)
######### create data frame for all models #############
all_models = []
for iCount in range(0, len(model_names)):
    all_models.append(pd.DataFrame())

