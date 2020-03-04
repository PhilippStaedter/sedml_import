import pandas as pd
import os
import matplotlib.pyplot as plt


adams_models = []
bdf_models = []
for Multistep in ['Adams']: #,'BDF']:
    print(Multistep)
    counters = []
    tol_exps = []
    for tol_exp in range(-20, 10):                # range(-20,10)
        tol = 10**tol_exp
        counter = 0
        total_counter = 0
        tol_str = f"{float(tol):.0e}"
        base_dir = f"json_files_all_results_{Multistep}/json_files_{tol_str}_{tol_str}"
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
        counters.append(counter)

plt.plot(tol_exps, counters, '-x')
plt.gca().set_title('Comparison of all State Trajectories to JWS for BDF')
plt.gca().set_xlabel("Error Tolerance for comparing State Trajectories")
plt.gca().set_ylabel("Matching models")
plt.gcf().tight_layout()
#plt.savefig("json_files_all_results_BDF/compareStateTrajectories_summary.pdf")
plt.show()