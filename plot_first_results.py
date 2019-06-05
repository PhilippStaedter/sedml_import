# plot a bar plot for num_states and num_species
import matplotlib.pyplot as plt
import pandas as pd

# open .tsv file
path = '../sbml2amici/table_with_parameter_and_time.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# take number of states for those models that worked
data_states_ok = []
for iLine in range(0, len(tsv_file['id'])):
    if tsv_file['error_message'][iLine] == 'OK':
        data_states_ok.append(tsv_file['states'][iLine])                 # no 'ignore_index=True' permitted

# take number of reactions for those models that worked
data_reactions_ok = []
for iLine in range(0, len(tsv_file['id'])):
    if tsv_file['error_message'][iLine] == 'OK':
        data_reactions_ok.append(tsv_file['reactions'][iLine])

# take number of parameter for those models that worked
data_parameter_ok = []
for iLine in range(0, len(tsv_file['id'])):
    if tsv_file['error_message'][iLine] == 'OK':
        data_parameter_ok.append(tsv_file['parameters'][iLine])

# histogram of states
plt.subplot(3,1,1)
plot1 = plt.hist(x=data_states_ok, range=[0,100], bins=100, log=True)
plt.xlim((None, 100))
plt.ylim((None, 100))
plt.xlabel('Number of state variables')
plt.ylabel('Amount of models')

# histogram of reactions
plt.subplot(3,1,2)
plot2 = plt.hist(x=data_reactions_ok, bins=100, log=True)
plt.xlim((None, 100))
plt.ylim((None, 100))
plt.xlabel('Number of reactions')
plt.ylabel('Amount of models')

# histogram of parameter
plt.subplot(3,1,3)
plot3 = plt.hist(x=data_parameter_ok, bins=100, log=True)
plt.xlim((None, 150))
plt.ylim((None, 100))
plt.xlabel('Number of parameters')
plt.ylabel('Amount of models')

# better layout
plt.tight_layout()

# save figure
plt.savefig('../sbml2amici/Figures/First_Result_log_scale.png')

# show figure
plt.show()