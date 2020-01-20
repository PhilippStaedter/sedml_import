# plot a bar plot for num_states and num_species
import matplotlib.pyplot as plt
import pandas as pd
from averageTime import *

# open two .tsv file
path = '../sbml2amici/NEW_stat_reac_par_paper.tsv'
tsv_file = pd.read_csv(path, sep='\t')
tsv_file = averaging(tsv_file)

# no BioModels yet + delete nans at the end
tsv_file = tsv_file#[27:423]
tsv_file = tsv_file.reset_index()
del tsv_file['index']


# take number of states for those models that worked
data_states_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_states_ok.append(tsv_file['state_variables'][iLine])                 # no 'ignore_index=True' permitted

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_reactions_ok.append(tsv_file['reactions'][iLine])

# take number of parameters for those models that worked
data_parameters_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_parameters_ok.append(tsv_file['parameters'][iLine])


# histogram of states
fontsize = 16
labelsize = 16
bins = 200

rotation = 90
left = 0.1
bottom = 0.7
width = 0.8
height = 0.2
row_factor = 0.45
column_factor = 0.1
rotation_factor = 70
alpha = 1

# plots
ax1 = plt.axes([left, bottom, width, height])
ax2 = plt.axes([left, bottom - column_factor - height, width, height])
ax3 = plt.axes([left, bottom - 2 * column_factor - 2 * height, width, height])

#plt.subplot(3,1,1)
# add title
#plt.title('Basic properties of all models', fontsize=20)
plot1 = ax1.hist(x=data_states_ok, range=[1,2000], bins=10*bins, log=True) # range=[0,250],
ax1.set_xscale('log')
ax1.set_xlim((None, 2000)) #250 #100                                                                       # Froehlich2018: 1396
ax1.set_ylim((0.5, 150))
ax1.set_xlabel('Number of state variables', fontsize=fontsize)
ax1.set_ylabel('Amount of models', fontsize=fontsize)
ax1.tick_params(labelsize=labelsize)

# histogram of reactions
#plt.subplot(3,1,2)
plot2 = ax2.hist(x=data_reactions_ok, range=[1,3000], bins=15*bins, log=True) # range=[0,600],
ax2.set_xscale('log')
ax2.set_xlim((None, 3000)) #600 #100                                                                       # Froehlich2018: 2686
ax2.set_ylim((0.5, 150))
ax2.set_xlabel('Number of reactions', fontsize=fontsize)
ax2.set_ylabel('Amount of models', fontsize=fontsize)
ax2.tick_params(labelsize=labelsize)

# histogram of parameters
#plt.subplot(3,1,3)
plot3 = ax3.hist(x=data_parameters_ok, range=[1,5000], bins=25*bins, log=True) # range=[0,350],
ax3.set_xscale('log')
ax3.set_xlim((None, 5000)) #350 #1000                                                                       # Froehlich2018: 4704
ax3.set_ylim((0.5, 150))
ax3.set_xlabel('Number of parameters',  fontsize=fontsize)
ax3.set_ylabel('Amount of models', fontsize=fontsize)
ax3.tick_params(labelsize=labelsize)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../paper_SOlverSettings/Figures/Study_1/stat_reac_par_ylog.pdf')

# show figure
plt.show()