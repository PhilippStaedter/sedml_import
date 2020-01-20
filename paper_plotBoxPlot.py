# script to create box plot with percentiles and median

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *
from matplotlib import ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)


Multistep_Method = 'BDF'


# decision function
if Multistep_Method == 'Adams':
    prefix = '1_'
elif Multistep_Method == 'BDF':
    prefix = '2_'

# important paths
#tolerance_path = '../bachelor_thesis/Tolerance'
tolerance_path = '../paper_SolverSettings/Tolerances_1e4/' + Multistep_Method                                                           #

# main .tsv file to norm all other files
main_tsv = pd.read_csv(tolerance_path + '/' + prefix + '06_06.tsv', sep='\t')                                                       #

# get new .tsv file
main_tsv = averaging(main_tsv)

# set two axes objects
figure = plt.figure()
ax1 = figure.add_axes([0.1, 0.5, 0.8, 0.4])                 # ax = plt.axes()
ax2 = figure.add_axes([0.1, 0.15, 0.8, 0.3])

# get list for all data
xTickLabel = []
total_data = []

# open all .tsv tolerance files
tolerance_files_old = sorted(os.listdir(tolerance_path))
#del tolerance_files[0]
tolerance_files = []
for iTolFile in range(0, len(tolerance_files_old)):
    if len(tolerance_files_old[iTolFile].split(prefix)) > 2:
        tolerance_files.append(tolerance_files_old[iTolFile].split('_')[1] + '_' + tolerance_files_old[iTolFile].split('_')[2])
    else:
        tolerance_files.append(tolerance_files_old[iTolFile].split(prefix)[1])                                                #

######## 1.PART: create Box Plot
all_averaged_files = []
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
        next_tsv = pd.read_csv(tolerance_path + '/' + prefix + tolerance_files[iTolerance], sep='\t')                          #

        # get new .tsv file
        next_tsv = averaging(next_tsv)
        all_averaged_files.append(next_tsv)

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


# create box_plot
linestyle = (0,(2,5,2,5))
linewidth = 0.1

fontsize = 22
labelsize = 18
titlesize = 30 + 4

rotation = 45
ax1.set_yscale('log')
bp = ax1.boxplot(total_data, sym='+', patch_artist=True)

####### set more options
ax1.spines['top'].set_linestyle(linestyle)
ax1.spines['top'].set_linewidth(linewidth)
ax1.spines['right'].set_linestyle(linestyle)
ax1.spines['right'].set_linewidth(linewidth)

ax1.set_ylim([0.1,250])
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
for whisker in bp['whiskers']:
    whisker.set(color='#7570b3', linewidth=2)
for cap in bp['caps']:
    cap.set(color='#7570b3', linewidth=2)
for median in bp['medians']:
    median.set(color='black', linewidth=2)
for flier in bp['fliers']:
    flier.set(marker='+', color='#e7298a', alpha=0.5)


#ax1.set_title('Comparison of percentiles and median', fontsize=titlesize, fontweight='bold')
ax1.set_ylabel('Relative simulation time', fontsize=labelsize)
ax1.set_xticklabels([])

# add grit
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)


######### 2.PART: add bar plot with failure rate
fontsize = 22 - 4
labelsize = 18 - 5
titlesize = 30

all_percentages = []
counter = 0
for iTolerance in range(0, len(all_averaged_files) + 5):
    if iTolerance in [6, 13, 20, 27, 34]:
        all_percentages.append(0)
        counter += 1
        continue

    # get new .tsv file
    next_tsv = all_averaged_files[iTolerance - counter]
    #next_tsv = averaging(next_tsv)

    # store non-zero and zero values
    non_zero_value_counter = 0
    zero_value_counter = 0
    for iFile in range(0, len(next_tsv['id'])):
        next_intern = next_tsv['t_intern_ms'][iFile]
        if next_intern == 0:
            zero_value_counter += 1
        else:
            non_zero_value_counter += 1

    # store percentage
    all_percentages.append(round(non_zero_value_counter / (non_zero_value_counter + zero_value_counter) * 100, 4))

# create bar plot
# colors to use:  '#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'
plot_barplot = ax2.bar(x=list(range(0,41)), height=all_percentages, width=0.5, color=['#d73027', '#d73027', '#d73027', '#d73027', '#d73027', '#d73027',
                                                                                      'white',
                                                                                      '#fc8d59', '#fc8d59', '#fc8d59', '#fc8d59', '#fc8d59', '#fc8d59',
                                                                                      'white',
                                                                                      '#fee090', '#fee090', '#fee090', '#fee090', '#fee090', '#fee090',
                                                                                      'white',
                                                                                      '#e0f3f8', '#e0f3f8', '#e0f3f8', '#e0f3f8', '#e0f3f8', '#e0f3f8',
                                                                                      'white',
                                                                                      '#91bfdb', '#91bfdb', '#91bfdb', '#91bfdb', '#91bfdb', '#91bfdb',
                                                                                      'white',
                                                                                      '#4575b4', '#4575b4', '#4575b4', '#4575b4', '#4575b4', '#4575b4'])

# more options
ax2.spines['top'].set_linestyle(linestyle)
ax2.spines['top'].set_linewidth(linewidth)
ax2.spines['right'].set_linestyle(linestyle)
ax2.spines['right'].set_linewidth(linewidth)

#ax2.set_xscale('log')
ax2.set_xlim([-1,41])
ax2.set_ylim([0,100])
ax2.tick_params(labelsize=labelsize)
ax2.set_ylabel('Success rates [%]', fontsize=labelsize + 5)

#labels
ax2.minorticks_on()
Abs_xTickLabels = ['', '', r'$10^{-6}$', '', '', '', '', '', '', '', '', '', '', '', '' '', '', '', '', '', '' '', '', '', '', '', '', '', '', '', '', '', '' '',
                   r'$10^{-8}$', '', '', '', '', '', '', '', '', '', '', '', '' '', '', '', '', '', '' '', '', '', '', '', '', '', '', '', '', '',
                   r'$10^{-10}$', '', '', '', '', '', '', '', '', '', '', '', '' '', '', '', '', '', '' '', '', '', '', '', '', '', '', '', '', '',
                   r'$10^{-12}$', '', '', '', '', '', '', '', '', '', '', '', '' '', '', '', '', '', '' '', '', '', '', '', '', '', '', '', '', '',
                   r'$10^{-14}$', '', '', '', '', '', '', '', '', '', '', '', '' '', '', '', '', '', '' '', '', '', '', '', '', '', '', '', '', '',
                   r'$10^{-16}$']
Rel_xTckLabels = [r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$', '',
                  r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$', '',
                  r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$', '',
                  r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$', '',
                  r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$', '',
                  r'$10^{-6}$', r'$10^{-8}$', r'$10^{-10}$', r'$10^{-12}$', r'$10^{-14}$', r'$10^{-16}$']
Rel_xTickNames = plt.setp(ax2, xticklabels=Rel_xTckLabels)
ax2.xaxis.set_minor_formatter(ticker.FixedFormatter(Abs_xTickLabels))
plt.setp(ax2.xaxis.get_minorticklabels(), rotation=45, fontsize=labelsize, fontweight='bold')
ax2.tick_params(axis='x', which='major', pad=40)
ax2.set_axisbelow(True)
plt.setp(Rel_xTickNames, rotation=rotation, fontsize=fontsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

'''
############# something like this
# Make a plot with major ticks that are multiples of 20 and minor ticks that
# are multiples of 5.  Label major ticks with '%d' formatting but don't label
# minor ticks.
ax2.xaxis.set_major_locator(MultipleLocator(20))
ax2.xaxis.set_major_formatter(FormatStrFormatter('Rel_Tol'))

# For the minor ticks, use no labels; default NullFormatter.
ax2.xaxis.set_minor_locator(MultipleLocator(5))
ax2.xaxis.set_major_formatter(FormatStrFormatter('\nAbs_Tol'))

# in combination with this
ax2.set_xticklabels(('A1', 'A2', '\n\nGeneral Info', 'B1', 'B2', '\n\nTechnical', 'C1', 'C2', '\n\nPsycological'),ha='center')
ax2.tick_params(axis='x', which='minor',length=0)
'''

# add rel and abs in a text box
ax2.text(-2.5, -2.5, 'Abs_Tol: ', fontsize=labelsize, fontweight='bold')
ax2.text(-2.5, -3.5, 'Rel_Tol: ', fontsize=labelsize, fontweight='bold')



## better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../paper_SolverSettings/Figures/Study_2/Tolerances_BoxPlot_BarPlot_' + Multistep_Method + '.pdf')

# show figure
plt.show()