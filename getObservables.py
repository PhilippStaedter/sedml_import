# copy all observables from sedml to sbml

import libsedml
import libsbml
import sys
import os
import importlib


iSEDML = 'bachmann2011'
iSBML = 'bachmann'

# def getObservables(iSEDML, iSBML):

# important paths
sedml_path = './sedml_models/' + iSEDML + '/' + iSEDML + '.sedml'
sbml_path = './sedml_models/' + iSEDML + '/sbml_models/' + iSBML + '.sbml'
new_sbml_path = './sedml_models/' + iSEDML + '/sbml_models/' + iSBML + '_with_observabels.sbml'

# read in sedml file
sedml_file = libsedml.readSedML(sedml_path)

# get number of tasks and observables
num_task = sedml_file.getNumTasks()
num_obs = sedml_file.getNumDataGenerators()

for iTask in range(0, num_task):
    task_id = sedml_file.getTask(iTask).getId()

    for iObservable in range(0, num_obs):
        # get important formula
        obs_Formula = libsedml.formulaToString(sedml_file.getDataGenerator(iObservable).getMath())             # has to be autmomatist
        obs_Id = sedml_file.getDataGenerator(iObservable).getId()                                              # iCount instead of 0
        SBML_model_Id,Observable_Id = obs_Id.split('_',1)
        new_obs_Id = 'observable_' + Observable_Id

        # get list of parameters
        list_par = []
        num_par = sedml_file.getDataGenerator(iObservable).getNumParameters()
        if num_par == 0:
            print(obs_Id + ' has no parameters as observables!')
        else:
            for iCount in range(0, num_par):
                list_par.append(sedml_file.getDataGenerator(iObservable).getParameter(1).getId())

        # get task reference
        task_ref = sedml_file.getDataGenerator(iObservable).getVariable(0).getTaskReference()

        # read in sbml model
        sbml_file = libsbml.readSBML(sbml_path)

        if task_id == task_ref:
            # create formula
            assignmentRule = sbml_file.createModel()
            assignmentRule.createAssignmentRule()
            assignmentRule.setId(new_obs_Id)
            assignmentRule.setVariable(new_obs_Id)
            assignmentRule.setFormula(obs_Formula)

            # create parameter to formula for observables
            obs_parameter = sbml_file.createParameter()
            obs_parameter.setId(new_obs_Id)
            obs_parameter.setConstant(False)

            # create parameter to formula for parameters
            for iCount in range(0, num_par):
                iPar = list_par[iCount]
                parameter = libsbml.createParameter()
                parameter.setId(iPar)
                parameter.setConstant(False)                        # not available
                parameter.setValue(iPar)                            # not available

    libsbml.writeSBMLToFile(sbml_path,new_sbml_path)