# test
import libsbml
import importlib
import amici
import os
import sys
import numpy as np
import logging
import shutil

# important stuff
sbml_file = '/home/paulstapor/sedml_import/model_steadystate_scaled.xml'
model_name = 'model_steadystate_scaled'
model_output_dir = '/home/paulstapor/sedml_import/' + model_name


# Create SBML importer
sbml_importer = amici.SbmlImporter(sbml_file)

# SBML2AMICI
sbml_importer.sbml2amici(model_name, model_output_dir, verbose=False)