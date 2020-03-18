import pandas as pd
import os
import matplotlib.pyplot as plt


all_abs_tol = ['03', '06', '06', '16', '12']
all_rel_tol = ['03', '06', '03', '08', '12']

counter_Tol_0 = []
counter_Tol_1 = []
counter_Tol_2 = []
counter_Tol_3 = []
counter_Tol_4 = []
for iTolerance in range(0, len(all_abs_tol)):
    abs_tol = all_abs_tol[iTolerance]
    rel_tol = all_rel_tol[iTolerance]
    adams_models = []
    bdf_models = []
    counters_Adams = []
    counters_BDF = []
    for Multistep in ['Adams', 'BDF']:
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
                        if Multistep == 'Adams':
                            adams_models.append(sedml_model + '_' + sbml_model)
                        elif Multistep == 'BDF':
                            bdf_models.append(sedml_model + '_' + sbml_model)
                    total_counter += 1
            print(tol_exp, counter, total_counter)
            tol_exps.append(tol_exp)
            if Multistep == 'Adams':
                counters_Adams.append(counter)
            elif Multistep == 'BDF':
                counters_BDF.append(counter)
    if iTolerance == 0:
        counter_Tol_0.append(counters_Adams)
        counter_Tol_0.append(counters_BDF)
    elif iTolerance == 1:
        counter_Tol_1.append(counters_Adams)
        counter_Tol_1.append(counters_BDF)
    elif iTolerance == 2:
        counter_Tol_2.append(counters_Adams)
        counter_Tol_2.append(counters_BDF)
    elif iTolerance == 3:
        counter_Tol_3.append(counters_Adams)
        counter_Tol_3.append(counters_BDF)
    elif iTolerance == 4:
        counter_Tol_4.append(counters_Adams)
        counter_Tol_4.append(counters_BDF)

plt.plot(tol_exps, counter_Tol_0[0], '-x', c='#d73027', label=f'AM_{all_abs_tol[0]}_{all_rel_tol[0]}')
plt.plot(tol_exps, counter_Tol_0[1], '-x', c='#f46d43', label=f'BDF_{all_abs_tol[0]}_{all_rel_tol[0]}')
plt.plot(tol_exps, counter_Tol_1[0], '-x', c='#fdae61', label=f'AM_{all_abs_tol[1]}_{all_rel_tol[1]}')
plt.plot(tol_exps, counter_Tol_1[1], '-x', c='#fee090', label=f'BDF_{all_abs_tol[1]}_{all_rel_tol[1]}')
plt.plot(tol_exps, counter_Tol_2[0], '-x', c='#ffffbf', label=f'AM_{all_abs_tol[2]}_{all_rel_tol[2]}')
plt.plot(tol_exps, counter_Tol_2[1], '-x', c='#e0f3f8', label=f'BDF_{all_abs_tol[2]}_{all_rel_tol[2]}')
plt.plot(tol_exps, counter_Tol_3[0], '-x', c='#abd9e9', label=f'AM_{all_abs_tol[3]}_{all_rel_tol[3]}')
plt.plot(tol_exps, counter_Tol_3[1], '-x', c='#74add1', label=f'BDF_{all_abs_tol[3]}_{all_rel_tol[3]}')
plt.plot(tol_exps, counter_Tol_4[0], '-x', c='#4575b4', label=f'AM_{all_abs_tol[4]}_{all_rel_tol[4]}')
plt.plot(tol_exps, counter_Tol_4[1], '-x', c='#2E2D66', label=f'BDF_{all_abs_tol[4]}_{all_rel_tol[4]}')

fontsize = 11
plt.legend(loc=2)
plt.gca().set_title(f'Comparison of all State Trajectories to JWS for AM vs BDF using all tolerances', fontsize=fontsize)
plt.gca().set_xlabel("Error Tolerance for comparing State Trajectories", fontsize=fontsize)
plt.gca().set_ylabel("Matching models", fontsize=fontsize)
plt.gcf().tight_layout()

# save plot
#plt.savefig(f"figures_paper/Study_1/compareStateTrajectories_summary_{abs_tol}_{rel_tol}.pdf")

# show plot
plt.show()