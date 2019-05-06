# plot a bar plot for num_states and num_species
import matplotlib.pyplot as plt
import pandas as pd

# open .tsv file
path = '../sbml2amici/table.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# take number of states for those models that worked
data_states_ok = []
for iLine in range(len(tsv_file['id']) - 1):
    if tsv_file['error_message'][iLine] == 'OK':
        data_states_ok.append(tsv_file['states'][iLine])                 # no 'ignore_index=True' permitted

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(len(tsv_file['id']) - 1):
    if tsv_file['error_message'][iLine] == 'OK':
        data_reactions_ok.append(tsv_file['reactions'][iLine])

# histogram of states
plt.subplot(2,1,1)
plot1 = plt.hist(x=data_states_ok, bins=100)
plt.xlabel('Amount of states')
plt.ylabel('Amount of models')

# histogram of reactions
plt.subplot(2,1,2)
plot2 = plt.hist(x=data_reactions_ok, bins=100)
plt.xlabel('Amount of reactions')
plt.ylabel('Amount of models')

# better layout
plt.tight_layout()

# save figure
plt.savefig('../sbml2amici/Figures/First_Result.png')

# show figure
plt.show()