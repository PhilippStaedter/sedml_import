# reduce number of 202 JWS models (1e-1) to 186 JWS models (1e-4)

import pandas as pd
import os
import shutil

# get new correct models (1e-4)
base_path_new = '../sedml_import/json_files_all_results_BDF_12_12/json_files_1e-04_1e-04'
models_match = []
models_dont_match = []
sbml_1e4 = sorted(os.listdir(base_path_new))
for iModel in sbml_1e4:
  all_sbmls = sorted(os.listdir(base_path_new + '/' + iModel))
  for iSBML in all_sbmls:
    tsv_file = pd.read_csv(base_path_new + '/' + iModel + '/' + iSBML + '/whole_error.csv', sep='\t')
    if tsv_file['trajectories_match'][0] == 1:
        models_match.append('{' + iModel + '}_{' + iSBML + '}')
    else:
        models_dont_match.append('{' + iModel + '}_{' + iSBML + '}')

# get old correct models (1e-1) + delete BioModels models
base_path_old = '../sbml2amici/correct_amici_models_paper_old'
correct_models_until_now = []
sbml_1e1 = sorted(os.listdir(base_path_old))
for iModel in sbml_1e1:
    all_sbmls_1e1 = sorted(os.listdir(base_path_old + '/' + iModel))
    for iSBML in all_sbmls_1e1:
        correct_models_until_now.append('{' + iModel + '}_{' + iSBML + '}')
correct_models = correct_models_until_now[27:]

# get differences between lists
list_of_models_to_be_deleted = sorted(list(set(correct_models) - set(models_match)))


# open all amici import models and delete models
base_path_newer = '../sbml2amici/correct_amici_models_paper'
sbml_1e1_new = sorted(os.listdir(base_path_newer))
for iModel in sbml_1e1_new:
    all_sbmls_1e1 = sorted(os.listdir(base_path_newer + '/' + iModel))
    for iSBML in all_sbmls_1e1:
        model_id = '{' + iModel + '}_{' + iSBML + '}'
        if model_id in list_of_models_to_be_deleted:
            shutil.rmtree(base_path_newer + '/' + iModel + '/' + iSBML)
    if len(os.listdir(base_path_newer + '/' + iModel)) == 0:
        os.rmdir(base_path_newer + '/' + iModel)

# open all .tsv data files of 'WholeStudy' and remove data of those models
path = '../paper_SolverSettings/WholeStudy'
all_tsv_files = sorted(os.listdir(path))
for iTSV in all_tsv_files:
    delete_counter = 0
    tsv_file = pd.read_csv(path + '/' + iTSV, sep='\t')
    for iModel in range(0, len(tsv_file['id'])):
        if tsv_file['id'][iModel - delete_counter] in list_of_models_to_be_deleted:
            tsv_file = tsv_file.drop(labels=iModel - delete_counter, axis=0)
            tsv_file = tsv_file.reset_index(drop=True)
            delete_counter += 1
    tsv_file.to_csv(path + '/' + iTSV, sep='\t', index=False)

# open all .tsv data files of 'Tolerance_1e4' and remove data of those models
for iSolAlg in ['Adams', 'BDF']:
    path_solALg = '../paper_SolverSettings/Tolerances_1e4/' + iSolAlg
    all_tsv_files_solAlg = sorted(os.listdir(path_solALg))
    for iTSV in all_tsv_files_solAlg:
        delete_counter = 0
        tsv_file = pd.read_csv(path_solALg + '/' + iTSV, sep='\t')
        for iModel in range(0, len(tsv_file['id'])):
            if tsv_file['id'][iModel - delete_counter] in list_of_models_to_be_deleted:
                tsv_file = tsv_file.drop(labels=iModel - delete_counter, axis=0)
                tsv_file = tsv_file.reset_index(drop=True)
                delete_counter += 1
        tsv_file.to_csv(path_solALg + '/' + iTSV, sep='\t', index=False)