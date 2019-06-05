# script to do a scatter plot of num_x vs. num_p

import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *

# open .tsv file from Tolerance study
path = '../bachelor_thesis/Tolerance/06_06.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# take number of states for those models that worked
num_x= []
for iLine in range(0, len(tsv_file['id'])):
    num_x.append(tsv_file['state_variables'][iLine])

# take number of parameter for those models that worked
num_p = []
for iLine in range(0, len(tsv_file['id'])):
    num_p.append(tsv_file['parameters'][iLine])


# scatter plot
plt.subplot(1,1,1)
plt.scatter(num_x, num_p, alpha=0.8, c='blue', edgecolors='none', s=30)
# plt.xscale("log")
# plt.yscale("log")
plt.xlabel('Number of state variables')
plt.ylabel('Number of parameters')
# ax.set_xscale('log')

# plot linear regression
a,b = linearRegression(tsv_file, 'state_variables', 'parameters')

# add linear regression to plot
x = []
for iCount in range(0, sorted(num_x, reverse=True)[0] + 1):
    x.append(iCount)
plt.plot(x, a + x*b, color='red')

# title
plt.title('Num_x vs. Num_p')

# removing top and right borders
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# adds major gridlines
plt.grid(color='grey', linestyle='-', linewidth=0.15, alpha=0.5)

# better layout
plt.tight_layout()

# save figure
plt.savefig('../sbml2amici/Figures/Num_x_vs_Num_p.png')

# show figure
plt.show()