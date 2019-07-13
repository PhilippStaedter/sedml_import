# script to do a scatter plot of num_x vs. num_p

import matplotlib.pyplot as plt
import pandas as pd
from LinearRegression import *

# open .tsv file from Tolerance study
path = '../sbml2amici/stat_reac_par.tsv'
tsv_file = pd.read_csv(path, sep='\t')

########### only for comparison ####################
num_x_bio= []
for iLine in range(0, 27):
    num_x_bio.append(tsv_file['states'][iLine])

num_p_bio = []
for iLine in range(0, 27):
    num_p_bio.append(tsv_file['parameters'][iLine])

####################################################
# take number of states for those models that are correct
num_x= []
for iLine in range(27, len(tsv_file['id'])):                                        # switch between 0 and 27
    num_x.append(tsv_file['states'][iLine])

# take number of parameter for those models that are correct
num_p = []
for iLine in range(27, len(tsv_file['id'])):                                        # switch between 0 and 27
    num_p.append(tsv_file['parameters'][iLine])


# scatter plot
plt.subplot(1,1,1)
not_bio = plt.scatter(num_x, num_p, alpha=0.8, c='blue', edgecolors='none', s=30)
bio = plt.scatter(num_x_bio, num_p_bio, alpha=0.8, c='red', edgecolors='none', s=30)

# for section 1 figure
plt.xlim(-5, 250)                                                                   # switch between section and whole figure
plt.ylim(-10, 450)

# for section 2 figure
plt.xlim(-5, 80)
plt.ylim(-10, 200)

# for section 3 figure
plt.xlim(-5, 20)
plt.ylim(-10, 40)

# plt.xscale("log")
# plt.yscale("log")
plt.xlabel('Number of state variables')
plt.ylabel('Number of parameters')
# ax.set_xscale('log')

# plot linear regression
a,b,d,e = linearRegression(tsv_file, 'states', 'parameters')

# add linear regression to plot
x = []
try:
    rangeNumber = np.asarray([sorted(num_x_bio , reverse=True)[0] + 1], dtype=np.int64)
except:
    rangeNumber = np.asarray([sorted(num_x_bio, reverse=True)[1] + 1], dtype=np.int64)

for iCount in range(0, rangeNumber[0]):
    x.append(iCount)
reg1 = plt.plot(x, a + x*b, color='blue')

############## only for comparison ######
reg2 = plt.plot(x, d + x*e, color='red')

#########################################
# title
plt.title('Num_x vs. Num_p')

# removing top and right borders
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# adds major gridlines
plt.grid(color='grey', linestyle='-', linewidth=0.15, alpha=0.5)

################### only for comparison ##################################################################################################################################
# adds legend
plt.legend((not_bio, bio, reg1[0], reg2[0]), ('all models from JWS only', 'all models from BioModels-Database only',
                                              'slope: ' + str(round(b[0],4)), 'slope: ' + str(round(e[0],4))), loc=2, frameon=False)

##########################################################################################################################################################################
# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../sbml2amici/Figures/zzz_Figures_new/Num_x_vs_Num_p_section_3_with_BioModels_regression.pdf')

# show figure
plt.show()