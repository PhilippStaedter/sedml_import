# script to plot a histogram for stuy 2 ---- for intern and extern

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# important paths
tolerance_path = '../bachelor_thesis/Tolerance'

# main .tsv file to norm all other files
main_tsv = pd.read_csv(tolerance_path + '/06_06.tsv', sep='\t')

# open all .tsv tolernace files
tolerance_files = sorted(os.listdir(tolerance_path))
for iTolerance in range(0, len(tolerance_files)):
    next_tsv = pd.read_csv(tolerance_path + '/' + tolerance_files[iTolerance], sep='\t')

    normed_list = []
    for iFile in range(0, len(main_tsv['id'])):
        main_intern = main_tsv['t_intern_ms'][iFile]
        next_intern = next_tsv['t_intern_ms'][iFile]

        # norm all internal + external time by 06_06
        if main_intern == 0:
            quotient = 0
        else:
            quotient = next_intern/main_intern
        normed_list.append(quotient)

    # for xlim control
    if sorted(normed_list, reverse=True)[0] > 10:
        print('Need bigger xlim: ' + str(sorted(normed_list, reverse=True)[0]) + ' ; ' + main_tsv['id'][iFile] + ' ; ' + tolerance_files[iTolerance])

    # get absolute and relative tolerance number
    abs_tol, rest = tolerance_files[iTolerance].split('_')
    rel_tol = rest.split('.')[0]

    # plot as histogram
    left = 0.08
    bottom = 0.75
    width = 0.13
    height = 0.12
    row_factor = 0.15
    column_factor = 0.13
    rotation_factor = 70

    # create axes
    if iTolerance in range(0,6):
        ax1 = plt.axes([left + iTolerance * row_factor, bottom, width, height])                                                                              # [left, bottom, width, height]
        ax1.set_ylim([0, 40])
        ax1.get_xaxis().set_visible(False)
        if iTolerance == 0:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
            ax1.text(0.3, 1.1, 'rtol = 1e-' + str(rel_tol), fontsize=14, fontweight='bold', transform=ax1.transAxes)
        if iTolerance in range(1,6):
            ax1.get_yaxis().set_visible(False)
            ax1.text(0.35, 1.1, 'rtol = 1e-' + str(rel_tol), fontsize=14, fontweight='bold', transform=ax1.transAxes)
    elif iTolerance in range(6,12):
        ax1 = plt.axes([left + (iTolerance -6) * row_factor, bottom - 1 * column_factor ,width, height])
        ax1.set_ylim([0, 40])
        ax1.get_xaxis().set_visible(False)
        if iTolerance == 6:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(7,12):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(12,18):
        ax1 = plt.axes([left + (iTolerance - 12) * row_factor, bottom - 2 * column_factor , width, height])
        ax1.set_ylim([0, 40])
        ax1.get_xaxis().set_visible(False)
        if iTolerance == 12:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(13,18):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(18, 24):
        ax1 = plt.axes([left + (iTolerance - 18) * row_factor, bottom - 3 * column_factor , width, height])
        ax1.set_ylim([0, 40])
        ax1.get_xaxis().set_visible(False)
        if iTolerance == 18:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(19,24):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(24,30):
        ax1 = plt.axes([left + (iTolerance - 24) * row_factor, bottom - 4 * column_factor , width, height])
        ax1.set_ylim([0, 40])
        ax1.get_xaxis().set_visible(False)
        if iTolerance == 24:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(25,30):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(30,36):
        ax1 = plt.axes([left + (iTolerance - 30) * row_factor, bottom- 5 * column_factor , width, height])
        ax1.set_ylim([0, 40])
        if iTolerance == 30:
            ax1.text(-0.35, 0.85, 'atol = 1e-' + str(abs_tol), fontsize=12, fontweight='bold', transform=ax1.transAxes, rotation=rotation_factor)
        if iTolerance in range(31,36):
            ax1.get_yaxis().set_visible(False)

    plot_histogram = ax1.hist(x=normed_list, range=[0, 10], bins=200) #, log=True)

# set global labels
plt.text(-3, -0.5, 'Quotient', fontsize=24, transform=ax1.transAxes)
plt.text(-6.3, 4, 'Amount of models', fontsize=24, transform=ax1.transAxes, rotation=90)
plt.text(-5.2, 7, 'Simulation time distribution of models for different tolerance combinations', fontsize=24, transform=ax1.transAxes)  # -60 , 350

# adds major gridlines
# plt.grid(color='grey', linestyle='-', linewidth=0.15, alpha=0.5)

# fig, ax2 = plt.subplot(6, 6, iTolerance + 1)
#plt.xlim((None, 250))  # Froehlich2018: 1396
#plt.ylim((None, 100))
#plt.xlabel('Quotinet')
#plt.ylabel('Amount of models')


# better layout
plt.tight_layout()

# save figure
# plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Tolerance_Histogram.png')

# show figure
plt.show()