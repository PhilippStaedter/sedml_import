# scrip to plot a bar plot to investigate the difference for the Multistep Method - study 5

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *
from matplotlib import ticker


def Multistep():

    # important paths
    base_path = '../paper_SolverSettings/WholeStudy'

    # list of all data frames for nonLinSol == 1 for better indexing in the future
    all_intern_columns_1 = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[])]

    # list of all data frames for nonLinSol == 2 for better indexing in the future
    all_intern_columns_2 = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                          pd.DataFrame(columns=[]), pd.DataFrame(columns=[])]

    all_intern_columns = [all_intern_columns_1, all_intern_columns_2]
    column_names = []

    # choose only the correct files
    all_files = sorted(os.listdir(base_path))
    correct_files_1 = []
    correct_files_2 = []
    for iFile in range(0, len(all_files)):
        if all_files[iFile].split('_')[0] == '1':
            correct_files_1.append(all_files[iFile])
        elif all_files[iFile].split('_')[0] == '2':
            correct_files_2.append(all_files[iFile])
    correct_files = [correct_files_1, correct_files_2]

    # open all .tsv linear solver files + save right column in data frame
    for iNonLinSol in range(0, len(correct_files)):
        for iCorrectFile in range(0, len(correct_files_1)):  # each .tsv file
            next_tsv = pd.read_csv(base_path + '/' + correct_files[iNonLinSol][iCorrectFile], sep='\t')

            # change .tsv-id form e.g. 1_06_10.tsv to 06_10
            new_name = correct_files[iNonLinSol][iCorrectFile].split('.')[0].split('_')[3] + '_' + \
                       correct_files[iNonLinSol][iCorrectFile].split('.')[0].split('_')[4]

            # reset after each iteration
            next_time_value = []
            num_x = []

            # open next file
            next_tsv = averaging(next_tsv)

            # get the correct values
            for iFile in range(0, len(next_tsv['id'])):  # each file
                if next_tsv['t_intern_ms'][iFile] != 0:
                    next_time_value.append(next_tsv['t_intern_ms'][iFile])
                    num_x.append(next_tsv['state_variables'][iFile])

            # append new column to existing data frame with correct values
            column_names.append(str(new_name))
            all_intern_columns[iNonLinSol][iCorrectFile]['state_variables'] = pd.Series(num_x)
            all_intern_columns[iNonLinSol][iCorrectFile][str(new_name)] = pd.Series(next_time_value)

    # length of the last file
    file_length = len(next_tsv['id'])

    # get correct data for all five linear solvers in one of the seven figures
    # plot a customized scatter plot
    fontsize = 22 - 12 + 4
    labelsize = 10 + 4
    titlesize = 30 - 8

    rotation = 90
    left = 0.12
    bottom = 0.6
    width = 0.8
    height = 0.25
    row_factor = 0.45
    column_factor = 0.15
    rotation_factor = 70
    alpha = 1

    bar_width = 0.35

    # plot two bar plots
    figure = plt.figure()
    ax1 = figure.add_axes([left, bottom, width, height])
    ax2 = figure.add_axes([left, bottom - height - column_factor, width, height])
    index = np.arange(35)


    # just for a legend
    adams_data_2 = all_intern_columns_1[int(len(correct_files_1)/2)][column_names[int(len(correct_files_1)/2)]]
    bdf_data_2 = all_intern_columns_2[int(len(correct_files_1)/2)][column_names[int(len(correct_files_1)/2)]]
    nonLinSol12 = ax2.bar(index[int(len(correct_files_1)/2) - int(len(correct_files_1) / 2)], round(len(adams_data_2) / file_length, 2), bar_width, alpha=alpha, color='orange', label='Adams')
    nonLinSol22 = ax2.bar(index[int(len(correct_files_1)/2) - int(len(correct_files_1) / 2)] + bar_width, round(len(bdf_data_2) / file_length, 2), bar_width, alpha=alpha, color='blue', label='BDF')

    for iBarPlot in range(0, int(len(correct_files_1)/2)):
        adams_data_1 = all_intern_columns_1[iBarPlot][column_names[iBarPlot]]
        bdf_data_1 = all_intern_columns_2[iBarPlot][column_names[iBarPlot]]
        nonLinSol11 = ax1.bar(index[iBarPlot], round(len(adams_data_1)/file_length,2) , bar_width, alpha=alpha, color='orange')
        nonLinSol21 = ax1.bar(index[iBarPlot] + bar_width, round(len(bdf_data_1)/file_length,2), bar_width, alpha = alpha, color = 'blue')

    for iBarPlot in range(int(len(correct_files_1)/2) + 1, len(correct_files_1)):
        adams_data_2 = all_intern_columns_1[iBarPlot][column_names[iBarPlot]]
        bdf_data_2 = all_intern_columns_2[iBarPlot][column_names[iBarPlot]]
        nonLinSol12 = ax2.bar(index[iBarPlot - int(len(correct_files_1)/2)], round(len(adams_data_2)/file_length,2) , bar_width, alpha=alpha, color='orange')
        nonLinSol22 = ax2.bar(index[iBarPlot - int(len(correct_files_1)/2)] + bar_width, round(len(bdf_data_2)/file_length,2), bar_width, alpha = alpha, color = 'blue')

    ax1.set_title('Non-Linear Solver: Functional', fontsize=titlesize)
    ax1.set_ylabel('Success Rate [%]', fontsize=titlesize)
    ax2.set_title('Non-Linear Solver: Newton-type', fontsize=titlesize)
    ax2.set_ylabel('Success Rate [%]', fontsize=titlesize)
    ax1.set_ylim([0.7, 1])
    ax2.set_ylim([0.7, 1])
    #ax1.set_xticklabels(['D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K',
    #                     'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K'])
    #ax2.set_xticklabels(['D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K',
    #                     'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K'])
    ax1.minorticks_on()
    ax2.minorticks_on()
    lower_labels = [r'$10^{-6}$' + ',' + r'$10^{-8}$', '' '', '', '',
                       r'$10^{-8}$' + ',' + r'$10^{-6}$', '', '', '', '',
                       r'$10^{-8}$' + ',' + r'$10^{-16}$', '', '', '', '',
                       r'$10^{-10}$' + ',' + r'$10^{-12}$', '', '', '', '',
                       r'$10^{-12}$' + ',' + r'$10^{-10}$', '', '', '', '',
                       r'$10^{-14}$' + ',' + r'$10^{-14}$', '', '', '', '',
                       r'$10^{-16}$' + ',' + r'$10^{-8}$']
    upper_labels = ['D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K',
                      'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K', 'D', 'G', 'B', 'T', 'K']
    upper_1 = plt.setp(ax1, xticklabels=lower_labels)
    upper_2 = plt.setp(ax2, xticklabels=lower_labels)
    ax1.xaxis.set_minor_formatter(ticker.FixedFormatter(upper_labels))
    ax2.xaxis.set_minor_formatter(ticker.FixedFormatter(upper_labels))
    plt.setp(ax1.xaxis.get_minorticklabels(), fontsize=labelsize, fontweight='bold')
    plt.setp(ax2.xaxis.get_minorticklabels(), fontsize=labelsize, fontweight='bold')
    ax1.tick_params(axis='x', which='major', pad=40)
    ax2.tick_params(axis='x', which='major', pad=40)
    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)
    plt.setp(upper_1, fontsize=fontsize, fontweight='bold')
    plt.setp(upper_2, fontsize=fontsize, fontweight='bold')
    plt.tick_params(labelsize=labelsize)
    #plt.title('Scores by person')
    #plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
    ax2.legend(loc=2)

    # set global labels
    plt.text(0.3, 3, 'Adams vs BDF - Success Rate', fontsize=titlesize, fontweight='bold', transform=ax2.transAxes)

    # better layout
    plt.tight_layout()

    # change plotting size
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    # save figure
    plt.savefig('../paper_SolverSettings/Figures/Study_5/SolAlg.pdf')

    # show figure
    plt.show()

# call functions
Multistep()