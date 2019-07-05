# script to plot a histogram for stuy 2 ---- for intern and extern

import pandas as pd
import os
import matplotlib.pyplot as plt


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


    # plot as histogram
    left = 0.08
    bottom = 0.75
    width = 0.13
    height = 0.12
    row_factor = 0.15
    column_factor = 0.13
    # create axes
    if iTolerance in range(0,6):
        ax1 = plt.axes([left + iTolerance * row_factor, bottom, width, height])                                                                              # [left, bottom, width, height]
        ax1.get_xaxis().set_visible(False)
        if iTolerance in range(1,6):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(6,12):
        ax1 = plt.axes([left + (iTolerance -6) * row_factor, bottom - 1 * column_factor ,width, height])
        ax1.get_xaxis().set_visible(False)
        if iTolerance in range(7,12):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(12,18):
        ax1 = plt.axes([left + (iTolerance - 12) * row_factor, bottom - 2 * column_factor , width, height])
        ax1.get_xaxis().set_visible(False)
        if iTolerance in range(13,18):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(18, 24):
        ax1 = plt.axes([left + (iTolerance - 18) * row_factor, bottom - 3 * column_factor , width, height])
        ax1.get_xaxis().set_visible(False)
        if iTolerance in range(19,24):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(24,30):
        ax1 = plt.axes([left + (iTolerance - 24) * row_factor, bottom - 4 * column_factor , width, height])
        ax1.get_xaxis().set_visible(False)
        if iTolerance in range(25,30):
            ax1.get_yaxis().set_visible(False)
    elif iTolerance in range(30,36):
        ax1 = plt.axes([left + (iTolerance - 30) * row_factor, bottom- 5 * column_factor , width, height])
        if iTolerance in range(31,36):
            ax1.get_yaxis().set_visible(False)

    plott = ax1.hist(x=normed_list, range=[0, 10], bins=200) #, log=True)

    # show figure
    #plt.show()

axes = plt.gca()
axes.set_ylim([0, 50])
ax1.set_xlabel('Quotient')
ax1.set_ylabel('Amount of models')
ax1.set_title('Simulation time distribution of models for different tolerance combinations')

# fig, ax2 = plt.subplot(6, 6, iTolerance + 1)
#plt.xlim((None, 250))  # Froehlich2018: 1396
#plt.ylim((None, 100))
#plt.xlabel('Quotinet')
#plt.ylabel('Amount of models')


# better layout
# plt.tight_layout()

# save figure
# plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Tolerance_study.png')

# show figure
plt.show()