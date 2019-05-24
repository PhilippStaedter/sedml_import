# plot a bar plot for 16_08_9_2 vs state variables
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# open .tsv file
path = '../sbml2amici/simulation_16_08_9_2.tsv'
tsv_file = pd.read_csv(path, sep='\t')

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


# scatter plot of data
plt.scatter(state_variable, intern_time, alpha=0.8, c='blue', edgecolors='none', s=30, label='Intern Time')
plt.scatter(state_variable, extern_time, alpha=0.8, c='red', edgecolors='none', s=30, label='Extern Time')
plt.xlabel('Amount of state variables')
plt.ylabel('Simulation time in milliseconds')

# title + legend
plt.title('Intern vs Extern')
plt.legend(loc=2)

# better layout
plt.tight_layout()

# save figure
plt.savefig('../sbml2amici/Figures/Intern_vs_Extern.png')

# show figure
plt.show()
