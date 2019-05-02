# SBML2AMICI
import libsbml
import importlib
import amici
import os
import sys
import numpy as np
import logging
import shutil


# important paths
models_path = "../sbml2amici/amici_models"
base_path = "/sedml_models"


# create directory for all future amici models
if not os.path.exists(models_path):
    os.makedirs(models_path)

# Create logger object
logger = logging.getLogger()

# initialize the log settings
logging.basicConfig(filename='all_logs',level=logging.DEBUG)

# list of all directories + SBML files
list_directory = os.listdir(base_path)

for models in list_directory:
    list_files = os.listdir(base_path + '/' + models + '/sbml_models')
    for files in list_files:
        sbml_file = base_path + '/' + models + '/sbml_models/' + files
        model_name, other_stuff = files.split(".",1)
        model_output_dir = models_path + '/' + models + '/' + model_name

        try:
            # Create SBML importer
            sbml_importer = amici.SbmlImporter(sbml_file)

            # SBML2AMICI
            sbml_importer.sbml2amici(model_name,
                        model_output_dir,
                        verbose=False)

        except:
            print(sys.exc_info()[0])
            logging.exception('Model failed: %s, %s', models, files)
            logging.info('\n')
            #logging.exception(str(Exception))
        #except Exception as e:
         #   logging.exeption(str(e), exc_info=True)
            #continue

# copy file 'all_logs' in new directory 'sbml2amici'
old_path = '/all_logs'
new_path = models_path + '/all_logs'
shutil.move(old_path, new_path)