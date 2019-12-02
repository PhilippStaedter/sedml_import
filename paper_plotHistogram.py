# script to plot a histogram for stuy 2 ---- for intern and extern

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *

# important paths
tolerance_path = '../paper_SolverSettings/Tolerances_1e4/BDF'

# main .tsv file to norm all other files
main_tsv = pd.read_csv(tolerance_path + '/2_06_06.tsv', sep='\t')

# get new .tsv file
main_tsv = averaging(main_tsv)

# open all .tsv tolerance files
tolerance_files = sorted(os.listdir(tolerance_path))
for iTolerance in range(0, len(tolerance_files)):
    next_tsv = pd.read_csv(tolerance_path + '/' + tolerance_files[iTolerance], sep='\t')

    # get new .tsv file
    next_tsv = averaging(next_tsv)

    zero_values_counter = 0
    normed_list = []
    for iFile in range(0, len(main_tsv['id'])):
        main_intern = main_tsv['t_intern_ms'][iFile]
        next_intern = next_tsv['t_intern_ms'][iFile]

        # norm all internal + external time by 06_06
        if main_intern == 0:
            quotient = 0
        else:
            quotient = next_intern/main_intern

        # leave out value iff zero
        if quotient == 0:
            zero_values_counter = zero_values_counter + 1
            'No 0 values allowed!'
        else:
            normed_list.append(quotient)

    # for xlim control
    if sorted(normed_list, reverse=True)[0] > 10:
        print('Need bigger xlim: ' + str(sorted(normed_list, reverse=True)[0]) + ' ; ' + main_tsv['id'][iFile] + ' ; ' + tolerance_files[iTolerance])

    # get absolute and relative tolerance number
    _, abs_tol, rest = tolerance_files[iTolerance].split('_')
    rel_tol = rest.split('.')[0]

    # plot as histogram
    fontsize = 22 - 4
    labelsize = 18 - 5
    titlesize = 30

    left = 0.08
    bottom = 0.75
    width = 0.13
    height = 0.115
    row_factor = 0.15
    column_factor = 0.13
    rotation_factor = 78
    ylim = [0.5, 200]
    xlim = [0.1, 100]

    # create axes
    if iTolerance in range(0,6):
        ax1 = plt.axes([left + iTolerance * row_factor, bottom, width, height])                                                                              # [left, bottom, width, height]
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        ax1.tick_params(labelbottom=False)
        if iTolerance == 0:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
            ax1.text(0.2, 1.1, 'rtol = 1e-' + str(rel_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes)
        if iTolerance in range(1,6):
            ax1.tick_params(labelleft=False)
            ax1.text(0.2, 1.1, 'rtol = 1e-' + str(rel_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes)
    elif iTolerance in range(6,12):
        ax1 = plt.axes([left + (iTolerance - 6) * row_factor, bottom - 1 * column_factor ,width, height])
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        ax1.tick_params(labelbottom=False)
        if iTolerance == 6:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(7,12):
            ax1.tick_params(labelleft=False)
    elif iTolerance in range(12,18):
        ax1 = plt.axes([left + (iTolerance - 12) * row_factor, bottom - 2 * column_factor , width, height])
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        ax1.tick_params(labelbottom=False)
        if iTolerance == 12:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(13,18):
            ax1.tick_params(labelleft=False)
    elif iTolerance in range(18, 24):
        ax1 = plt.axes([left + (iTolerance - 18) * row_factor, bottom - 3 * column_factor , width, height])
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        ax1.tick_params(labelbottom=False)
        if iTolerance == 18:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(19,24):
            ax1.tick_params(labelleft=False)
    elif iTolerance in range(24,30):
        ax1 = plt.axes([left + (iTolerance - 24) * row_factor, bottom - 4 * column_factor , width, height])
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        ax1.tick_params(labelbottom=False)
        if iTolerance == 24:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(25,30):
            ax1.tick_params(labelleft=False)
    elif iTolerance in range(30,36):
        ax1 = plt.axes([left + (iTolerance - 30) * row_factor, bottom- 5 * column_factor , width, height])
        ax1.set_xlim(xlim)
        ax1.set_ylim(ylim)
        if iTolerance == 30:
            ax1.text(-0.4, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=fontsize, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(31,36):
            ax1.tick_params(labelleft=False)

    ax1.set_xscale('log')
    ax1.tick_params(labelsize=labelsize)
    plot_histogram = ax1.hist(x=normed_list, range=None, bins=100, log=True)
    plt.text(x=1, y=50, s='sucess: ' + str(round(len(normed_list) / (len(normed_list) + zero_values_counter) * 100, 2)) + ' %', fontsize=labelsize - 4, fontweight='bold')
    #plt.legend('Hi')#'success rate: ' + str(zero_values_counter / (len(normed_list) + zero_values_counter)) + ' %')


# set global labels
plt.text(-5.65, -0.7, 'Relative simulation time (compared to default simulation conditions) of a model', fontsize=titlesize - 5, fontweight='bold', transform=ax1.transAxes)
plt.text(-6.4, 5, 'Amount of models', fontsize=titlesize, fontweight='bold', transform=ax1.transAxes, rotation=90)
plt.text(-5.75, 7.2, 'Simulation time distribution of models for different tolerance combinations - BDF', fontsize=titlesize - 5, fontweight='bold', transform=ax1.transAxes)  # -60 , 350

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../paper_SolverSettings/Tolerances_one_repetition/Tolerances_one_repetition_1e8/Tolerances_Histogram_BDF.pdf')

# show figure
plt.show()