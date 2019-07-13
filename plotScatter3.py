# script to plot a scatter plot for study 3

import os
import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *
from averageTime import *

# important paths
tolerance_path_1 = '../bachelor_thesis/SolverAlgorithm/Adams'
tolerance_path_2 = '../bachelor_thesis/SolverAlgorithm/BDF'

####################### Adams ####################################
# list of all data frames for better indexing in the future
all_intern_columns_1 = pd.DataFrame(columns=[], data=[])

column_names_1 = []

# open all .tsv linear solver files + save right column in data frame
SolAlg_files_1 = sorted(os.listdir(tolerance_path_1))
for iLinSol in range(0, len(SolAlg_files_1)):                                                                             # each .tsv file

    # new/reset data frame
    new_df_1 = pd.DataFrame(columns=[], data=[])

    # open next .tsv file
    next_tsv = pd.read_csv(tolerance_path_1 + '/' + SolAlg_files_1[iLinSol], sep='\t')

    # change .tsv-id form e.g. 1_06_10.tsv to 06_10
    #new_lin_sol = linSol_files[iLinSol].split('.')[0]
    times = 't_intern_ms_Adams'

    # reset after each iteration
    next_time_value = []
    num_x = []

    # calculate average values of certain models
    next_tsv = averaging(next_tsv)

    for iFile in range(0, len(next_tsv['id'])):                                                                         # each file
        if next_tsv['t_intern_ms'][iFile] != 0:
            next_time_value.append(next_tsv['t_intern_ms'][iFile])
            num_x.append(next_tsv['state_variables'][iFile])

    # append new column to existing data frame with correct values
    column_names_1.append(times)
    new_df_1['state_variables'] = pd.Series(num_x)
    new_df_1[times] = pd.Series(next_time_value)

    # concatenate data frames
    all_intern_columns_1 = all_intern_columns_1.append(new_df_1, ignore_index=True)

################################ BDF ###################################################
# list of all data frames for better indexing in the future
all_intern_columns_2 = pd.DataFrame(columns=[], data=[])

column_names_2 = []

# open all .tsv linear solver files + save right column in data frame
SolAlg_files_2 = sorted(os.listdir(tolerance_path_2))
for iLinSol in range(0, len(SolAlg_files_2)):                                                                             # each .tsv file

    # new/reset data frame
    new_df_2 = pd.DataFrame(columns=[], data=[])

    # open new .tsv file
    next_tsv = pd.read_csv(tolerance_path_2 + '/' + SolAlg_files_2[iLinSol], sep='\t')

    # change .tsv-id form e.g. 1_06_10.tsv to 06_10
    #new_lin_sol = linSol_files[iLinSol].split('.')[0]
    times = 't_intern_ms_BDF'

    # reset after each iteration
    next_time_value = []
    num_x = []

    # calculate average values of certain models
    next_tsv = averaging(next_tsv)

    for iFile in range(0, len(next_tsv['id'])):                                                                         # each file
        if next_tsv['t_intern_ms'][iFile] != 0:
            next_time_value.append(next_tsv['t_intern_ms'][iFile])
            num_x.append(next_tsv['state_variables'][iFile])

    # append new column to existing data frame with correct values
    column_names_2.append(times)
    new_df_2['state_variables'] = pd.Series(num_x)
    new_df_2[times] = pd.Series(next_time_value)

    # concatenate data frames
    all_intern_columns_2 = all_intern_columns_2.append(new_df_2, ignore_index=True)


################################# simulate data ##########################################
# plot a customized scatter plot
left = 0.1
bottom = 0.5
width = 0.4
height = 0.33
row_factor = 0.44
column_factor = 0.41
rotation_factor = 70

for iCounter in range(0, 3):

    # for ylim control
    if sorted(all_intern_columns_1[column_names_1[iCounter]])[0] < 0.1 or sorted(all_intern_columns_1[column_names_1[iCounter]])[0] > 50000 or \
       sorted(all_intern_columns_2[column_names_2[iCounter]])[0] < 0.1 or sorted(all_intern_columns_2[column_names_2[iCounter]])[0] > 50000:
        print('Need smaller or bigger ylim: ' + sorted(all_intern_columns_1[column_names_1[iCounter]])[0] + ' / ' + column_names_1[iCounter])

    # first plot
    if iCounter == 0:
        ax1 = plt.axes([left, bottom, width, height])
        ax1.text(0.35, 1.05, 'SolAlg = Adams', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.tick_params(labelbottom=False)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

        # get correct data in one of the two figures
        # num_x
        first_x = all_intern_columns_1['state_variables']

        # data
        first_data = all_intern_columns_1[column_names_1[0]]

        # change .tsv-id form e.g. 1_06_10.tsv to 06_10
        SolAlgLegend_1 = 'Only Adams'

        # scatter plot
        ax1.set_xlim([0.5, 1500])
        ax1.set_ylim([0.1, 50000])
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.scatter(first_x, first_data, alpha=0.8, c='red', edgecolors='none', s=30, label=SolAlgLegend_1)

        # plot two legends
        leg1 = ax1.legend(loc=2)
        leg2 = ax1.legend([str(round(len(all_intern_columns_1['state_variables']) * 100 / (166 * 16), 2)) + ' %'], loc=4)
        ax1.add_artist(leg1)

    elif iCounter == 1:
        ax1 = plt.axes([left, bottom - iCounter * column_factor, width, height])
        ax1.text(0.35, 1.05, 'SolAlg = BDF', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.text(0.25, -0.15, 'Number of state variables', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

        # get correct data in one of the two figures
        # num_x
        second_x = all_intern_columns_2['state_variables']

        # data
        second_data = all_intern_columns_2[column_names_2[0]]

        # change .tsv-id form e.g. 1_06_10.tsv to 06_10
        SolAlgLegend_2 = 'Only BDF'

        # scatter plot
        ax1.set_xlim([0.5, 1500])
        ax1.set_ylim([0.1, 50000])
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.scatter(second_x, second_data, alpha=0.8, c='blue', edgecolors='none', s=30, label=SolAlgLegend_2)

        # plot two legends
        leg1 = ax1.legend(loc=2)
        leg2 = ax1.legend([str(round(len(all_intern_columns_1['state_variables']) * 100 / (166 * 16), 2)) + ' %'], loc=4)
        ax1.add_artist(leg1)

    elif iCounter == 2:
        ax1 = plt.axes([left + iCounter * row_factor/1.8, bottom - iCounter * column_factor/2.2, width, height * 2.1])
        ax1.text(0.3, 1.05, 'Difference = Adams - BDF', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        ax1.text(-0.12, 0.65, 'Time difference [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)
        ax1.text(0.3, -0.1, 'Number of state variables', fontsize=14, fontweight='bold', transform=ax1.transAxes)

        # percental deviation
        time_difference = []
        for iTime in range(0, len(all_intern_columns_1[column_names_1[0]])):
            time_difference.append(all_intern_columns_1[column_names_1[0]][iTime] - all_intern_columns_2[column_names_2[0]][iTime])

        # change .tsv-id form e.g. 1_06_10.tsv to 06_10
        SolAlgLegend_3 = 'Time Difference'

        # scatter plot
        ax1.set_xscale('log')
        #ax1.set_yscale('log')
        ax1.set_xlim([0.5, 1500])
        #ax1.set_ylim([0.0005, 50000])
        ax1.set_yscale('symlog')
        ax1.set_ylim([-100000, 100000])
        ax1.scatter(first_x, time_difference, alpha=0.8, c='green', edgecolors='none', s=30, label=SolAlgLegend_3)
        ax1.hlines(0, 0.5, 1500, 'red', 'dashed')

        # plot legend
        leg1 = ax1.legend(loc=2)

# set global labels
plt.text(-0.8, 1.15, 'Simulation time distribution of models for the BDF Method', fontsize=24, transform=ax1.transAxes)  # -60 , 350

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../sbml2amici/Figures/zzz_Figures_new/SolAlg_Scatter.pdf')

# show figure
plt.show()