# script to simulate models using the petab format files

import pypesto
import petab
import amici
import matplotlib.pyplot as plt
import numpy as np


# important paths
model_base_path = '../benchmark-models/hackathon_contributions_new_data_format/Boehm_JProteomeRes2014'
other_one = './sedml_models/perelson1996_fig1b_top'

# manage petab problem
petab_problem = petab.Problem.from_folder(other_one)      #'./sedml_models/perelson1996_fig1b_top/experimental_data_rearranged')
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

a = 4