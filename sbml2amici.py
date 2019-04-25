# SBML2AMICI
import libsbml
import importlib
import amici
import os
import sys
import numpy as np
import logging
import shutil


# create directory for all future amici models
if not os.path.exists("/home/paulstapor/sbml2amici/amici_models"):
    os.makedirs("/home/paulstapor/sbml2amici/amici_models")

# Create logger object
logger = logging.getLogger()

# initialize the log settings
logging.basicConfig(filename='all_logs',level=logging.DEBUG)

# list of all directories + SBML files
list_directory = os.listdir("/home/paulstapor/sedml_import/sedml_models")

for models in list_directory:
    list_files = os.listdir("/home/paulstapor/sedml_import/sedml_models/" + models + "/sbml_models")
    for files in list_files:
        sbml_file = '/home/paulstapor/sedml_import/sedml_models/' + models + '/sbml_models/' + files                  # bachmann.sbml / adlung2017_fig2bto2e / model0_adlung1
        model_name, other_stuff = files.split(".",1)
        model_output_dir = "/home/paulstapor/sbml2amici/amici_models/" + models + "/" + model_name                                   # model_name

        try:
            # Create SBML importer
            sbml_importer = amici.SbmlImporter(sbml_file)

            # SBML2AMICI
            sbml_importer.sbml2amici(model_name,                                                                          # crashes!
                        model_output_dir,
                        verbose=False)

        except:
            print(sys.exc_info()[0])
            logging.exception('Model failed: %s, %s', models, files)
            logging.info('\n')
            #logging.exception(str(Exception))
        #except Exception as e:
         #   logging.exeption(str(e), exc_info=True)                                                                                   # no text saved?
            #continue

# copy file 'all_logs' in new directory 'sbml2amici'
old_path = '/home/paulstapor/sedml_import/all_logs'
new_path = '/home/paulstapor/sbml2amici/all_logs'
shutil.move(old_path, new_path)