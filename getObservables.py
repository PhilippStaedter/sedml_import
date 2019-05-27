# copy all observables from sedml to sbml

import libsedml
import libsbml

def getObservables(iSEDML, iSBML):

    # important paths
    sedml_path = './sedml_models/' + iSEDML + '/' + iSBML + '.sedml'
    sbml_path = './sedml_models/' + iSEDML + '/sbml_models/' + iSBML + '.sbml'

    # read in sedml file
    sedml_file = libsedml.readSedML(sedml_path)

    # get important values
    obsFormula = libsedml.formulaToString(sedml_file.getDataGenerator(0).getMath())             # has to be autmomatist
    obsId = sedml_file.getDataGenerator(0).getId()                                              # iCount instead of 0
    SBML_model_Id = obsId.split('_',1)
    obsId = 'observable_' + obsId

    # get list of parameters
    list_par = sedml_file.getParameters()

    # read in sbml model
    sbml_file = libsbml.readSBML(sbml_path)

    assignemtRule = sbml_file.createAssignmentRule()
    assignemtRule.setId(obsId)
    assignemtRule.setVariable(obsId)
    assignemtRule.setFormula(obsFormula)

    parameter = sbml_file.createParameter()
    parameter.setId(obsId)
    parameter.setConstant(False)

    for iPar in range(0, len(list_par)):
        parameter = libsbml.createParameter()
        parameter.setId(iPar)
        parameter.setConstant(False)
        parameter.setValue(iPar)

    writeSBMLToFile(sbml_model_no_observables,sbml_model_with_observables)