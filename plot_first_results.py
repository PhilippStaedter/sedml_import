# plot a bar plot for num_states and num_species
import matplotlib.pyplot as plt
import pandas as pd

# open two .tsv file
path = '../sbml2amici/stat_reac_par.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# take number of states for those models that worked
data_states_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_states_ok.append(tsv_file['states'][iLine])                 # no 'ignore_index=True' permitted

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_reactions_ok.append(tsv_file['reactions'][iLine])

# take number of parameters for those models that worked
data_parameters_ok = []
for iLine in range(0, len(tsv_file['id'])):
    data_parameters_ok.append(tsv_file['parameters'][iLine])

# histogram of states
plt.subplot(3,1,1)
plot1 = plt.hist(x=data_states_ok, range=[0,250], bins=200, log=True)
plt.xlim((None, 250))                                                                       # Froehlich2018: 1396
plt.ylim((None, 100))
plt.xlabel('Number of state variables')
plt.ylabel('Amount of models')

# histogram of reactions
plt.subplot(3,1,2)
plot2 = plt.hist(x=data_reactions_ok, range=[0,600], bins=200, log=True)
plt.xlim((None, 600))                                                                       # Froehlich2018: 2686
plt.ylim((None, 100))
plt.xlabel('Number of reactions')
plt.ylabel('Amount of models')

# histogram of parameters
plt.subplot(3,1,3)
plot3 = plt.hist(x=data_parameters_ok, range=[0,350], bins=200, log=True)
plt.xlim((None, 350))                                                                       # Froehlich2018: 4704
plt.ylim((None, 100))
plt.xlabel('Number of parameters')
plt.ylabel('Amount of models')

# better layout
plt.tight_layout()

# save figure
plt.savefig('../sbml2amici/Figures/zzz_Figures_new/stat_reac_par.png')

# show figure
plt.show()