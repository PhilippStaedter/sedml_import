import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

all_abs_tol = ['03', '06', '12']    # 16    # 6
all_rel_tol = ['03', '06', '12']    # 8     # 3

counter_Tol_0 = []
counter_Tol_1 = []
counter_Tol_2 = []
counter_Tol_3 = []
counter_Tol_4 = []
for iTolerance in range(0, len(all_abs_tol)):
    abs_tol = all_abs_tol[iTolerance]
    rel_tol = all_rel_tol[iTolerance]
    bdf_models = []
    counters_BDF = []
    for Multistep in ['BDF']:
        print(Multistep)
        tol_exps = []
        for tol_exp in range(-20, 10):                # range(-20,10)
            tol = 10**tol_exp
            counter = 0
            total_counter = 0
            tol_str = f"{float(tol):.0e}"
            base_dir = f"json_files_all_results_{Multistep}_{abs_tol}_{rel_tol}/json_files_{tol_str}_{tol_str}"
            sedml_models = os.listdir(base_dir)
            for sedml_model in sedml_models:
                sedml_dir = base_dir + "/" + sedml_model
                sbml_models = os.listdir(sedml_dir)
                for sbml_model in sbml_models:
                    sbml_dir = sedml_dir + "/" + sbml_model
                    filename = sbml_dir + "/" + "whole_error.csv"
                    df = pd.read_csv(filename, sep='\t')
                    if df['trajectories_match'][0] == True:
                        counter += 1
                        bdf_models.append(sedml_model + '_' + sbml_model)
                    total_counter += 1
            print(tol_exp, counter, total_counter)
            tol_exps.append(tol_exp)
            counters_BDF.append(counter)
    if iTolerance == 0:
        counter_Tol_0.append(counters_BDF)
    elif iTolerance == 1:
        counter_Tol_1.append(counters_BDF)
    elif iTolerance == 2:
        counter_Tol_2.append(counters_BDF)
    elif iTolerance == 3:
        counter_Tol_3.append(counters_BDF)
    elif iTolerance == 4:
        counter_Tol_4.append(counters_BDF)

plt.plot(tol_exps, counter_Tol_0[0], '-x', c='#d7191c', label=f'abs. tol.: {all_abs_tol[0]}, rel. tol.: {all_rel_tol[0]}')
plt.plot(tol_exps, counter_Tol_1[0], '-x', c='#fdae61', label=f'abs. tol.: {all_abs_tol[1]}, rel. tol.: {all_rel_tol[1]}')
plt.plot(tol_exps, counter_Tol_2[0], '-x', c='#ffffbf', label=f'abs. tol.: {all_abs_tol[2]}, rel. tol.: {all_rel_tol[2]}')
plt.plot(tol_exps, counter_Tol_3[0], '-x', c='#abd9e9', label=f'abs. tol.: {all_abs_tol[3]}, rel. tol.: {all_rel_tol[3]}')
plt.plot(tol_exps, counter_Tol_4[0], '-x', c='#2c7bb6', label=f'abs. tol.: {all_abs_tol[4]}, rel. tol.: {all_rel_tol[4]}')

# local properties
plt.xticks(np.array([-20, -15, -10, -5, 0, 5, 10]), (r'$10^{-20}$', r'$10^{-15}$', r'$10^{-10}$', r'$10^{-5}$', r'$10^{0}$', r'$10^{5}$', r'$10^{10}$'))

# global properties
plt.legend(loc=2)
#plt.gca().set_title(f'Comparison of all State Trajectories to JWS for AM vs BDF using all tolerances')
plt.gca().set_xlabel("Error Tolerance for comparing State Trajectories")
plt.gca().set_ylabel("Matching models")
plt.gcf().tight_layout()
#plt.savefig(f"figures_paper/Study_1/compareStateTrajectories_summary_{abs_tol}_{rel_tol}.pdf")
plt.show()