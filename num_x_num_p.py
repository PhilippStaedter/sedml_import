# script to do a scatter plot of num_x vs. num_p

import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *

# open .tsv file from Tolerance study
path = '../bachelor_thesis/Tolerance/08_06.tsv'
tsv_file = pd.read_csv(path, sep='\t')

# take number of states for those models that worked
num_x= []
for iLine in range(24, len(tsv_file['id'])):                                        # switch between 0 and 24
    num_x.append(tsv_file['state_variables'][iLine])

# take number of parameter for those models that worked
num_p = []
for iLine in range(24, len(tsv_file['id'])):                                        # switch between 0 and 24
    num_p.append(tsv_file['parameters'][iLine])


# scatter plot
plt.subplot(1,1,1)
plt.scatter(num_x, num_p, alpha=0.8, c='blue', edgecolors='none', s=30)

# for whole figure
plt.xlim(-5, 255)                                                                   # switch between section and whole figure
plt.ylim(-10, 360)

# for section
#plt.xlim(-5, 80)
#plt.ylim(-10, 150)

# plt.xscale("log")
# plt.yscale("log")
plt.xlabel('Number of state variables')
plt.ylabel('Number of parameters')
# ax.set_xscale('log')

# plot linear regression
a,b = linearRegression(tsv_file, 'state_variables', 'parameters')

# add linear regression to plot
x = []
try:
    rangeNumber = np.asarray([sorted(num_x , reverse=True)[0] + 1], dtype=np.int64)
except:
    rangeNumber = np.asarray([sorted(num_x, reverse=True)[1] + 1], dtype=np.int64)

for iCount in range(0, rangeNumber[0]):
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
plt.savefig('../sbml2amici/Figures/Num_x_vs_Num_p_whole_before_BioModels_2.png')

# show figure
plt.show()