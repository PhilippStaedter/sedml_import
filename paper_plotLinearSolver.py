# script to plot Scatter Plot and Box Plot for linear solver study

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from averageTime import *
from LinearRegression import *



left = 0.07
bottom = 0.1
width = 0.43
height = 0.85
row_factor = 0.47
column_factor = 0.22
rotation_factor = 90

ax1 = plt.axes([left, bottom, width, height])
ax2 = plt.axes([left + row_factor, bottom, width, height])

def LinearSolver(solAlg, nonLinSol):

    ######## subplot 1: linear regressions of combined scatter plots
    # list of all 35 data frames for better indexing in the future
    all_intern_columns_AMICI = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[])]

    all_intern_columns_LSODA = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                                pd.DataFrame(columns=[])]

    all_intern_columns = all_intern_columns_AMICI + all_intern_columns_LSODA
    column_names = []

    # important paths
    base_path = '../paper_SolverSettings/WholeStudy'
    base_path_LSODA = '../paper_SolverSettings/WholeStudy_LSODA'

    # choose only the correct files
    all_files_AMICI = sorted(os.listdir(base_path))
    all_files_COPASI = sorted(os.listdir(base_path_LSODA))
    all_files = all_files_AMICI + all_files_COPASI
    correct_files_AMICI = []
    correct_files_LSODA = []
    for iFile in range(0, len(all_files)):
        if all_files[iFile].split('_')[0] == solAlg and all_files[iFile].split('_')[1] == nonLinSol:
            correct_files_AMICI.append(all_files[iFile])
        elif all_files[iFile].split('_')[0] == '(1,2)':
            correct_files_LSODA.append(all_files[iFile])
    correct_files = correct_files_AMICI + correct_files_LSODA

    # open all .tsv linear solver files + save right column in data frame
    for iCorrectFile in range(0, len(correct_files)):  # each .tsv file

        # reset after each iteration
        next_time_value = []
        num_x = []

        if correct_files[iCorrectFile] in correct_files_AMICI:
            next_tsv = pd.read_csv(base_path + '/' + correct_files[iCorrectFile], sep='\t')

            # open next file
            next_tsv = averaging(next_tsv)

            # get the correct values
            for iFile in range(0, len(next_tsv['id'])):  # each file
                if next_tsv['t_intern_ms'][iFile] != 0:
                    next_time_value.append(next_tsv['t_intern_ms'][iFile])
                    num_x.append(next_tsv['state_variables'][iFile])

        elif correct_files[iCorrectFile] in correct_files_LSODA:
            next_tsv = pd.read_csv(base_path_LSODA + '/' + correct_files[iCorrectFile], sep='\t')

            # open next file
            next_tsv = averaging(next_tsv)

            # get the correct values
            for iFile in range(0, len(next_tsv['id'])):  # each file
                if next_tsv['t_intern_ms'][iFile] != 0:
                    next_time_value.append(next_tsv['t_intern_ms'][iFile] * 1000)
                    num_x.append(next_tsv['state_variables'][iFile])

        # append new column to existing data frame with correct log10 values
        column_names.append('simulation_time')
        all_intern_columns[iCorrectFile]['state_variables'] = pd.Series(num_x)
        all_intern_columns[iCorrectFile]['simulation_time'] = pd.Series(next_time_value)

    # plot scatter plot of all data points for the accompynying linear solver + linear regressions
    fontsize = 12
    labelsize = 8
    alpha = 0.5
    marker_size = 2
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim([0.8, 2000])
    ax1.set_ylim([0.1, 100000])
    ax1.set_xlabel('Number of state variables', fontsize=fontsize)
    ax1.set_ylabel('Simulation time [ms]', fontsize=fontsize)
    ax1.tick_params(labelsize=labelsize)

    # create five custom color maps

    # calculate point density

    # sort points by density

    linSol_for_Legend = ['DENSE', 'GMRES', 'BICGSTAB', 'TFQMR', 'KLU', 'LSODA']
    colors = ['#d73027', '#fc8d59', '#fee090', '#91bfdb', '#4575b4', '#4c3340']
    for iLinearSolverDataPoints in range(0, int(len(correct_files)/7)):
        # concatenate Data Frames in categories of linear solver data points
        vertically_stacked_tsv = pd.concat([all_intern_columns[7*iLinearSolverDataPoints], all_intern_columns[7*iLinearSolverDataPoints + 1],
                                    all_intern_columns[7*iLinearSolverDataPoints + 2], all_intern_columns[7*iLinearSolverDataPoints + 3],
                                    all_intern_columns[7*iLinearSolverDataPoints + 4], all_intern_columns[7*iLinearSolverDataPoints + 5],
                                    all_intern_columns[7*iLinearSolverDataPoints + 6]], axis=0)
        vertically_stacked_tsv = vertically_stacked_tsv.reset_index(drop=True)

        # do a linear regression
        y_axis_interception, slope = linearRegression(vertically_stacked_tsv, 'state_variables', 'simulation_time')
        #y_axis_interceptions.append(y_axis_interception)
        #slopes.append(slope)

        # plot a scatter plot + linear regressions
        num_x = [np.log10(p) for p in vertically_stacked_tsv['state_variables']]
        data_simulation_time = [np.log10(q) for q in vertically_stacked_tsv['simulation_time']]
        data_regression = [l[0] for l in [10 ** k for k in [y_axis_interception + j for j in [slope * i for i in num_x]]]]
        exp_num_x = [10 ** m for m in list(num_x)]
        exp_simulation_time = [10 ** n for n in list(data_simulation_time)]
        ax1.scatter(exp_num_x, exp_simulation_time, s=marker_size, alpha=alpha, c=colors[iLinearSolverDataPoints])
        ax1.plot(exp_num_x, data_regression, c=colors[iLinearSolverDataPoints], label=linSol_for_Legend[iLinearSolverDataPoints] + ': slope = ' + str(np.round(slope[0], 4)))
        #print('y_axis_interception: ' + str(y_axis_interception))

    # plot a black dashed bisection line
    #ax1.plot(list(range(1, int(sorted(exp_num_x, reverse=True)[0]))), list(range(1, int(sorted(exp_num_x, reverse=True)[0]))),
    #         'k--', label='Bisection line: slope = 1')

    # plot legend
    ax1.legend(loc=1, fontsize=labelsize - 2, frameon=False)

    # make top and right boxlines invisible
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # plot text 'A'
    ax1.text(-0.13, 1, 'A', fontsize=labelsize + 5, transform=ax1.transAxes)


    ######## subplot 2: box plot over computation times
    first_set = []
    second_set = []
    third_set = []
    fourth_set = []
    fifth_set = []
    sixth_set = []
    seventh_set = []
    for iDataFrame in range(0, len(all_intern_columns)):
        if iDataFrame in [0, 7, 14, 21, 28, 35]:
            #first_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            first_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [1, 8, 15, 22, 29, 36]:
            #second_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            second_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [2, 9, 16, 23, 30, 37]:
            #third_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            third_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [3, 10, 17, 24, 31, 38]:
            #fourth_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            fourth_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [4, 11, 18, 25, 32, 39]:
            #fifth_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            fifth_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [5, 12, 19, 26, 33, 40]:
            #sixth_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            sixth_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
        elif iDataFrame in [6, 13, 20, 27, 34, 41]:
            #seventh_set.append([np.log10(x) for x in list(all_intern_columns[iDataFrame]['simulation_time'])])
            seventh_set.append([x for x in list(all_intern_columns[iDataFrame]['simulation_time'])])

    # get all elements in one list and add empty spaces to enhance clarity
    total_data = first_set + [[]] + second_set + [[]] + third_set + [[]] +  fourth_set + [[]] + fifth_set + [[]] + sixth_set + [[]] + seventh_set

    # plot boxplot
    bp = ax2.boxplot(total_data, sym='+', widths=0.5, patch_artist=True, positions=range(1, 49))

    # set more options
    ax2.set_yscale('log')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_ylim([0.1, 100000])
    #ax2.set_ylim([np.log10(0.2), 5])
    #ax2.set_yticklabels(['', r'$10^{0}$', r'$10^{1}$', r'$10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$'])

    # change colour for each set
    color1 = '#d73027'
    color2 = '#fc8d59'
    color3 = '#fee090'
    color4 = '#91bfdb'
    color5 = '#4575b4'
    color6 = '#4c3340'

    colors = [color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6, 'white',
              color1, color2, color3, color4, color5, color6]

    # for bplot in bp:
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=1)
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=1)
    for median in bp['medians']:
        median.set(color='black', linewidth=2)
    for flier in bp['fliers']:
        flier.set(marker='+', color='#e7298a', alpha=0.5, markersize=3)

    # ax2.set_title('Comparison of percentiles and median', fontsize=titlesize, fontweight='bold')
    #ax2.set_ylabel('Simulation time', fontsize=fontsize)
    ax2.tick_params(labelsize=labelsize)
    ax2.set_xticklabels([])
    ax2.set_xlim([0, 49])
    specific_xticks = ax2.xaxis.get_major_ticks()
    #for iTick in [0, 7, 14, 21, 28, 35]:
    #    specific_xticks[iTick].set_visible(False)

    # create major and minor ticklabels
    Abs_xTickLabels = ['', '', '', r'$10^{-6}$', '', '', '',
                       '', '', '', r'$10^{-8}$', '', '', '',
                       '', '', '', r'$10^{-8}$', '', '', '',
                       '', '', '', r'$10^{-10}$', '', '', '',
                       '', '', '', r'$10^{-12}$', '', '', '',
                       '', '', '', r'$10^{-14}$', '', '', '',
                       '', '', '', r'$10^{-16}$', '', '', '']
    Rel_xTickLabels = ['', '', '', r'$10^{-8}$', '', '', '',
                       '', '', '', r'$10^{-6}$', '', '', '',
                       '', '', '', r'$10^{-16}$', '', '', '',
                       '', '', '', r'$10^{-12}$', '', '', '',
                       '', '', '', r'$10^{-10}$', '', '', '',
                       '', '', '', r'$10^{-14}$', '', '', '',
                       '', '', '', r'$10^{-8}$', '', '', '']

    ax2.set_xticks(list(range(49)))
    minor_list_1 = [x + 0.001 for x in list(range(49))]
    ax2.set_xticks(minor_list_1, minor=True)
    ax2.set_xticklabels(Abs_xTickLabels, fontsize=labelsize)
    ax2.set_xticklabels(Rel_xTickLabels, minor=True, fontsize=labelsize)
    ax2.tick_params(axis='x', which='major', pad=5)
    ax2.tick_params(axis='x', which='minor', pad=20)
    ax2.text(-0.1, -0.05, 'Abs. tol.: ', fontsize=labelsize, transform=ax2.transAxes)
    ax2.text(-0.1, -0.10, 'Rel. tol.: ', fontsize=labelsize, transform=ax2.transAxes)
    specific_xticks_major = ax2.xaxis.get_major_ticks()
    for iTick in range(1, 49):
        specific_xticks_major[iTick].set_visible(False)
    for iTick in [3, 10, 17, 24, 31, 38, 45]:
        specific_xticks_major[iTick].set_visible(True)
    specific_xticks_minor = ax2.xaxis.get_minor_ticks()
    for iTick in range(1, 49):
        specific_xticks_minor[iTick].set_visible(False)
    for iTick in [3, 10, 17, 24, 31, 38, 45]:
        specific_xticks_minor[iTick].set_visible(True)

    # add grit
    #ax2.yaxis.grid(True, linestyle='-', which='both', color='lightgrey', alpha=0.25)

    # plot text 'B'
    ax2.text(-0.13, 1, 'B', fontsize=labelsize + 5, transform=ax2.transAxes)




########## call both functions + some global properties
LinearSolver('2','2')

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
# plt.savefig('../paper_SolverSettings/Figures/Study_3/13012020/LinSol_' + solAlg + '_' + nonLinSol + '_Scatter.pdf')

# show figure
plt.show()
