# script to create box plot with percentiles and median

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from averageTime import *
from matplotlib import ticker


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
ax1 = figure.add_axes([0.1, 0.55, 0.8, 0.4])                 # ax = plt.axes()
ax2 = figure.add_axes([0.1, 0.05, 0.8, 0.3])

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

    #### get aF
    #else:
     #   abs_tol, rest = tolerance_files[iTolerance - 1].split('_')
     #   rel_tol = rest.split('.')[0]
     #   tol = '_' + str(rel_tol)
     #xTickLabel.append(tol)


# create box_plot
fontsize = 22
labelsize = 18
titlesize = 30 + 4

rotation = 45
ax1.set_yscale('log')
bp = ax1.boxplot(total_data, sym='+', patch_artist=True)

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
ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

#labels
ax1.minorticks_on()
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
Rel_xTickNames = plt.setp(ax1, xticklabels=Rel_xTckLabels)
ax1.xaxis.set_minor_formatter(ticker.FixedFormatter(Abs_xTickLabels))
plt.setp(ax1.xaxis.get_minorticklabels(), rotation=45, fontsize=labelsize, fontweight='bold')
ax1.tick_params(axis='x', which='major', pad=40)
ax1.set_axisbelow(True)
ax1.set_title('Comparison of percentiles and median', fontsize=titlesize, fontweight='bold')
ax1.set_xlabel('Success rates of all tolerance combinations', fontsize=titlesize, fontweight='bold')
ax1.set_ylabel(' default simulation conditions) of a model', fontsize=labelsize, fontweight='bold')
plt.setp(Rel_xTickNames, rotation=rotation, fontsize=fontsize, fontweight='bold')
plt.tick_params(labelsize=labelsize)

# add rel and abs in a text box
plt.text(-2.5, 0.65, 'Abs_Tol: ', fontsize=labelsize, fontweight='bold')
plt.text(-2.5, 0.43, 'Rel_Tol: ', fontsize=labelsize, fontweight='bold')
plt.text(-2.9, 70, 'Relative simulation time (compared to ', fontsize=labelsize + 3, fontweight='bold', rotation=90)


######### 2.PART: add bar plot with failure rate
fontsize = 22 - 4
labelsize = 18 - 5
titlesize = 30

all_percentages = []
for iTolerance in range(0, len(all_averaged_files)):
    #next_tsv = pd.read_csv(tolerance_path + '/' + tolerance_files_old[iTolerance], sep='\t')

    # get new .tsv file
    next_tsv = all_averaged_files[iTolerance]
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
    all_percentages.append(round(non_zero_value_counter / (non_zero_value_counter + zero_value_counter), 4))

# create bar plot
plot_barplot = ax2.bar(x=list(range(0,36)), height=all_percentages, width=0.5)

# more options
#ax2.set_xscale('log')
ax2.set_ylim([0,1])
ax2.tick_params(labelsize=labelsize)
#plt.text(x=1, y=50, s='sucess: ' + str(round(len(normed_list) / (len(normed_list) + zero_values_counter) * 100, 2)) + ' %', fontsize=labelsize - 4, fontweight='bold')
#plt.legend('Hi')#'success rate: ' + str(zero_values_counter / (len(normed_list) + zero_values_counter)) + ' %')


# set global labels
#plt.text(-5.65, -0.7, 'Relative simulation time (compared to default simulation conditions) of a model', fontsize=titlesize - 5, fontweight='bold', transform=ax1.transAxes)
#plt.text(-6.4, 5, 'Amount of models', fontsize=titlesize, fontweight='bold', transform=ax1.transAxes, rotation=90)
#plt.text(-5.75, 7.2, 'Simulation time distribution of models for different tolerance combinations - ' + Multistep_Method, fontsize=titlesize - 5, fontweight='bold', transform=ax1.transAxes)  # -60 , 350


# add legend
# plt.text(0.01, 0.9, bp['medians'][0] + ': ' + 'median', color='black', weight='roman', size='x-small', fontsize=24, transform=ax1.transaxes)
# plt.legend((bp['medians'], bp['fliers']), ('median', 'outliers'), loc=2, frameon=False)

## better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../paper_SolverSettings/Figures/Study_2/Tolerances_BoxPlot_BarPlot_' + Multistep_Method + '.pdf')

# show figure
plt.show()