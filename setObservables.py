# get observables for amici import

from transferObservables import *
import libsbml
import sys
import os
import importlib
import amici


models = 'bachmann2011'


model_output_dir = '../sbml2amici/' + models
model_path = './sedml_models/bachmann2011/sbml_models_with_observables/bachmann_with_observabels.xml'
sbml_doc = libsbml.readSBML(model_path)
model = sbml_doc.getModel()
observables = get_observables(model, False)                                                          ### error

sbml_importer = amici.SbmlImporter(model_path)
sbml_importer.sbml2amici(models, model_output_dir, observables=observables, verbose=False)

# load specific model
sys.path.insert(0, os.path.abspath(model_output_dir))
model_module = importlib.import_module(models)
model = model_module.getModel()

print("Model observables:   ", model.getObservableIds())    # get observables

