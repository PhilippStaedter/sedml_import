# scatter plot of the prediction settings against amici default settings

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from averageTime import *

# important paths
amici_default_path = '../bachelor_thesis/SolverAlgorithm/Total/2_9_16_08.tsv'
predictor_path = '../bachelor_thesis/SolverAlgorithm/Total/2_9_08_06.tsv'

# open .tsv files
amici_tsv_file = pd.read_csv(amici_default_path, sep='\t')
predictor_tsv_file = pd.read_csv(predictor_path, sep='\t')

# average from 210 to 166 models
amici_tsv_file = averaging(amici_tsv_file)
predictor_tsv_file = averaging(predictor_tsv_file)

# create list of tupels for scatter plot
amici_predictor_x = []          # red
amici_predictor_y = []
predictor_amici_x = []          # green
predictor_amici_y = []
equal_x = []                    # yellow
equal_y = []
for iModel in range(0, len(amici_tsv_file['t_intern_ms'])):
    x_amici_data = amici_tsv_file['t_intern_ms'][iModel]
    y_predictor_data = predictor_tsv_file['t_intern_ms'][iModel]

    if x_amici_data > y_predictor_data:
        predictor_amici_x.append(x_amici_data)
        predictor_amici_y.append(y_predictor_data)
    elif y_predictor_data > x_amici_data:
        amici_predictor_x.append(x_amici_data)
        amici_predictor_y.append(y_predictor_data)
    elif x_amici_data == y_predictor_data:
        equal_x.append(x_amici_data)
        equal_y.append(y_predictor_data)

# plot a scatter plot + diagonal line
ax = plt.axes()
z = range(0,200)
plt1 = ax.scatter(amici_predictor_x, amici_predictor_y, c='red', label='Amic default setting is better than the prediction')
plt2 = ax.scatter(predictor_amici_x, predictor_amici_y, c='green', label='Prediction is better than Amicis default setting')
plt3 = ax.scatter(equal_x, equal_y, c='blue', label='Both are equally good')
ax.plot(z)
ax.set_xlim([0.5, 250])
ax.set_ylim([0.5, 250])
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Amicis default simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_ylabel('Predictors simulation time [ms]', fontsize=12, fontweight='bold')
ax.set_title('Amici default vs. predictor settings', fontsize=24, fontweight='bold')
ax.legend(loc=2)

# second legend
#second_legend = plt.legend(handles=[plt1, plt2, plt3], loc='lower right')
leg = Legend(ax, [plt1, plt2, plt3], [str(round(len(amici_predictor_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                      str(round(len(predictor_amici_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %',
                                      str(round(len(equal_x)/len(amici_tsv_file['t_intern_ms'])*100, 2)) + ' %'], loc='lower right', frameon=True)
ax.add_artist(leg)

# better layout
plt.tight_layout()

# change plotting size
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

# save figure
plt.savefig('../bachelor_thesis/New_Figures/Figures_study_5/Predictor_vs_Amici_166SBML.pdf')

# show figure
plt.show()