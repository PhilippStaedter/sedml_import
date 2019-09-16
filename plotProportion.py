# sees how the simulation time scales with the number of state variables

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
adams_state_x = []          # red
adams_time_y = []
bdf_state_x = []          # green
bdf_time_y = []

for iTsvFile in range(0, len(list_directory_adams)):
    adams_tsv_file = pd.read_csv(Adams_base_path + '/' + list_directory_adams[iTsvFile], sep='\t')
    bdf_tsv_file = pd.read_csv(BDF_base_path + '/' + list_directory_bdf[iTsvFile], sep='\t')

    # average from 210 to 166 models
    adams_tsv_file = averaging(adams_tsv_file)
    bdf_tsv_file = averaging(bdf_tsv_file)

    for iModel in range(0, len(adams_tsv_file['t_intern_ms'])):
        x_adams_state = adams_tsv_file['t_intern_ms'][iModel]
        y_adams_time = adams_tsv_file['state_variables'][iModel]
        x_bdf_state = bdf_tsv_file['t_intern_ms'][iModel]
        y_bdf_time = bdf_tsv_file['state_variables'][iModel]

        # exclude zeros
        if y_adams_time != 0:
            adams_state_x.append(x_adams_state)
            adams_time_y.append(y_adams_time)
        if y_bdf_time != 0:
            bdf_state_x.append(x_bdf_state)
            bdf_time_y.append(y_bdf_time)

    print(iTsvFile)

# plot a customized scatter plot
left = 0.1
bottom = 0.5
width = 0.4
height = 0.33
row_factor = 0.44
column_factor = 0.41
rotation_factor = 70

for iCounter in range(0,2):

    if iCounter == 0:
        ax1 = plt.axes([left, bottom, width, height])
        ax1.text(0.35, 1.05, 'State Variables', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        #ax1.tick_params(labelbottom=False)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

        # scatter plot
        ax1.set_xlim([0.5, 1500])
        ax1.set_ylim([0.1, 50000])
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.scatter(adams_state_x, adams_time_y, alpha=0.8, c='red', edgecolors='none', s=30, label='Adams')

        # plot two legends
        leg1 = ax1.legend(loc=2)

    if iCounter == 1:
        ax1 = plt.axes([left + iCounter * row_factor, bottom, width, height])
        ax1.text(0.35, 1.05, 'State Variables', fontsize=14, fontweight='bold', transform=ax1.transAxes)
        #ax1.tick_params(labelbottom=False)
        ax1.text(-0.12, 0.85, 'Simulation Time [ms]', fontsize=14, fontweight='bold', transform=ax1.transAxes, rotation=90)

        # scatter plot
        ax1.set_xlim([0.5, 1500])
        ax1.set_ylim([0.1, 50000])
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.scatter(bdf_state_x, bdf_time_y, alpha=0.8, c='green', edgecolors='none', s=30, label='BDF')

        # plot two legends
        leg1 = ax1.legend(loc=2)


# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../bachelor_thesis/New_Figures/Figures_study_5/Scale_Scale_Adams_BDF_2_166SBML.pdf')

# show figure
plt.show()
