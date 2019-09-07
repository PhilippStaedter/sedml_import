# scatter plot of the prediction settings against amici default settings

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from averageTime import *

# important paths
Adams_base_path = '../bachelor_thesis/SolverAlgorithm/Adams'
BDF_base_path = '../bachelor_thesis/SolverAlgorithm/BDF'

# open .tsv files
list_directory_adams = sorted(os.listdir(Adams_base_path))
list_directory_bdf = sorted(os.listdir(BDF_base_path))

# create list of doubles for scatter plot
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

for iTsvFile in range(0, len(list_directory_adams)):
    adams_tsv_file = pd.read_csv(Adams_base_path + '/' + list_directory_adams[iTsvFile], sep='\t')
    bdf_tsv_file = pd.read_csv(BDF_base_path + '/' + list_directory_bdf[iTsvFile], sep='\t')

    # average from 210 to 166 models
    adams_tsv_file = averaging(adams_tsv_file)
    bdf_tsv_file = averaging(bdf_tsv_file)

    for iModel in range(0, len(adams_tsv_file['t_intern_ms'])):
        x_adams_data = adams_tsv_file['t_intern_ms'][iModel]
        y_bdf_data = bdf_tsv_file['t_intern_ms'][iModel]

        if x_adams_data != 0 and y_bdf_data != 0:
            if x_adams_data > y_bdf_data:
                bdf_adams_x.append(x_adams_data)
                bdf_adams_y.append(y_bdf_data)
            elif y_bdf_data > x_adams_data:
                adams_bdf_x.append(x_adams_data)
                adams_bdf_y.append(y_bdf_data)
            elif x_adams_data == y_bdf_data:
                equal_x.append(x_adams_data)
                equal_y.append(y_bdf_data)
        elif x_adams_data == 0 and y_bdf_data != 0:
            adams_zero_x.append(40000)
            adams_zero_y.append(y_bdf_data)
        elif x_adams_data != 0 and y_bdf_data == 0:
            bdf_zero_x.append(x_adams_data)
            bdf_zero_y.append(40000)
        elif x_adams_data == 0 and y_bdf_data == 0:
            equal_zero_x.append(40000)
            equal_zero_y.append(40000)

    # display progress
    print(iTsvFile)

# look for the biggest/smallest values
print('adams_bdf_x: ' + str(sorted(adams_bdf_x)[0]))                                            #, reverse=True
print('adams_bdf_y: ' + str(sorted(adams_bdf_y)[0]))
print('bdf_adams_x: ' + str(sorted(bdf_adams_x)[0]))
print('bdf_adams_y: ' + str(sorted(bdf_adams_y)[0]))
#print('equal_x: ' + str(sorted(equal_x, reverse=True)[0]))
#print('equal_y: ' + str(sorted(equal_y, reverse=True)[0]))
print('adams_zero_x: ' + str(sorted(adams_zero_x)[0]))
print('adams_zero_y: ' + str(sorted(adams_zero_y)[0]))
print('bdf_zero_x: ' + str(sorted(bdf_zero_x)[0]))
print('bdf_zero_y: ' + str(sorted(bdf_zero_y)[0]))
print('equal_zero_x: ' + str(sorted(equal_zero_x)[0]))
print('equal_zero_y: ' + str(sorted(equal_zero_y)[0]))

# plot a scatter plot + diagonal line
ax = plt.axes()
z = range(0,40000)
plt1 = ax.scatter(adams_bdf_x, adams_bdf_y, c='red', label='Adams default setting is better than the prediction', zorder=10, clip_on=False)
plt2 = ax.scatter(bdf_adams_x, bdf_adams_y, c='green', label='Prediction is better than Adams default setting', zorder=10, clip_on=False)
plt3 = ax.scatter(equal_x, equal_y, c='blue', label='Both are equally good', zorder=10, clip_on=False)
plt4 = ax.scatter(adams_zero_x, adams_zero_y, c='green', marker='s', label='Adams default failed to integrate the model', zorder=10, clip_on=False)
plt5 = ax.scatter(bdf_zero_x, bdf_zero_y, c='red', marker='s', label='Prediction setting failed to integrate the model', zorder=10, clip_on=False)
plt6 = ax.scatter(equal_zero_x, equal_zero_y, c='blue', marker='s', label='Both failed to integrate the model', zorder=10, clip_on=False)
ax.plot(z)
ax.set_xlim([0.5, 40000])
ax.set_ylim([0.5, 40000])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Adams default simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_ylabel('BDFs simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_title('Adams-Mouton vs. BDF settings', fontsize=24, fontweight='bold', pad=30)
ax.legend(loc=2)

leg = Legend(ax, [plt1, plt2, plt3, plt4, plt5, plt6], [str(round(len(adams_bdf_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %',
                                                        str(round(len(bdf_adams_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %',
                                                        str(round(len(equal_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %',
                                                        str(round(len(adams_zero_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %',
                                                        str(round(len(bdf_zero_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %',
                                                        str(round(len(equal_zero_x)/len(adams_tsv_file['t_intern_ms'])*5, 2)) + ' %'], loc='lower right', frameon=True)
ax.add_artist(leg)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../bachelor_thesis/New_Figures/Figures_study_5/Adams_vs_BDF_2_166SBML.pdf')

# show figure
plt.show()