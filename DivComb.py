# script to devide the solver combinations into eight columns

import pandas as pd
import numpy as np


# important paths
tsv_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data_0_1_updated.tsv'
save_path = '../bachelor_thesis/SolverAlgorithm/Input_Output_Data_0_1_updated_divided.tsv'

# load data frame
tsv_file = pd.read_csv(tsv_path, sep='\t')

######### change 'combinations' column into eight different ones #########
combinations = tsv_file['combinations']

# new columns + reindex
tsv_file['Adams'] = pd.Series()
tsv_file['BDF'] = pd.Series()
tsv_file['DENSE'] = pd.Series()
tsv_file['GMRES'] = pd.Series()
tsv_file['BicGStab'] = pd.Series()
tsv_file['SPTFQMR'] = pd.Series()
tsv_file['KLU'] = pd.Series()
tsv_file['Abs_Tol'] = pd.Series()
tsv_file['Rel_Tol'] = pd.Series()
headers = list(tsv_file.columns)
headers.remove('value')
headers.append('value')
tsv_file = tsv_file.reindex(columns=headers)

for iElement in range(0, len(combinations)):
    algorithm, rest1 = combinations[iElement].split('_',1)
    linear_solver, rest2 = rest1.split('_',1)
    abs_tol, rel_tol = rest2.split('_',1)

    # solver algorithm
    if algorithm == str(1):
        tsv_file['Adams'][iElement] = 1
        tsv_file['BDF'][iElement] = 0
    elif algorithm == str(2):
        tsv_file['Adams'][iElement] = 0
        tsv_file['BDF'][iElement] = 1

    # linear solver
    if linear_solver == str(1):
        tsv_file['DENSE'][iElement] = 1
        tsv_file['GMRES'][iElement] = 0
        tsv_file['BicGStab'][iElement] = 0
        tsv_file['SPTFQMR'][iElement] = 0
        tsv_file['KLU'][iElement] = 0
    elif linear_solver == str(6):
        tsv_file['DENSE'][iElement] = 0
        tsv_file['GMRES'][iElement] = 1
        tsv_file['BicGStab'][iElement] = 0
        tsv_file['SPTFQMR'][iElement] = 0
        tsv_file['KLU'][iElement] = 0
    elif linear_solver == str(7):
        tsv_file['DENSE'][iElement] = 0
        tsv_file['GMRES'][iElement] = 0
        tsv_file['BicGStab'][iElement] = 1
        tsv_file['SPTFQMR'][iElement] = 0
        tsv_file['KLU'][iElement] = 0
    elif linear_solver == str(8):
        tsv_file['DENSE'][iElement] = 0
        tsv_file['GMRES'][iElement] = 0
        tsv_file['BicGStab'][iElement] = 0
        tsv_file['SPTFQMR'][iElement] = 1
        tsv_file['KLU'][iElement] = 0
    elif linear_solver == str(9):
        tsv_file['DENSE'][iElement] = 0
        tsv_file['GMRES'][iElement] = 0
        tsv_file['BicGStab'][iElement] = 0
        tsv_file['SPTFQMR'][iElement] = 0
        tsv_file['KLU'][iElement] = 1

    # tolerance
    tsv_file['Abs_Tol'][iElement] = int(abs_tol)
    tsv_file['Rel_Tol'][iElement] = int(rel_tol)

    print(iElement)

# delete old column
tsv_file = tsv_file.drop('combinations', axis=1)

# save new data frame
tsv_file.to_csv(save_path, sep='\t', index=False)

