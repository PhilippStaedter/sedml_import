# histogram plot to plot the nonlinear solvers

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *

def NonLinSOl():

    # important path
    base_path = '../paper_SolverSettings/WholeStudy'

    # list of all data frames for nonLinSol == 1 for better indexing in the future
    all_intern_columns_1 = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[])]

    # list of all data frames for nonLinSol == 2 for better indexing in the future
    all_intern_columns_2 = [pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[]), pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]),
                            pd.DataFrame(columns=[]), pd.DataFrame(columns=[])]

    all_intern_columns = [all_intern_columns_1, all_intern_columns_2]
    column_names = []

    # choose only the correct files
    all_files = sorted(os.listdir(base_path))
    correct_files_1 = []
    correct_files_2 = []
    for iFile in range(0, len(all_files)):
        if all_files[iFile].split('_')[1] == '1':
            correct_files_1.append(all_files[iFile])
        elif all_files[iFile].split('_')[1] == '2':
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

    # get correct data for both non-linear solvers for the histogram
    # plot a customized histogram plot
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

    # initialise two histogram plots
    figure = plt.figure()
    ax1 = figure.add_axes([left, bottom, width, height])
    ax2 = figure.add_axes([left, bottom - height - column_factor, width, height])

    # get all data between 0 and 1
    functional_data_1 = []
    newton_data_1 = []
    for iHistogram in range(0, int(len(correct_files_1) / 2)):
        functional_data_1.append(round(len(all_intern_columns_1[iHistogram][column_names[iHistogram]])/file_length, 2))
        newton_data_1.append(round(len(all_intern_columns_2[iHistogram][column_names[iHistogram]])/file_length, 2))

    functional_data_2 = []
    newton_data_2 = []
    for iHistogram in range(int(len(correct_files_1) / 2) + 1, len(correct_files_1)):
        functional_data_2.append(round(len(all_intern_columns_1[iHistogram][column_names[iHistogram]])/file_length, 2))
        newton_data_2.append(round(len(all_intern_columns_2[iHistogram][column_names[iHistogram]])/file_length, 2))

    # plot two (times two) histograms
    adams1 = ax1.hist(functional_data_1, bins=50, range=(0.7, 1), color='orange', label='Functional', alpha=0.5)
    bdf1 = ax1.hist(newton_data_1, bins=50, range=(0.7, 1), color='blue', label='Newton-type', alpha=0.5)
    adams2 = ax2.hist(functional_data_2, bins=50, range=(0.7, 1), color='orange', alpha=0.5)
    bdf2 = ax2.hist(newton_data_2, bins=50, range=(0.7, 1), color='blue', alpha=0.5)                                               # density=True,

    # further settings
    ax1.set_xlabel('Success rate')
    ax2.set_xlabel('Success rate')
    ax1.set_ylabel('Absolute amount of models')
    ax2.set_ylabel('Absolute amount of models')
    #ax1.set_xlim([0,1])
    #ax2.set_xlim([0,1])
    ax1.legend()

    # set global labels
    plt.text(0.3, 3, 'Functionsl vs Newton-type - Success Rate', fontsize=titlesize, fontweight='bold', transform=ax2.transAxes)

    # better layout
    plt.tight_layout()

    # change plotting size
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    # save figure
    plt.savefig('../paper_SolverSettings/Figures/Study_4/Success_Rate_NonLinSol_3.pdf')

    # show figure
    plt.show()


# call function
NonLinSOl()