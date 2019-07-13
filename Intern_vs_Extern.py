# plot a bar plot for 16_08_9_2 vs state variables
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from averageTime import *

# open .tsv file
path = '../bachelor_thesis/Tolerance/16_08.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# get new .tsv file
tsv_file = averaging(tsv_file)

# take intern_time
intern_time = []
for iLine in range(len(tsv_file['id']) - 1):
    intern_time.append(tsv_file['t_intern_ms'][iLine])

# take extern_time
extern_time = []
for iLine in range(len(tsv_file['id']) - 1):
    extern_time.append(tsv_file['t_extern_ms'][iLine])

# take number of state variables
state_variable = []
for iLine in range(len(tsv_file['id']) - 1):
    state_variable.append(tsv_file['state_variables'][iLine])

# take number of reactions
parameters = []
for iLine in range(len(tsv_file['id']) - 1):
    parameters.append(tsv_file['parameters'][iLine])


##### several plots
plt.subplot(2,2,1)
# scatter plot of data
plt.scatter(state_variable, intern_time, alpha=0.8, c='blue', edgecolors='none', s=30, label='Intern Time')
plt.scatter(state_variable, extern_time, alpha=0.8, c='red', edgecolors='none', s=30, label='Extern Time')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 2000))
plt.ylim((0.3, 2000))
plt.ylabel('Simulation time in milliseconds')

# title + legend
plt.title('Intern vs Extern Timekeeping')
plt.legend(loc=2)

#######
plt.subplot(2,2,3)
# percental deviation
time_difference = []
for iTime in range(0, len(intern_time)):
    time_difference.append(extern_time[iTime] - intern_time[iTime])
plt.scatter(state_variable, time_difference, alpha=0.8, c='green', edgecolors='none', s=30)
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 2000))
plt.ylim((0.1, 100))
plt.xlabel('Number of state variables')
plt.ylabel('Time difference in milliseconds')

# title + legend
plt.title('Intern vs Extern Time-derivation')

######
plt.subplot(2,2,2)
# scatter plot of data
plt.scatter(parameters, intern_time, alpha=0.8, c='blue', edgecolors='none', s=30, label='Intern Time')
plt.scatter(parameters, extern_time, alpha=0.8, c='red', edgecolors='none', s=30, label='Extern Time')
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 5000))
plt.ylim((0.3, 2000))

# title + legend
plt.title('Intern vs Extern Timekeeping')
plt.legend(loc=2)

#######
plt.subplot(2,2,4)
# percental deviation
time_difference = []
for iTime in range(0, len(intern_time)):
    time_difference.append(extern_time[iTime] - intern_time[iTime])
plt.scatter(parameters, time_difference, alpha=0.8, c='green', edgecolors='none', s=30)
plt.xscale("log")
plt.yscale("log")
plt.xlim((0.3, 5000))
plt.ylim((0.1, 100))
plt.xlabel('Number of parameters')

# title + legend
plt.title('Intern vs Extern Time-derivation')



###########
# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Intern_vs_Extern.pdf')

# show figure
plt.show()