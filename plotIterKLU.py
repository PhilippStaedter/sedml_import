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
x_Iter = []
y_KLU = []
for iModel in range(1, len(column_names)):
    all_values = real_data[column_names[iModel]]
    ITER = pd.Series(list(all_values[4:16]) + list(all_values[24:36]))
    KLU = pd.Series(list(all_values[16:20]) + list(all_values[36:]))

    smallest_Iter = sorted(ITER)
    for iNumber in range(0, len(smallest_Iter)):
        if sum(smallest_Iter) != 0:
            if smallest_Iter[0] == 0:
                del smallest_Iter[0]
            else:
                x_Iter.append(smallest_Iter[0])
                break
        else:
            x_Iter.append(0)
            break

    smallest_KLU = sorted(KLU)
    for iNumber in range(0, len(smallest_KLU)):
        if sum(smallest_KLU) != 0:
            if smallest_KLU[0] == 0:
                del smallest_KLU[0]
            else:
                y_KLU.append(smallest_KLU[0])
                break
        else:
            y_KLU.append(0)
            break

#decide which solver is better
iter_klu_x = []          # red
iter_klu_y = []
klu_iter_x = []          # green
klu_iter_y = []
equal_x = []                    # yellow
equal_y = []
iter_zero_x = []
iter_zero_y = []
klu_zero_x = []
klu_zero_y = []
equal_zero_x = []
equal_zero_y = []
for iValue in range(0, len(x_Iter)):
    if x_Iter[iValue] != 0 and y_KLU[iValue] != 0:
        if x_Iter[iValue] < y_KLU[iValue]:
            iter_klu_x.append(x_Iter[iValue])
            iter_klu_y.append(y_KLU[iValue])
        elif y_KLU[iValue] < x_Iter[iValue]:
            klu_iter_x.append(x_Iter[iValue])
            klu_iter_y.append(y_KLU[iValue])
        elif x_Iter[iValue] == y_KLU[iValue]:
            equal_x.append(x_Iter[iValue])
            equal_y.append(y_KLU[iValue])
    elif x_Iter[iValue] == 0 and y_KLU[iValue] != 0:
        iter_zero_x.append(4000)
        iter_zero_y.append(y_KLU[iValue])
    elif x_Iter[iValue] != 0 and y_KLU[iValue] == 0:
        klu_zero_x.append(x_Iter[iValue])
        klu_zero_y.append(200)
    elif x_Iter[iValue] == 0 and y_KLU[iValue] == 0:
        equal_zero_x.append(4000)
        equal_zero_y.append(200)

# look for the biggest/smallest values
print('iter_klu_x: ' + str(sorted(iter_klu_x, reverse=True)[0]))                                            #, reverse=True
print('iter_klu_y: ' + str(sorted(iter_klu_y, reverse=True)[0]))
print('klu_iter_x: ' + str(sorted(klu_iter_x, reverse=True)[0]))
print('klu_iter_y: ' + str(sorted(klu_iter_y, reverse=True)[0]))
#print('equal_x: ' + str(sorted(equal_x, reverse=True)[0]))
#print('equal_y: ' + str(sorted(equal_y, reverse=True)[0]))
print('iter_zero_x: ' + str(sorted(iter_zero_x, reverse=True)[0]))
print('iter_zero_y: ' + str(sorted(iter_zero_y, reverse=True)[0]))
print('klu_zero_x: ' + str(sorted(klu_zero_x, reverse=True)[0]))
print('klu_zero_y: ' + str(sorted(klu_zero_y, reverse=True)[0]))
#print('equal_zero_x: ' + str(sorted(equal_zero_x)[0]))
#print('equal_zero_y: ' + str(sorted(equal_zero_y)[0]))

# plot a scatter plot + diagonal line
ax = plt.axes()
z = range(0,4000)
plt1 = ax.scatter(iter_klu_x, iter_klu_y, c='red', label='Iterative solver is faster than KLU', zorder=10, clip_on=False)
plt2 = ax.scatter(klu_iter_x, klu_iter_y, c='green', label='KLU is faster than Iterative solver', zorder=10, clip_on=False)
plt3 = ax.scatter(equal_x, equal_y, c='blue', label='Both are equally fast', zorder=10, clip_on=False)
plt4 = ax.scatter(iter_zero_x, iter_zero_y, marker='D', s=100, facecolors='none', edgecolors='green', label='Iterative solver failed completely to integrate the model', zorder=10, clip_on=False)
plt5 = ax.scatter(klu_zero_x, klu_zero_y, marker='D', s=100, facecolors='none', edgecolors='red', label='KLU failed completely to integrate the model', zorder=10, clip_on=False)
plt6 = ax.scatter(equal_zero_x, equal_zero_y, marker='D', s=100, facecolors='none', edgecolors='blue', label='Both failed to integrate the model', zorder=10, clip_on=False)
ax.plot(z)
ax.set_xlim([0.5, 4000])
ax.set_ylim([0.5, 200])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Iterative solver simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_ylabel('KLU simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_title('Iterative Solver vs. KLU Models', fontsize=24, fontweight='bold', pad=30)
ax.legend(loc=2)

leg = Legend(ax, [plt1, plt2, plt3, plt4, plt5, plt6], [str(round(len(iter_klu_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(klu_iter_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(equal_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(iter_zero_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(klu_zero_x)/166 * 100, 2)) + ' %',
                                                        str(round(len(equal_zero_x)/166 * 100, 2)) + ' %'], loc='lower right', frameon=True)
ax.add_artist(leg)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../bachelor_thesis/New_Figures/Figures_study_4/Iter_vs_KLU_Models_166SBML.pdf')

# show figure
plt.show()