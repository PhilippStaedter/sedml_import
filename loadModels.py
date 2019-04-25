# load all 130 Models into workspace

import sys
import os
import importlib
import amici


# path to all models (now just)
model_output_dir = '/home/paulstapor/sbml2amici/amici_models/hockin2002_fig3-user/model4_hockin1' # + models + "/" + model_name
model_name = 'model4_hockin1'

# load models
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(model_name)
model = model_module.getModel()

print("Model states: ", model.getStateIds())



