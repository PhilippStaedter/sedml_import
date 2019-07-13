# script to plot a scatter plot for study 3

import os
import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *
from averageTime import *

# important paths
tolerance_path = '../bachelor_thesis/SolverAlgorithm/BDF'

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

# open all .tsv linear solver files + save right column in data frame
linSol_files = sorted(os.listdir(tolerance_path))
for iLinSol in range(0, len(linSol_files)):                                                                             # each .tsv file
    next_tsv = pd.read_csv(tolerance_path + '/' + linSol_files[iLinSol], sep='\t')

    # change .tsv-id form e.g. 1_06_10.tsv to 06_10
    new_lin_sol = linSol_files[iLinSol].split('.')[0]

    # reset after each iteration
    next_time_value = []
    num_x = []

############## calculate average values of certain models ####################
    next_tsv = averaging(next_tsv)

##############################################################################

    for iFile in range(0, len(next_tsv['id'])):                                                                         # each file
        if next_tsv['t_intern_ms'][iFile] != 0:
            next_time_value.append(next_tsv['t_intern_ms'][iFile])
            num_x.append(next_tsv['state_variables'][iFile])

    # append new column to existing data frame with correct values
    column_names.append(str(new_lin_sol))
    all_intern_columns[iLinSol]['state_variables'] = pd.Series(num_x)
    all_intern_columns[iLinSol][str(new_lin_sol)] = pd.Series(next_time_value)


# plot a customized scatter plot
left = 0.1
bottom = 0.5
width = 0.4
height = 0.33
row_factor = 0.44
column_factor = 0.41
rotation_factor = 70

for iCounter in range(0, int(len(linSol_files)/4)):

    # for ylim control
    if sorted(all_intern_columns[4*iCounter][column_names[4*iCounter]])[0] < 0.1 or sorted(all_intern_columns[4*iCounter + 1][column_names[4*iCounter + 1]])[0] < 0.1 or \
            sorted(all_intern_columns[4*iCounter + 2][column_names[4*iCounter + 2]])[0] < 0.1 or sorted(all_intern_columns[4*iCounter + 2][column_names[4*iCounter + 2]])[0] < 0.1:
        print('Need smaller ylim')

    # first plot
    if iCounter == 0:
        ax1 = plt.axes([left, bottom, width, height])
        ax1.text(0.35, 1.05, 'linsol = DENSE', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.get_xaxis().set_visible(False)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

    elif iCounter == 1:
        ax1 = plt.axes([left + iCounter * row_factor, bottom, width, height])
        ax1.text(0.35, 1.05, 'linsol = BICGSTAB', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)

    elif iCounter == 2:
        ax1 = plt.axes([left, bottom - (iCounter-1) * column_factor, width, height])
        ax1.text(0.35, 1.05, 'linsol = SPTFQMR', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

    elif iCounter == 3:
        ax1 = plt.axes([left + (iCounter-2) * row_factor, bottom - (iCounter-2) * column_factor, width, height])
        ax1.text(0.35, 1.05, 'linsol = KLU', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.get_yaxis().set_visible(False)
        ax1.text(-0.5, -0.2, 'Number of state variables', fontsize=24, transform=ax1.transAxes)

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

    # change .tsv-id form e.g. 1_06_10.tsv to 06_10
    linSol4legend_1 = column_names[4*iCounter].split('_',1)[1]
    linSol4legend_2 = column_names[4*iCounter + 1].split('_',1)[1]
    linSol4legend_3 = column_names[4*iCounter + 2].split('_',1)[1]
    linSol4legend_4 = column_names[4*iCounter + 3].split('_',1)[1]

    # scatter plot
    ax1.set_xlim([0.5, 1500])
    ax1.set_ylim([0.1, 50000])
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.scatter(first_x, first_data, alpha=0.8, c='blue', edgecolors='none', s=30, label=str(linSol4legend_1))
    ax1.scatter(second_x, second_data, alpha=0.8, c='red', edgecolors='none', s=30, label=str(linSol4legend_2))
    ax1.scatter(third_x, third_data, alpha=0.8, c='yellow', edgecolors='none', s=30, label=str(linSol4legend_3))
    ax1.scatter(fourth_x, fourth_data, alpha=0.8, c='green', edgecolors='none', s=30, label=str(linSol4legend_4))

    # plot two legends
    leg1 = ax1.legend(loc=2)
    leg2 = ax1.legend([str(round(len(all_intern_columns[iCounter]['state_variables'])*100/166,2)) + ' %',
                       str(round(len(all_intern_columns[iCounter + 1]['state_variables'])*100/166,2)) + ' %',
                       str(round(len(all_intern_columns[iCounter + 2]['state_variables'])*100/166,2)) + ' %',
                       str(round(len(all_intern_columns[iCounter + 3]['state_variables'])*100/166,2)) + ' %'], loc=4)
    ax1.add_artist(leg1)

# set global labels
plt.text(-0.9, 2.5, 'Simulation time distribution of models for the BDF Method', fontsize=24, transform=ax1.transAxes)  # -60 , 350

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../sbml2amici/Figures/zzz_Figures_new/SolAlg_Scatter_BDF.pdf')

# show figure
plt.show()