# script to create box plot with percentiles and median

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# important paths
tolerance_path = '../bachelor_thesis/Tolerance'

# main .tsv file to norm all other files
main_tsv = pd.read_csv(tolerance_path + '/06_06.tsv', sep='\t')

# get list for all data
xTickLabel = []
total_data = []

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

    # add list to total_data
    total_data.append(normed_list)

    # get absolute and relative tolerance number
    if iTolerance == 0 or iTolerance == 6 or iTolerance == 12 or iTolerance == 18 or iTolerance == 24 or iTolerance == 30:
        tol = tolerance_files[iTolerance].split('.')[0]
    else:
        abs_tol, rest = tolerance_files[iTolerance].split('_')
        rel_tol = rest.split('.')[0]
        tol = '_' + str(rel_tol)
    xTickLabel.append(tol)


# create box_plot
ax = plt.axes()
bp = ax.boxplot(total_data, sym='+', patch_artist=True)

####### set more options
plt.ylim([-1,15])
# change colour
for box in bp['boxes']:
    box.set( color='#7570b3', linewidth=2)
    box.set( facecolor = 'darkkhaki')
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


## better layout
plt.tight_layout()

# save figure
# plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Tolerance_study.png')

# show figure
plt.show()