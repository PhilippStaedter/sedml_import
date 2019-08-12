# script to simulate models using the petab format files

import pypesto
import petab
import amici
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pypesto.visualize


iModel = 'kouril2017_fig2b'
n_starts = 5


# important paths
model_base_path = './sedml_models/' + iModel

# manage petab problem
petab_problem = petab.Problem.from_folder(model_base_path)      #'./sedml_models/perelson1996_fig1b_top/experimental_data_rearranged')
petab_problem.get_optimization_to_simulation_parameter_mapping()

# import model to amici
importer = pypesto.PetabImporter(petab_problem)
model = importer.create_model()
print(model.getParameterScale())
print("Model parameters:", list(model.getParameterIds()), '\n')
print("Model const parameters:", list(model.getFixedParameterIds()), '\n')
print("Model outputs:   ", list(model.getObservableIds()), '\n')
print("Model states:    ", list(model.getStateIds()), '\n')

# create objective function
obj = importer.create_objective()
print("Nominal parameter values:\n", petab_problem.x_nominal)
print(obj(petab_problem.x_nominal))

# run optimization
optimizer = pypesto.ScipyOptimizer()
problem = importer.create_problem(obj)
engine = pypesto.SingleCoreEngine()
# engine = pypesto.MultiProcessEngine()
result = pypesto.minimize(problem=problem, optimizer=optimizer, n_starts=n_starts, engine=engine)

# visualize
ref = pypesto.visualize.create_references(x=petab_problem.x_nominal, fval=obj(petab_problem.x_nominal))
pypesto.visualize.waterfall(result, reference=ref, scale_y='lin')
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.savefig(model_base_path + '/waterfall_estimation_' + str(n_starts) + '_merrors.pdf')
pypesto.visualize.parameters(result, reference=ref)
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.savefig(model_base_path + '/waterfall_parameter_' + str(n_starts) + '_merrors.pdf')
print(result.optimize_result.get_for_key('fval'))

# simulated data
rdatas = obj(result.optimize_result.get_for_key('x')[0], return_dict=True)['rdatas']
df = importer.rdatas_to_measurement_df(rdatas)
plt.xlabel("Experiment")
plt.ylabel("Simulation")
plt.scatter(petab_problem.measurement_df['measurement'], df['measurement'])
#plt.show()

# save all plots and data frame in same folder
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.savefig(model_base_path + '/measurement_' + str(n_starts) + '_merrors.pdf')
df.to_csv(model_base_path + '/simulatedData_' + iModel + '_' + str(n_starts) + '_merrors.tsv', sep='\t', index=False)