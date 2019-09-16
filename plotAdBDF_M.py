# script for a predictor model to test and predict best simulation parameters

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *
from matplotlib.legend import Legend


# important paths
tsv_save_path = '../bachelor_thesis/SolverAlgorithm'
real_data_path = '../bachelor_thesis/SolverAlgorithm/Real_Data.tsv'

# open data
real_data = pd.read_csv(real_data_path, sep='\t')
column_names = real_data.columns

# get smallest simulation time != 0
x_Adams = []
y_BDF = []
for iModel in range(1, len(column_names)):
    all_values = real_data[column_names[iModel]]
    ADAMS = all_values[:20]
    BDF = all_values[20:]

    smallest_Adams = sorted(ADAMS)
    for iNumber in range(0, len(smallest_Adams)):
        if sum(smallest_Adams) != 0:
            if smallest_Adams[0] == 0:
                del smallest_Adams[0]
            else:
                x_Adams.append(smallest_Adams[0])
                break
        else:
            x_Adams.append(0)
            break

    smallest_BDF = sorted(BDF)
    for iNumber in range(0, len(smallest_BDF)):
        if sum(smallest_BDF) != 0:
            if smallest_BDF[0] == 0:
                del smallest_BDF[0]
            else:
                y_BDF.append(smallest_BDF[0])
                break
        else:
            y_BDF.append(0)
            break

# decide which solver algorithm is better
adams_bdf_x = []          # red
adams_bdf_y = []
bdf_adams_x = []          # green
bdf_adams_y = []
equal_x = []                    # yellow
equal_y = []
adams_zero_x = []
adams_zero_y = []
bdf_zero_x = []
bdf_zero_y = []
equal_zero_x = []
equal_zero_y = []
for iValue in range(0, len(x_Adams)):
    if x_Adams[iValue] != 0 and y_BDF[iValue] != 0:
        if x_Adams[iValue] < y_BDF[iValue]:
            adams_bdf_x.append(x_Adams[iValue])
            adams_bdf_y.append(y_BDF[iValue])
        elif y_BDF[iValue] < x_Adams[iValue]:
            bdf_adams_x.append(x_Adams[iValue])
            bdf_adams_y.append(y_BDF[iValue])
        elif x_Adams[iValue] == y_BDF[iValue]:
            equal_x.append(x_Adams[iValue])
            equal_y.append(y_BDF[iValue])
    elif x_Adams[iValue] == 0 and y_BDF[iValue] != 0:
        adams_zero_x.append(2000)
        adams_zero_y.append(y_BDF[iValue])
    elif x_Adams[iValue] != 0 and y_BDF[iValue] == 0:
        bdf_zero_x.append(x_Adams[iValue])
        bdf_zero_y.append(200)
    elif x_Adams[iValue] == 0 and y_BDF[iValue] == 0:
        equal_zero_x.append(2000)
        equal_zero_y.append(200)

# look for the biggest/smallest values
print('adams_bdf_x: ' + str(sorted(adams_bdf_x, reverse=True)[0]))                                            #, reverse=True
print('adams_bdf_y: ' + str(sorted(adams_bdf_y, reverse=True)[0]))
print('bdf_adams_x: ' + str(sorted(bdf_adams_x, reverse=True)[0]))
print('bdf_adams_y: ' + str(sorted(bdf_adams_y, reverse=True)[0]))
#print('equal_x: ' + str(sorted(equal_x, reverse=True)[0]))
#print('equal_y: ' + str(sorted(equal_y, reverse=True)[0]))
print('adams_zero_x: ' + str(sorted(adams_zero_x, reverse=True)[0]))
print('adams_zero_y: ' + str(sorted(adams_zero_y, reverse=True)[0]))
print('bdf_zero_x: ' + str(sorted(bdf_zero_x, reverse=True)[0]))
print('bdf_zero_y: ' + str(sorted(bdf_zero_y, reverse=True)[0]))
#print('equal_zero_x: ' + str(sorted(equal_zero_x)[0]))
#print('equal_zero_y: ' + str(sorted(equal_zero_y)[0]))

# plot a scatter plot + diagonal line
ax = plt.axes()
z = range(0,2000)
plt1 = ax.scatter(adams_bdf_x, adams_bdf_y, c='red', label='Adams default setting is better than the prediction', zorder=10, clip_on=False)
plt2 = ax.scatter(bdf_adams_x, bdf_adams_y, c='green', label='Prediction is better than Adams default setting', zorder=10, clip_on=False)
plt3 = ax.scatter(equal_x, equal_y, c='blue', label='Both are equally good', zorder=10, clip_on=False)
plt4 = ax.scatter(adams_zero_x, adams_zero_y, c='green', marker='s', label='Adams default failed to integrate the model', zorder=10, clip_on=False)
plt5 = ax.scatter(bdf_zero_x, bdf_zero_y, c='red', marker='s', label='Prediction setting failed to integrate the model', zorder=10, clip_on=False)
plt6 = ax.scatter(equal_zero_x, equal_zero_y, c='blue', marker='s', label='Both failed to integrate the model', zorder=10, clip_on=False)
ax.plot(z)
ax.set_xlim([0.5, 2000])
ax.set_ylim([0.5, 200])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Adams default simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_ylabel('BDFs simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_title('Adams-Mouton vs. BDF settings', fontsize=24, fontweight='bold', pad=30)
ax.legend(loc=2)

leg = Legend(ax, [plt1, plt2, plt3, plt4, plt5, plt6], [str(round(len(adams_bdf_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(bdf_adams_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(equal_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(adams_zero_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(bdf_zero_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(equal_zero_x)/166 * 100, 2)) + ' %'], loc='lower right', frameon=True)
ax.add_artist(leg)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../bachelor_thesis/New_Figures/Figures_study_4/Adams_vs_BDF_Models_166SBML.pdf')

# show figure
plt.show()
