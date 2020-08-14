# Main Manuscript Plot --- Figure 1
# combined plot for study one

import matplotlib.pyplot as plt
import pandas as pd
from averageTime import *
import numpy as np


# all axes objects
fontsize = 9
labelsize = 9

rotation = 90
left = 0.07
bottom = 0.1
width = 0.43
height = 0.75
row_factor = 0.48
column_factor = 0
rotation_factor = 70
alpha = 1

ax1 = plt.axes([left, bottom, width, height])
ax2 = plt.axes([left + row_factor, bottom, width, height])


################ plot bar plot #################
# open one .tsv file from 'WholeStudy'
path = '../sbml2amici/NEW_stat_reac_par_paper.tsv'
tsv_file = pd.read_csv(path, sep='\t')
tsv_file = averaging(tsv_file)

# no BioModels yet + delete nans at the end
tsv_file = tsv_file
tsv_file = tsv_file.reset_index()
del tsv_file['index']


# take number of states for those models that worked
data_states_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_states_ok.append(np.log10(tsv_file['state_variables'][iLine]))

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_reactions_ok.append(np.log10(tsv_file['reactions'][iLine]))


# histogram of states
bins = 80
plot1 = ax1.hist(x=data_states_ok, range=[-1,4], bins=bins, log=True)
ax1.set_xlim((-0.1, 4))
ax1.set_ylim((0.5, 25))
ax1.set_xticklabels(['', r'$10^{0}$', '', r'$10^{1}$', '', r'$10^{2}$', '', r'$10^{3}$', '', r'$10^{4}$'])
ax1.set_xlabel('Number of state variables', fontsize=fontsize)
ax1.set_ylabel('Number of models', fontsize=fontsize)
ax1.tick_params(labelsize=labelsize)
ax1.set_yscale('linear')

# plot text 'B'
ax1.text(-0.22, 1, 'B', fontsize=labelsize + 3, transform=ax1.transAxes)

# histogram of reactions
plot2 = ax2.hist(x=data_reactions_ok, range=[-1,4], bins=bins, log=True)
ax2.set_xlim((-0.1, 4))
ax2.set_ylim((0.5, 25))
ax2.set_xticklabels(['', r'$10^{0}$', '', r'$10^{1}$', '', r'$10^{2}$', '', r'$10^{3}$', '', r'$10^{4}$'])
ax2.set_xlabel('Number of reactions', fontsize=fontsize)
ax2.set_ylabel('Number of models', fontsize=fontsize)
ax2.tick_params(labelsize=labelsize)
ax2.set_yscale('linear')

# make all top and right boxlines invisible
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)


# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# show figure
plt.show()
