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
#adapted_column_names = ['model_id', 'model_id', 'model_id', 'model_id', 'model_id', 'model_id', 'model_id']
data_in_correct_shape = []
for iRow in range(0, 24):
    intermediate = []
    for iColumn in range(0, 7):
        if iRow == 23 and iColumn == 6:
            intermediate.append('')
        else:
            _,adapted_id = tsv_file['id'][iRow + 24*iColumn].split('{',1)
            adapted_id,_ = adapted_id.split('}',1)
            intermediate.append(adapted_id)
    data_in_correct_shape.append(intermediate)


# transfer data into plt.table()
ax = plt.axes([0.03,0.02,0.96,0.97])
fontsize = 60
table = plt.table(data_in_correct_shape, cellLoc='center', colLoc='center', loc=0, fontsize=fontsize)
plt.axis('off')
ax.add_table(table)

# adjust table properties
props = table.properties()
for cell in props['children']:
    cell.set_height(0.04)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
# plt.savefig('../paper_SolverSettings/Figures/Study_3/13012020/LinSol_' + solAlg + '_' + nonLinSol + '_Scatter.pdf')

# show figure
plt.show()