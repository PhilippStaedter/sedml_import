# script to plot a scatter plot for study 3

import os
import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *

# important paths
tolerance_path = '../bachelor_thesis/LinearSolver'

# list of all data frames for better indexing in the future
all_intern_columns = [pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[]),
                      pd.DataFrame(columns=[])]


column_names = []

# open all .tsv linera solver files + save rigth column in data frame
linSol_files = sorted(os.listdir(tolerance_path))
for iLinSol in range(0, len(linSol_files)):                                                                             # each .tsv file
    next_tsv = pd.read_csv(tolerance_path + '/' + linSol_files[iLinSol], sep='\t')

    # reset after each iteration
    next_time_value = []
    num_x = []

    for iFile in range(0, len(next_tsv['id'])):                                                                         # each file
        if next_tsv['t_intern_ms'][iFile] != 0:
            next_time_value.append(next_tsv['t_intern_ms'][iFile])
            num_x.append(next_tsv['state_variables'][iFile])

    # append new column to existing data frame with correct values
    column_names.append(str(linSol_files[iLinSol]))
    all_intern_columns[iLinSol]['state_variables'] = pd.Series(num_x)
    all_intern_columns[iLinSol][str(linSol_files[iLinSol])] = pd.Series(next_time_value)


# plot a customized scatter plot
left = 0.12
bottom = 0.65
width = 0.38
height = 0.2
row_factor = 0.42
column_factor = 0.3
rotation_factor = 70

for iCounter in range(0, int(len(linSol_files)/4)):

    # first plot
    if iCounter == 0:
        ax1 = plt.axes([left, bottom, width, height])
        # ax1.get_xaxis().set_visible(False)
        ax1.text(0.3, 1.1, 'linsol = DENSE', fontsize=14, fontweight='bold', transform=ax1.transAxes)

    elif iCounter == 1:
        ax1 = plt.axes([left + iCounter * row_factor, bottom, width, height])
        ax1.text(0.3, 1.1, 'linsol = GMRES', fontsize=14, fontweight='bold', transform=ax1.transAxes)

    elif iCounter == 2:
        ax1 = plt.axes([left, bottom - (iCounter-1) * column_factor, width, height])
        ax1.text(0.3, 1.1, 'linsol = BICGSTAB', fontsize=14, fontweight='bold', transform=ax1.transAxes)

    elif iCounter == 3:
        ax1 = plt.axes([left + (iCounter-2) * row_factor, bottom - (iCounter-2) * column_factor, width, height])
        ax1.text(0.3, 1.1, 'linsol = SPTFQMR', fontsize=14, fontweight='bold', transform=ax1.transAxes)

    elif iCounter == 4:
        ax1 = plt.axes([left, bottom - (iCounter-2) * column_factor, width, height])
        ax1.text(0.3, 1.1, 'linsol = KLU', fontsize=14, fontweight='bold', transform=ax1.transAxes)


    # get correct data for all four plots in one of the five figures
    # apply formula:   iCounter --> 4*iCounter
    # num_x
    first_x = all_intern_columns[4*iCounter]['state_variables']
    second_x = all_intern_columns[4*iCounter + 1]['state_variables']
    third_x = all_intern_columns[4*iCounter + 2]['state_variables']
    fourth_x = all_intern_columns[4*iCounter + 3]['state_variables']
    # data
    first_data = all_intern_columns[4*iCounter][column_names[4*iCounter]]
    second_data = all_intern_columns[4*iCounter + 1][column_names[4*iCounter + 1]]
    third_data = all_intern_columns[4*iCounter + 2][column_names[4*iCounter + 2]]
    fourth_data = all_intern_columns[4*iCounter + 3][column_names[4*iCounter + 3]]


    ax1.scatter(first_x, first_data, alpha=0.8, c='blue', edgecolors='none', s=30, label=str(column_names[iCounter]))
    ax1.scatter(second_x, second_data, alpha=0.8, c='red', edgecolors='none', s=30, label=str(column_names[iCounter + 1]))
    ax1.scatter(third_x, third_data, alpha=0.8, c='yellow', edgecolors='none', s=30, label=str(column_names[iCounter + 2]))
    ax1.scatter(fourth_x, fourth_data, alpha=0.8, c='green', edgecolors='none', s=30, label=str(column_names[iCounter + 3]))


# better layout
plt.tight_layout()

# save figure
# plt.savefig('../sbml2amici/Figures/zzz_Figures_new/LinSol_Scatter.png')

# show figure
plt.show()