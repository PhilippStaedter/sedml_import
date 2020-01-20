# scatter plot of the prediction settings against amici default settings

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from averageTime import *
import matplotlib.cm as cm

# important paths
base_path = '../paper_SolverSettings/WholeStudy'
Adams_base_path = base_path
BDF_base_path = base_path
#Adams_base_path = '../bachelor_thesis/SolverAlgorithm/Adams'
#BDF_base_path = '../bachelor_thesis/SolverAlgorithm/BDF'

# open .tsv files
list_directory_general = sorted(os.listdir(base_path))
list_directory_adams = []
list_directory_bdf = []
for iFile in range(0, int(len(list_directory_general)/2)):
    list_directory_adams.append(list_directory_general[iFile])
    list_directory_bdf.append(list_directory_general[iFile + int(len(list_directory_general)/2)])
#list_directory_adams = sorted(os.listdir(Adams_base_path))
#list_directory_bdf = sorted(os.listdir(BDF_base_path))

# create list of doubles for scatter plot
adams_bdf_x = []          # red
adams_bdf_y = []
bdf_adams_x = []          # green
bdf_adams_y = []
equal_x = []                    # yellow
equal_y = []
adams_zero_x = []
adams_zero_y = []
bdf_zero_x = []
bdf_zero_y = []
equal_zero_x = []
equal_zero_y = []

for iTsvFile in range(0, len(list_directory_adams)):
    adams_tsv_file = pd.read_csv(Adams_base_path + '/' + list_directory_adams[iTsvFile], sep='\t')
    bdf_tsv_file = pd.read_csv(BDF_base_path + '/' + list_directory_bdf[iTsvFile], sep='\t')

    # average from 210 to 166 models
    adams_tsv_file = averaging(adams_tsv_file)
    bdf_tsv_file = averaging(bdf_tsv_file)

    for iModel in range(0, len(adams_tsv_file['t_intern_ms'])):
        x_adams_data = adams_tsv_file['t_intern_ms'][iModel]
        y_bdf_data = bdf_tsv_file['t_intern_ms'][iModel]

        if x_adams_data != 0 and y_bdf_data != 0:
            if x_adams_data > y_bdf_data:
                bdf_adams_x.append(x_adams_data)
                bdf_adams_y.append(y_bdf_data)
            elif y_bdf_data > x_adams_data:
                adams_bdf_x.append(x_adams_data)
                adams_bdf_y.append(y_bdf_data)
            elif x_adams_data == y_bdf_data:
                equal_x.append(x_adams_data)
                equal_y.append(y_bdf_data)
        elif x_adams_data == 0 and y_bdf_data != 0:
            adams_zero_x.append(45000)
            adams_zero_y.append(y_bdf_data)
        elif x_adams_data != 0 and y_bdf_data == 0:
            bdf_zero_x.append(x_adams_data)
            bdf_zero_y.append(45000)
        elif x_adams_data == 0 and y_bdf_data == 0:
            equal_zero_x.append(45000)
            equal_zero_y.append(45000)

    # display progress
    print(iTsvFile)

# look for the biggest/smallest values
print('adams_bdf_x: ' + str(sorted(adams_bdf_x)[0]))                                            #, reverse=True
print('adams_bdf_y: ' + str(sorted(adams_bdf_y)[0]))
print('bdf_adams_x: ' + str(sorted(bdf_adams_x)[0]))
print('bdf_adams_y: ' + str(sorted(bdf_adams_y)[0]))
#print('equal_x: ' + str(sorted(equal_x, reverse=True)[0]))
#print('equal_y: ' + str(sorted(equal_y, reverse=True)[0]))
print('adams_zero_x: ' + str(sorted(adams_zero_x)[0]))
print('adams_zero_y: ' + str(sorted(adams_zero_y)[0]))
print('bdf_zero_x: ' + str(sorted(bdf_zero_x)[0]))
print('bdf_zero_y: ' + str(sorted(bdf_zero_y)[0]))
print('equal_zero_x: ' + str(sorted(equal_zero_x)[0]))
print('equal_zero_y: ' + str(sorted(equal_zero_y)[0]))

# plot a scatter plot + diagonal line
linestyle = (0, (2, 5, 2, 5))
linewidth = 1

fontsize = 22 - 4
labelsize = 18 - 4
titlesize = 30

alpha = 0.4
marker_size = 60

# Calculate the point density
# orange
xy = np.vstack([adams_bdf_x, adams_bdf_y])
zz = gaussian_kde(xy)(xy)
# blue
vw = np.vstack([bdf_adams_x, bdf_adams_y])
zzz = gaussian_kde(vw)(vw)
# orange edge
xxyy = np.vstack([adams_zero_x, adams_zero_y])
z_z_ = gaussian_kde(xxyy)(xxyy)
# blue edge
vvww = np.vstack([bdf_zero_x, bdf_zero_y])
z_z_z_ = gaussian_kde(vvww)(vvww)

ax = plt.axes([0.1, 0.1, 0.8, 0.8])
z = range(0,45000)
plt1 = ax.scatter(adams_bdf_x, adams_bdf_y, c=zz, cmap=cm.autumn_r, label='AM faster: ' + str(round(len(adams_bdf_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %', zorder=10, clip_on=False, alpha=alpha)
plt2 = ax.scatter(bdf_adams_x, bdf_adams_y, c=zzz, cmap=cm.winter_r, label='BDF faster: ' + str(round(len(bdf_adams_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %', zorder=10, clip_on=False, alpha=alpha)
plt3 = ax.scatter(equal_x, equal_y, c='grey', zorder=10, clip_on=False, alpha=alpha) # label='Both are equally good: ' + str(round(len(equal_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %',
plt4 = ax.scatter(adams_zero_x, adams_zero_y, c=z_z_, cmap=cm.winter_r, marker='D', s=marker_size, facecolors='none', edgecolors='blue', zorder=10, clip_on=False) # label='Adams-Moulton failed to integrate the model: ' + str(round(len(adams_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %',
plt5 = ax.scatter(bdf_zero_x, bdf_zero_y, c=z_z_z_, cmap=cm.autumn_r, s=marker_size, facecolors='none', edgecolors='orange', marker='D', zorder=10, clip_on=False) # label='BDF failed to integrate the model: ' + str(round(len(bdf_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %',
plt6 = ax.scatter(equal_zero_x, equal_zero_y, s=marker_size, facecolors='none', edgecolors='grey', marker='D', zorder=10, clip_on=False) # label='Both failed to integrate the model: ' + str(round(len(equal_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %',
ax.plot(z, c='black', zorder=20)
ax.set_xlim([0.2, 45000])
ax.set_ylim([0.2, 45000])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('AM simulation time [ms]', fontsize=fontsize)
ax.set_ylabel('BDF simulation time [ms]', fontsize=fontsize)
#ax.set_title('Adams-Moulton vs. BDF settings', fontsize=titlesize, fontweight='bold', pad=40)
lg = ax.legend(loc=2, fontsize=fontsize)
fr = lg.get_frame()
fr.set_lw(0.2)
#plt.colorbar(plt1, orientation='vertical', pad = 0.2)
#plt.colorbar(plt2, orientation='vertical', pad = 0.4)
plt.tick_params(labelsize=labelsize)
plt.gca().set_aspect('equal', adjustable='box')
ax.spines['top'].set_linestyle(linestyle)
ax.spines['top'].set_linewidth(linewidth)
ax.spines['right'].set_linestyle(linestyle)
ax.spines['right'].set_linewidth(linewidth)
ax.spines['top'].set_color('red')
ax.spines['right'].set_color('red')

# write text over axis
ax.text(55000, 500,'AM failed: ' + str(round(len(adams_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %', fontsize=fontsize, rotation=-90)
ax.text(30, 55000, 'BDF failed: ' + str(round(len(bdf_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %', fontsize=fontsize)
ax.text(20000, 80000, 'Both failed:' + str(round(len(equal_zero_x)/len(adams_tsv_file['t_intern_ms'])*10/7, 2)) + ' %', fontsize=fontsize, rotation=-45)
#ax.text(0.1, 70000, 'Adams-Moulton vs. BDF settings', fontsize=titlesize, fontweight='bold', pad=30)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
#plt.savefig('../bachelor_thesis/New_Figures/Figures_study_5/Adams_vs_BDF_2_166SBML.pdf')

# show figure
plt.show()