# python script for checking if an sbml has units

import libsbml
import numpy as np
import pandas as pd
import os

error = 0
path = './sedml_models'
print(str(os.path.isdir(path)))
all_models = sorted(os.listdir(path))
#all_models = all_models[50:]
list = []
list2 = []
list3 = []
for iSEDML in all_models:
    all_sbml = sorted(os.listdir(path + '/' + iSEDML + '/sbml_models'))
    for iSBML in all_sbml:
        sbml_model = libsbml.readSBML(path + '/' + iSEDML + '/sbml_models/' + iSBML)
        sbml = sbml_model.getModel()
        list3.append(1)
        try:
            units = sbml.getListOfUnitDefinitions()
        except:
            error = error + 1
            print(error)
            break
        if len(units) > 1:
            list.append(len(units))
            list2.append(1)
        #print('SBML Name: ' + iSBML)
        #print('Unit Length: ' + str(len(units)))

print('Total number of units for models with unite#  > 1: ' + str(sum(list)))
print('Total number of sbmls with units > 1: ' + str(sum(list2)))
print('Total number of sbml models: ' + str(len(list3)))
print('Total error: ' + str(error))


# only for models with units > 1
# store as .tsv

# further code
#getModel().getListOfSpecies().getUnitDefinition().getId()