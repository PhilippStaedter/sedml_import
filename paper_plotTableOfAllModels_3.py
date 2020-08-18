# python script to plot a table containing all benchmark models and their basic properties:
# number of state variables, number of reactions, number of parameters

import matplotlib.pyplot as plt
import pandas as pd
from averageTime import *


# important paths
tsv_path = '../Solver_Study/Data/Stat_Reac_Par/NEW_stat_reac_par_paper.tsv'

# load NEW_stat_reac_par_paper.tsv file containing all data needed after averaging
tsv_file = pd.read_csv(tsv_path, sep='\t')
tsv_file = averaging(tsv_file)

# adapt column names
old_names = tsv_file.columns
adapted_column_names = ['model_id', 'number_of_state_variables', 'number_of_reactions', 'number_of_parameters']
for iName in range(0, len(adapted_column_names)):
    tsv_file = tsv_file.rename(columns={old_names[iName]:adapted_column_names[iName]})

# Id names in better shape
data_in_better_shape = []
for iRow in range(0, len(tsv_file['model_id'])):
    _,adapted_id = tsv_file['model_id'][iRow].split('{')
    adapted_id,_ = adapted_id.split('}')
    tsv_file['model_id'][iRow] = adapted_id

# add column for classification
JWS = ['JWS'] * 26
BioModels = ['BioModels'] * (len(tsv_file['model_id']) - len(JWS))
list_of_databases = JWS + BioModels
tsv_file['taken_from_database'] = list_of_databases


# save new .tsv file to add to the supplement
tsv_file.to_csv('../paper_SolverSettings/Figures/Supplementary_ListOfAllModels.tsv', index=False, sep='\t')