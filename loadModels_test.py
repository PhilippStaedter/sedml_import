# load test model into workspace

import sys
import os
import importlib
import amici

# IMPORTANT INFORMATION
#models = 'hockin2002_fig3-user'
model_name = 'model_steadystate_scaled'

# path to all models (now just)
model_output_dir = "/home/paulstapor/sedml_import/" + model_name

# load models
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(model_name)
model = model_module.getModel()

print("Model states: ", model.getStateIds())



