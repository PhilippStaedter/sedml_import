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

    # get correct data for the bar plot
    # plot a customized bar plot
    labelsize = 8
    fontsize = 12
    titlesize = 22

    rotation = 45
    left = 0.07
    bottom = 0.6
    width = 0.86
    height = 0.3
    row_factor = 0.45
    column_factor = 0.1
    rotation_factor = 70
    alpha = 1
    bar_width = 0.35

    # plot one density plot
    ax = plt.axes()
    index = np.arange(35)

    # initialize y-data
    adams_data_1 = []
    bdf_data_1 = []
    adams_data_2 = []
    bdf_data_2 = []

    '''
    # just one for the legend
    adams_data_1.append(all_intern_columns_1[0][column_names[0]])
    bdf_data_1.append(all_intern_columns_2[0][column_names[0]])
    nonLinSol11 = ax.plot(index[0], round(len(adams_data_1) / file_length, 2), '-x', c='#e66101', label='Functional AM')
    nonLinSol21 = ax.plot(index[0], round(len(bdf_data_1) / file_length, 2), '-x', c='#fdb863', label='Functional BDF')
    adams_data_2 = all_intern_columns_1[int(len(correct_files_1)/2)][column_names[int(len(correct_files_1)/2)]]
    bdf_data_2 = all_intern_columns_2[int(len(correct_files_1)/2)][column_names[int(len(correct_files_1)/2)]]
    nonLinSol12 = ax.plot(index[int(len(correct_files_1)/2) - int(len(correct_files_1) / 2)], round(len(adams_data_2) / file_length, 2), '-x', c='#b2abd2', label='Newton-type AM')
    nonLinSol22 = ax.plot(index[int(len(correct_files_1)/2) - int(len(correct_files_1) / 2)], round(len(bdf_data_2) / file_length, 2), '-x', c='#5e3c99', label='Newton_type BDF')
    '''

    # Functional
    for iDensityPoint in range(0, int(len(correct_files_1)/2)):
        adams_data_1.append(round(len(all_intern_columns_1[iDensityPoint][column_names[iDensityPoint]]) / file_length, 2))
        bdf_data_1.append(round(len(all_intern_columns_2[iDensityPoint][column_names[iDensityPoint]]) / file_length, 2))
    nonLinSol11 = ax.plot(index, adams_data_1, '-x', c='#e66101', label='Functional AM')
    nonLinSol21 = ax.plot(index, bdf_data_1, '-x', c='#fdb863', label='Functional BDF')

    # Newton-type
    for iDensityPoint in range(int(len(correct_files_1)/2), len(correct_files_1)):
        adams_data_2.append(round(len(all_intern_columns_1[iDensityPoint][column_names[iDensityPoint]]) / file_length, 2))
        bdf_data_2.append(round(len(all_intern_columns_2[iDensityPoint][column_names[iDensityPoint]]) / file_length, 2))
    nonLinSol12 = ax.plot(index, adams_data_2, '-x', c='#b2abd2', label='Newton-type AM')
    nonLinSol22 = ax.plot(index, bdf_data_2, '-x', c='#5e3c99', label='Newton-type BDF')

    #ax.set_title('Non-Linear solver: Functional', fontsize=titlesize)
    ax.set_ylabel('Success rate [%]', fontsize=fontsize)
    #ax.set_title('Non-Linear solver: Newton-type', fontsize=titlesize)
    ax.set_xlim([-0.5, 34.5])
    ax.set_ylim([0.7, 1])
    ax.set_yticklabels(['70', '75', '80', '85', '90', '95', '100'], fontsize=labelsize)


    # create major and minor ticklabels
    '''
    upper_labels = ['D', '', '', '', '', '', '', 'G', '', '', '', '', '', '', 'B', '', '', '', '', '', '',
                    'T', '', '', '', '', '', '', 'K', '', '', '', '', '', '']
    Abs_Rel_Tol = [r'$10^{-6}$' '\n' r'$10^{-8}$', r'$10^{-8}$' '\n' r'$10^{-6}$', r'$10^{-8}$' '\n' r'$10^{-16}$', r'$10^{-10}$' '\n' r'$10^{-12}$',
                   r'$10^{-12}$' '\n'  r'$10^{-10}$', r'$10^{-14}$' '\n' r'$10^{-14}$', r'$10^{-16}$' '\n' r'$10^{-8}$',
                   r'$10^{-6}$' '\n' r'$10^{-8}$', r'$10^{-8}$' '\n' r'$10^{-6}$', r'$10^{-8}$' '\n' r'$10^{-16}$', r'$10^{-10}$' '\n' r'$10^{-12}$',
                   r'$10^{-12}$' '\n'  r'$10^{-10}$', r'$10^{-14}$' '\n' r'$10^{-14}$', r'$10^{-16}$' '\n' r'$10^{-8}$',
                   r'$10^{-6}$' '\n' r'$10^{-8}$', r'$10^{-8}$' '\n' r'$10^{-6}$', r'$10^{-8}$' '\n' r'$10^{-16}$', r'$10^{-10}$' '\n' r'$10^{-12}$',
                   r'$10^{-12}$' '\n'  r'$10^{-10}$', r'$10^{-14}$' '\n' r'$10^{-14}$', r'$10^{-16}$' '\n' r'$10^{-8}$',
                   r'$10^{-6}$' '\n' r'$10^{-8}$', r'$10^{-8}$' '\n' r'$10^{-6}$', r'$10^{-8}$' '\n' r'$10^{-16}$', r'$10^{-10}$' '\n' r'$10^{-12}$',
                   r'$10^{-12}$' '\n'  r'$10^{-10}$', r'$10^{-14}$' '\n' r'$10^{-14}$', r'$10^{-16}$' '\n' r'$10^{-8}$',
                   r'$10^{-6}$' '\n' r'$10^{-8}$', r'$10^{-8}$' '\n' r'$10^{-6}$', r'$10^{-8}$' '\n' r'$10^{-16}$', r'$10^{-10}$' '\n' r'$10^{-12}$',
                   r'$10^{-12}$' '\n'  r'$10^{-10}$', r'$10^{-14}$' '\n' r'$10^{-14}$', r'$10^{-16}$' '\n' r'$10^{-8}$']
    '''

    ax.text(0, -0.1, '  D                                         G                                          B'
                     '                                          T                                          K', fontsize=labelsize, transform=ax.transAxes)
    upper_labels = [r'$10^{-6}$', r'$10^{-8}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$',
                    r'$10^{-6}$', r'$10^{-8}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$',
                    r'$10^{-6}$', r'$10^{-8}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$',
                    r'$10^{-6}$', r'$10^{-8}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$',
                    r'$10^{-6}$', r'$10^{-8}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$']
    lower_labels = [r'$10^{-8}$', r'$10^{-6}$', r'$10^{-16}$', r'$10^{-12}$', r'$10^{-10}$', r'$10^{-14}$', r'$10^{-8}$',
                    r'$10^{-8}$', r'$10^{-6}$', r'$10^{-16}$', r'$10^{-12}$', r'$10^{-10}$', r'$10^{-14}$', r'$10^{-8}$',
                    r'$10^{-8}$', r'$10^{-6}$', r'$10^{-16}$', r'$10^{-12}$', r'$10^{-10}$', r'$10^{-14}$', r'$10^{-8}$',
                    r'$10^{-8}$', r'$10^{-6}$', r'$10^{-16}$', r'$10^{-12}$', r'$10^{-10}$', r'$10^{-14}$', r'$10^{-8}$',
                    r'$10^{-8}$', r'$10^{-6}$', r'$10^{-16}$', r'$10^{-12}$', r'$10^{-10}$', r'$10^{-14}$', r'$10^{-8}$']


    ax.set_xticks(list(range(35)))
    minor_list_1 = [x + 0.001 for x in list(range(35))]
    ax.set_xticks(minor_list_1, minor=True)
    ax.set_xticklabels(upper_labels, fontsize=labelsize, rotation=rotation)
    ax.set_xticklabels(lower_labels, minor=True, fontsize=labelsize, rotation=rotation)
    ax.tick_params(axis='x', which='major', pad=25)
    ax.tick_params(axis='x', which='minor', pad=50)
    ax.text(-0.12, -0.1, 'Lin. sol.: ', fontsize=fontsize, transform=ax.transAxes)
    ax.text(-0.12, -0.22, 'Abs. tol.: ', fontsize=fontsize, transform=ax.transAxes)
    ax.text(-0.12, -0.34, 'Rel. tol.: ', fontsize=fontsize, transform=ax.transAxes)

    # create new empty invisible axis for legend
    #ax3 = figure.add_axes([0.15, 0.4, 0.02, 0.02])
    #ax3.plot(range(2), c='orange', label='AM')
    #ax3.plot(range(2), c='blue', label='BDF')
    ax.legend(loc=4, fontsize=labelsize)
    ax.text(0.15, -0.48, 'D: Dense,  G: GMRES,  B: BCG,  T: TFQMR,  K: KLU', fontsize=fontsize, transform=ax.transAxes)

    # make top and right boxlines invisible
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # set global labels
    #ax1.set_title('Adams-Moulton vs BDF - Success Rate', fontsize=titlesize, fontweight='bold', pad=30)
    #plt.text(0.3, 2.75, 'Adams-Moulton vs BDF - Success Rate', fontsize=titlesize, fontweight='bold', transform=ax2.transAxes)

    # better layout
    plt.tight_layout()

    # change plotting size
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    # save figure
    #plt.savefig('../paper_SolverSettings/Figures/Study_5/Success_Rate_SolAlg.pdf')

    # show figure
    plt.show()
    # adjustment values
    #top = 0.959,
    #bottom = 0.328,
    #left = 0.116,
    #right = 0.95,
    #hspace = 0.2,
    #wspace = 0.2

# call functions
Multistep()