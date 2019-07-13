# script to create box plot with percentiles and median

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *

# important paths
tolerance_path = '../bachelor_thesis/Tolerance'

# main .tsv file to norm all other files
main_tsv = pd.read_csv(tolerance_path + '/06_06.tsv', sep='\t')

# get new .tsv file
main_tsv = averaging(main_tsv)

# set axis
ax = plt.axes()

# get list for all data
xTickLabel = []
total_data = []

# open all .tsv tolerance files
tolerance_files = sorted(os.listdir(tolerance_path))
tolerance_files.insert(6,'')
tolerance_files.insert(13,'')
tolerance_files.insert(20,'')
tolerance_files.insert(27,'')
tolerance_files.insert(34,'')
for iTolerance in range(0, len(tolerance_files)):

    # get empty data in there
    if iTolerance == 6 or iTolerance == 13 or iTolerance == 20 or iTolerance == 27 or iTolerance == 34:
        total_data.append([])

    else:
        # open next .tsv file
        next_tsv = pd.read_csv(tolerance_path + '/' + tolerance_files[iTolerance], sep='\t')

        # get new .tsv file
        next_tsv = averaging(next_tsv)

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
                'No 0 values allowed!'
            else:
                normed_list.append(quotient)

        # add list to total_data
        total_data.append(normed_list)

    #### get absolute and relative tolerance number
    # data
    if iTolerance == 6 or iTolerance == 13 or iTolerance == 20 or iTolerance == 27 or iTolerance == 34:
        tol = ''
        plt.setp(ax.get_xticklines(), visible=False)
    # group
    elif iTolerance == 0 or iTolerance == 7 or iTolerance == 14 or iTolerance == 21 or iTolerance == 28 or iTolerance == 35:
        tol = tolerance_files[iTolerance].split('.')[0]
    else:
        tol = tolerance_files[iTolerance].split('.')[0]
        abs_tol, rest = tolerance_files[iTolerance].split('_')
        rel_tol = rest.split('.')[0]
        tol = '_' + str(rel_tol)
    # second group
    #elif iTolerance == 7 or iTolerance == 14 or iTolerance == 21 or iTolerance == 28 or iTolerance == 35:
     #   tol = tolerance_files[iTolerance - 1].split('.')[0]
    #else:
     #   abs_tol, rest = tolerance_files[iTolerance - 1].split('_')
     #   rel_tol = rest.split('.')[0]
     #   tol = '_' + str(rel_tol)
    xTickLabel.append(tol)


# create box_plot
ax.set_yscale('log')
bp = ax.boxplot(total_data, sym='+', patch_artist=True)

####### set more options
plt.ylim([0.9,100])
# change colour for each set
colors = ['orange', 'orange', 'orange', 'orange', 'orange', 'orange',
          'white',
          'cyan', 'cyan', 'cyan', 'cyan', 'cyan', 'cyan',
          'white',
          'violet', 'violet', 'violet', 'violet', 'violet', 'violet',
           'white',
          'tan', 'tan', 'tan', 'tan', 'tan', 'tan',
          'white',
          'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
          'white',
          'lavender', 'lavender', 'lavender', 'lavender', 'lavender', 'lavender']
#for bplot in bp:
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    #for box in bp['boxes']:
        #box.set( color='darkkhaki', linewidth=2)
        #box.set( facecolor = 'blue')
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)
for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)
for median in bp['medians']:
    median.set(color='red', linewidth=2)
for flier in bp['fliers']:
    flier.set(marker='+', color='#e7298a', alpha=0.5)

# add grit
ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

#labels
xtickNames = plt.setp(ax, xticklabels=xTickLabel)
ax.set_axisbelow(True)
ax.set_title('Comparison of percentiles and median', fontsize=24)
ax.set_xlabel('All tolerance combinations', fontsize=24)
ax.set_ylabel('Quotient', fontsize=24)
plt.setp(xtickNames, rotation=45, fontsize=12, fontweight='bold')

# add legend
# plt.text(0.01, 0.9, bp['medians'][0] + ': ' + 'median', color='black', weight='roman', size='x-small', fontsize=24, transform=ax.transAxes)
# plt.legend((bp['medians'], bp['fliers']), ('median', 'outliers'), loc=2, frameon=False)

## better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Tolerance_Boxplot.pdf')

# show figure
plt.show()