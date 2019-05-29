# script for changing sbml vectors through sedml vectors
from loadModels import *
import libsedml
import libsbml
import re
import numpy as np


def changeValues(model, model_name, explicit_model):

    # important paths
    sedml_path = './sedml_models/' + model_name + '/' + model_name + '.sedml'
    sbml_path = './sedml_models/' + model_name + '/sbml_models/' + explicit_model + '.sbml'

    # load model
    # model = load_specific_model(model_name, explicit_model)

    # load SBML && SEDML models
    sbml_file = libsbml.readSBML(sbml_path)
    sedml_file = libsedml.readSedML(sedml_path)

    # old species settings of SBML model that have to be replaced
    all_properties = sbml_file.getModel()
    spcs = all_properties.getListOfSpecies()
    spcs_id = []
    spcs_num = []
    for iCount in range(0, len(spcs)):
        spcs_id.append(spcs[iCount].id)
        spcs_num.append(spcs[iCount].initial_concentration)

    # old parameter settings of SBML model that have to be replaced
    par_id = model.getParameterIds()
    par_id = list(par_id)
    par_num = model.getParameters()
    par_num = list(par_num)

    # new settings of SEDML parameters
    for iSBMLModel in range(0, sedml_file.getNumModels()):
        all_models = sedml_file.getModel(iSBMLModel)
        for iAttribute in range (0, all_models.getNumChanges()):
            all_changes = all_models.getChange(iAttribute)
            new_targ = all_changes.getTarget()
            new_val = all_changes.getNewValue()

            # decide for species or parameter
            div = new_targ.split('[')
            div = div[0]
            div = div.split(':')
            div = div[4]

            if div == 'species':
                # parse right id out of new_trag string
                id = new_targ.split('\'', )
                id = id[1]

                # counter
                counter = 0

                # swap species settings
                while id != spcs_id[counter]:
                    counter = counter + 1
                spcs_num[counter] = new_val

            elif div == 'parameter':
                # parse right id out of new_trag string
                id = new_targ.split('\'',)
                id = id[1]

                # counter
                counter = 0

                # swap parameter settings
                while id != par_id[counter]:
                    counter = counter + 1
                par_num[counter] = new_val

    # transform par_num into an array
    par_num = np.asarray(par_num)                                                   # is never being reached
    p_num = []
    for iCount in range(0, len(par_num)):
        p_num.append(float(par_num[iCount]))

    # transform spcs_id into an array
    spcs_num = np.asarray(spcs_num)
    s_num = []
    for iCount in range(0, len(spcs_num)):
        s_num.append(float(spcs_num[iCount]))

    # replace old vector by new one
    model.setParameters(p_num)
    model.setInitialStates(s_num)

    return model