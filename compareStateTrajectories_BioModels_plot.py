import pandas as pd
import os
import matplotlib.pyplot as plt

all_abs_tol = ['16','14']
all_rel_tol = ['08','14']

counter_Tol_0 = []
counter_Tol_1 = []
counter_Tol_2 = []
for iTolerance in range(0, len(all_abs_tol)):
    abs_tol = all_abs_tol[iTolerance]
    rel_tol = all_rel_tol[iTolerance]
    adams_models = []
    bdf_models = []
    counters_Adams = []
    counters_BDF = []
    for Multistep in ['BDF']:           # 'Adams'
        print(Multistep)
        tol_exps = []
        for tol_exp in range(-20, 10):                # range(-20,10)
            tol = 10**tol_exp
            counter = 0
            total_counter = 0
            tol_str = f"{float(tol):.0e}"
            base_dir = f"COPASI_all_results_{Multistep}_{abs_tol}_{rel_tol}/COPASI_{tol_str}_{tol_str}"
            bio_models = sorted(os.listdir(base_dir))
            for bio_model in bio_models:
                filename = bio_model + "/" + "whole_error.csv"
                df = pd.read_csv('./' + base_dir  + '/' + filename, sep='\t')
                if df['trajectories_match'][0] == True:
                    counter += 1
                    if Multistep == 'Adams':
                        adams_models.append(bio_model)
                    elif Multistep == 'BDF':
                        bdf_models.append(bio_model)
                total_counter += 1
            print(tol_exp, counter, total_counter)
            tol_exps.append(tol_exp)
            if Multistep == 'Adams':
                counters_Adams.append(counter)
            elif Multistep == 'BDF':
                counters_BDF.append(counter)
    if iTolerance == 0:
        #counter_Tol_0.append(counters_Adams)
        counter_Tol_0.append(counters_BDF)
    elif iTolerance == 1:
        #counter_Tol_1.append(counters_Adams)
        counter_Tol_1.append(counters_BDF)
    elif iTolerance == 2:
        counter_Tol_2.append(counters_Adams)
        counter_Tol_2.append(counters_BDF)

plt.plot(tol_exps, counter_Tol_0[0], '-x', c='blue', label=f'BDF_{all_abs_tol[0]}_{all_rel_tol[0]}')
plt.plot(tol_exps, counter_Tol_1[0], '-x', c='green', label=f'BDF_{all_abs_tol[1]}_{all_rel_tol[1]}')
#plt.plot(tol_exps, counter_Tol_0[0], '-x', c='orange', label=f'AM_{all_abs_tol[0]}_{all_rel_tol[0]}')
#plt.plot(tol_exps, counter_Tol_0[1], '-x', c='blue', label=f'BDF_{all_abs_tol[0]}_{all_rel_tol[0]}')
#plt.plot(tol_exps, counter_Tol_1[0], '-x', c='red', label=f'AM_{all_abs_tol[1]}_{all_rel_tol[1]}')
#plt.plot(tol_exps, counter_Tol_1[1], '-x', c='green', label=f'BDF_{all_abs_tol[1]}_{all_rel_tol[1]}')
#plt.plot(tol_exps, counter_Tol_2[0], '-x', c='purple', label=f'AM_{all_abs_tol[2]}_{all_rel_tol[2]}')
#plt.plot(tol_exps, counter_Tol_2[1], '-x', c='black', label=f'BDF_{all_abs_tol[2]}_{all_rel_tol[2]}')
plt.legend(loc=2)
plt.gca().set_title(f'Comparison of all State Trajectories to JWS for AM vs BDF using all tolerances', fontsize=11)
plt.gca().set_xlabel("Acceptance Threshold for matching State Trajectories", fontsize=11)
plt.gca().set_ylabel("Matching models", fontsize=11)
plt.gcf().tight_layout()
#plt.savefig(f"figures_paper/Study_1/compareStateTrajectories_summary_{abs_tol}_{rel_tol}.pdf")
plt.show()