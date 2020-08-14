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
adapted_column_names = ['model_id', 'number of state variables', 'number of reactions', 'number of parameters']
data_in_correct_shape = []
for iRow in range(0, len(tsv_file.id)):
    intermediate = []
    for iColumn in range(0, len(tsv_file.columns)):
        intermediate.append(tsv_file[tsv_file.columns[iColumn]][iRow])
    data_in_correct_shape.append(intermediate)


# transfer data into plt.table()
fontsize = 30
plt.table(data_in_correct_shape, cellLoc='center', colLabels=adapted_column_names, colLoc='center', loc=0, fontsize=fontsize)
plt.axis('off')

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
# plt.savefig('../paper_SolverSettings/Figures/Study_3/13012020/LinSol_' + solAlg + '_' + nonLinSol + '_Scatter.pdf')

# show figure
plt.show()