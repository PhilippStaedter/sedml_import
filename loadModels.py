# load every one of the working 130 models into workspace
import sys
import os
import importlib
import amici


def LoadSpecificModel(model_name, explicit_model):

    # path to one specific model
    model_output_dir = "/home/paulstapor/sbml2amici/amici_models/" + model_name + "/" + explicit_model

    # load specific model
    sys.path.insert(0, os.path.abspath(model_output_dir))
    model_module = importlib.import_module(explicit_model)
    model = model_module.getModel()

    # some useful properties
    print("Model states: ", model.getStateIds())    # get states
    print("Model observables:   ", model.getObservableIds())    # get observables
    print("Model parameters:    ", model.getParameterIds())     # get parameters




