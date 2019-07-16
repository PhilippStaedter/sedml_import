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
    sedml_name,_ = stat_par_rec_file['id'][iModel].split('}')
    _,sedml_name = sedml_name.split('{')

    sedml_name = 'bachmann2011'

    if not os.path.exists('./BioModelsDatabase_models/' + sedml_name):
        # read in sedml file
        sedml_file = libsedml.readSedML(sedml_base_path + '/' + sedml_name + '/' + sedml_name + '.sedml')

        # get number of tasks, observables and variables
        num_task = sedml_file.getNumTasks()
        num_obs = sedml_file.getNumDataGenerators()

        # get formula
        all_var = []
        all_formulas = []
        for iTask in range(0, num_task):
            for iObservable in range(0, num_obs):
                # get all variables
                num_var = sedml_file.getDataGenerator(iObservable).getNumVariables()
                var_list = []
                for iVar in range(0, num_var):
                    var_id = sedml_file.getDataGenerator(iObservable).getVariable(iVar).getId()
                    if not var_id == 'time':
                        var_list.append(var_id)
                all_var.append(var_list)

                # get all formulas
                obs_Formula = libsedml.formulaToString(sedml_file.getDataGenerator(iObservable).getMath())
                if not obs_Formula == 'time':
                    all_formulas.append(obs_Formula)

                # assign number of 1 - 7
                kinetic_list = []
                # check if a variable is in the formula and where it is
                for iVar in range(0, len(var_list)):
                    if var_list[iVar] in obs_Formula:
                        if '/' in obs_Formula:                                                                          # for how many denominators should be looked for?
                            index1 = obs_Formula.find('/')
                            if obs_Formula.find(var_list[iVar], index1 + 1, len(obs_Formula)) != -1:
                                print('We have a variable in a denominator! => We have a Kinetic!')
                                if obs_Formula.find('/', index1 + 1, len(obs_Formula)) != -1:
                                    index2 = obs_Formula.find('/', index1 + 1, len(obs_Formula))
                                    if obs_Formula.find(var_list[iVar], index2 + 1, len(obs_Formula)) != -1:
                                        kinetic_list.append('5/6/7')
                                    else:
                                        print('Variable could be in a nominator!')
                                        kinetic_list.append('5/6/7')
                                else:
                                    print('Variable could be in a nominator!')
                                    kinetic_list.append('5/6/7')
                            else:
                                print('No variable in denominator!')
                                kinetic_list.append('1/2/3/4')
                        else:
                            print('No denominator!')
                            kinetic_list.append('1/2/3/4')
                    else:
                        print('Variable ' + var_list[iVar] + ' is not in the formula!')
                        kinetic_list.append(0)

        # give total kinetic number from 1 - 7
        kin = sorted(kinetic_list, reverse=True)[0]

    else:
        'BioModels models do not have sedml files!'
        continue


    ### save data
    num_x = stat_par_rec_file['states'][iModel]
    num_r = stat_par_rec_file['reactions'][iModel]
    num_p = stat_par_rec_file['parameters'][iModel]
    all_data = [num_x, num_r, num_p, kin]

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
# final_df.to_csv(path_or_buf=tsv_save_path + '/Input_Data.tsv', sep='\t', index=True)

