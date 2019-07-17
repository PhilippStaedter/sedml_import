# copy all observables from sedml to sbml + save new sbml with observables

import libsedml
import libsbml
import sys
import os
import importlib



def getAllObservables(iSEDML, core_iSbml):


# list of all directories + SBML files
#list_directory_sedml = sorted(os.listdir(base_path_sedml))

# create new sbml file with observables
#for iSEDML in list_directory_sedml:

    # iSEDML = 'kouril2017_fig1a'

 #   list_files = sorted(os.listdir(base_path_sedml + '/' + iSEDML + '/sbml_models'))

  #  for iSBML in list_files:


    # split iSBML
    #core_iSbml, XML = iSBML.split('.')

#iSEDML = 'bachmann2011'
#core_iSbml = 'bachmann'

    # important paths
    base_path_sedml = './sedml_models'
    sedml_path = './sedml_models/' + iSEDML + '/' + iSEDML + '.sedml'
    sbml_path = './sedml_models/' + iSEDML + '/sbml_models/' + core_iSbml + '.sbml'
    new_sbml_path = base_path_sedml + '/' + iSEDML + '/sbml_models_with_observables/' + core_iSbml + '_with_observabels.xml'
    if not os.path.exists(sedml_path):
        print('No Observables!')
    else:
        # new folder for all sbml models with observables
        if not os.path.exists(base_path_sedml + '/' + iSEDML + '/sbml_models_with_observables'):
            os.makedirs(base_path_sedml + '/' + iSEDML + '/sbml_models_with_observables')
        # read in sedml file
        sedml_file = libsedml.readSedML(sedml_path)
        # get number of tasks and observables
        num_task = sedml_file.getNumTasks()
        num_obs = sedml_file.getNumDataGenerators()
        # read in sbml model
        reader = libsbml.SBMLReader()
        sbml_file = reader.readSBML(sbml_path)
        model = sbml_file.getModel()
        for iTask in range(0, num_task):
            task_id = sedml_file.getTask(iTask).getId()

            # create list with all parameter-ids to check for uniqueness
            # all_par_id = []
            almost_all_par_id = []

            for iObservable in range(0, num_obs):
                # get important formula
                obs_Formula = libsedml.formulaToString(sedml_file.getDataGenerator(iObservable).getMath())
                obs_Id = sedml_file.getDataGenerator(iObservable).getId()
                # SBML_model_Id,Observable_Id = obs_Id.split('_',1)
                new_obs_Id = 'observable_' + obs_Id
                # get list of parameters
                list_par_id = []
                list_par_value = []
                num_par = sedml_file.getDataGenerator(iObservable).getNumParameters()
                if num_par == 0:
                    print(obs_Id + ' has no parameters as observables!')

                else:
                    for iCount in range(0, num_par):
                        list_par_id.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getId())
                        # list_par_value.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getValue())
                        # all_par_id.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getId())
                        list_par_value.append(
                            sedml_file.getDataGenerator(iObservable).getParameter(iCount).getValue())
                        almost_all_par_id.append(
                            sedml_file.getDataGenerator(iObservable).getParameter(iCount).getId())

                        # check for uniqueness of parameter-ids
                        # for iNum in range(0, len(all_par_id)):
                        #   almost_all_par_id = all_par_id.remove(all_par_id[len(all_par_id) - 1])
                        for iNum in range(0, len(almost_all_par_id)):
                            all_par_id = almost_all_par_id[iNum]
                            almost_all_par_id.remove(almost_all_par_id[len(almost_all_par_id) - 1])
                            last_element = list(all_par_id[len(all_par_id) - 1])
                            intersection = [i for i in last_element if i in almost_all_par_id]
                            if len(intersection) != 0:
                                print('Two or more parameters have the same Id!')
                                # sys.exit(1)
                # look for correct observables: with target and with task_id == task_ref
                if sedml_file.getDataGenerator(iObservable).getVariable(0).getTarget() != '':
                    # get task reference
                    task_target = sedml_file.getDataGenerator(iObservable).getVariable(0).getTarget()
                    task_ref = sedml_file.getDataGenerator(iObservable).getVariable(0).getTaskReference()
                    if task_id == task_ref:
                        # create formula
                        assignmentRule = model.createAssignmentRule()
                        assignmentRule.setId(new_obs_Id)
                        assignmentRule.setVariable(new_obs_Id)
                        assignmentRule.setFormula(obs_Formula)
                        # create parameter to formula for observables
                        obs_parameter = model.createParameter()
                        obs_parameter.setId(new_obs_Id)
                        obs_parameter.setConstant(False)
                        # create parameter to formula for parameters
                        for iCount in range(0, num_par):
                            iPar_id = list_par_id[iCount]
                            iPar_value = list_par_value[iCount]
                            parameter = model.createParameter()
                            parameter.setId(iPar_id)
                            parameter.setConstant(False)
                            parameter.setValue(iPar_value)
        libsbml.writeSBMLToFile(sbml_file, new_sbml_path)