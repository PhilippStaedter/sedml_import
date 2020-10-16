# script for all processes conserning the COPASI LSODA simulation of all models with correct state trajectories

import os
import sys
import libsedml
import libsbml
from setTime_BioModels import *


def getTimeCourse(iModel, iFile):
    # important paths
    BioModels_path = './BioModelsDatabase_models'
    xml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.xml'
    sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'
    sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'

    # get time curse depending on type of model
    if os.path.exists(BioModels_path + '/' + iModel):
        sim_start_time, sim_end_time, sim_num_time_points, y_bound = timePointsBioModels(iModel)
        xml_model = libsbml.readSBML(xml_path)
        model_name = xml_model.getModel().getId()
    else:
        sedml_file = libsedml.readSedML(sedml_path)
        sbml_file = libsbml.readSBML(sbml_path)
        model_name = sbml_file.getModel().getId()

        for iTask in range(0, sedml_file.getNumTasks()):
            all_tasks = sedml_file.getTask(iTask)
            tsk_Id = all_tasks.getId()
            task_name = all_tasks.getName()
            task_modRef = all_tasks.getModelReference()
            task_simReference = all_tasks.getSimulationReference()

            # time courses
            try:
                all_simulations = sedml_file.getSimulation(iTask)
                sim_Id = all_simulations.getId()
            except:  # need 'except' clause if more models have same time period
                if all_simulations == None:
                    all_simulations = sedml_file.getSimulation(0)
                    sim_Id = all_simulations.getId()
            try:
                while task_simReference != sim_Id:
                    iTask = iTask + 1
                    all_simulations = sedml_file.getSimulation(iTask)
                    sim_Id = all_simulations.getId()
            except:
                iTask = 0
                while task_simReference != sim_Id:
                    all_simulations = sedml_file.getSimulation(iTask)
                    sim_Id = all_simulations.getId()
                    iTask = iTask + 1

            sim_start_time = all_simulations.getOutputStartTime()
            sim_end_time = all_simulations.getOutputEndTime()
            sim_num_time_points = all_simulations.getNumberOfPoints()

    return model_name, sim_start_time, sim_end_time, sim_num_time_points


def createCpsFiles(iModel, iFile):
    # important paths
    path_copasiSE = '../Documents/Software/COPASI/bin/CopasiSE'
    sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
    biomodels_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.xml'
    save_path = '../copasi_sim/' + iModel + '/' + iFile + '/' + iModel + '.cps'

    # check for type of model
    if os.path.exists(sbml_path):
        os.system(f'{path_copasiSE} -i {sbml_path} -s {save_path}')
    elif os.path.exists(biomodels_path):
        os.system(f'{path_copasiSE} -i {biomodels_path} -s {save_path}')
    else:
        print('Something with the paths went wrong!')
        sys.exit()


def changeCpsFile(iModel, iFile):
    # important paths
    path_cps = '../copasi_sim/' + iModel + '/' + iFile + '/' + iModel + '.cps'
    new_path_cps = '../copasi_sim/' + iModel + '/' + iFile

    # load time course of the specific model and additional values
    model_name, sim_start_time, sim_end_time, sim_num_time_points = getTimeCourse(iModel, iFile)
    step_size = 10000
    abs_tol = [1e-08, 1e-6, 1e-12, 1e-10, 1e-14, 1e-16, 1e-8]
    rel_tol = [1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-8, 1e-16]

    # open .cps as text file
    cps_file = open(path_cps, 'r')
    model_name = iModel + '_' + iFile

    # look for all necessary lines to alter the file - for every tolerance combination
    atol = [str(Tol).split('-')[1] for Tol in abs_tol]
    rtol = [str(Tol).split('-')[1] for Tol in rel_tol]
    for iTol in range(0, len(atol)):
        AbsTol = atol[iTol]
        RelTol = rtol[iTol]

        changed_cps_file = open(new_path_cps + '/Changed_' + iModel + '_' + AbsTol + '_' + RelTol + '.cps', 'w')
        for line in cps_file:
            if 'type="timeCourse" scheduled="false" updateModel="false"' in line:
                line = line.replace('scheduled="false"', 'scheduled="true"')
                changed_cps_file.write(line)
            elif '<Parameter name="StepNumber" type="unsignedInteger" value="100"/>' in line:
                line = line.replace('value="100"', f'value="{sim_num_time_points}"')
                changed_cps_file.write(line)
            elif '<Parameter name="StepSize" type="float" value="0.01"/>' in line:
                line = line.replace('value="0.01"', f'value="{sim_end_time / sim_num_time_points}"')
                changed_cps_file.write(line)
            elif '<Parameter name="Duration" type="float" value="1"/>' in line:
                line = line.replace('value="1"', f'value="{sim_end_time}"')
                changed_cps_file.write(line)
            elif '<Parameter name="OutputStartTime" type="float" value="0"/>' in line:
                line = line.replace('value="0"', f'value="{sim_start_time}"')
                changed_cps_file.write(line)
            elif '<Parameter name="Relative Tolerance" type="unsignedFloat" value="9.9999999999999995e-07"/>' in line:
                line = line.replace('value="9.9999999999999995e-07"', f'value="{rel_tol[iTol]}"')
                changed_cps_file.write(line)
            elif '<Parameter name="Absolute Tolerance" type="unsignedFloat" value="9.9999999999999998e-13"/>' in line:
                line = line.replace('value="9.9999999999999998e-13"', f'value="{abs_tol[iTol]}"')
                changed_cps_file.write(line)
            elif '<Parameter name="Max Internal Steps" type="unsignedInteger" value="100000"/>' in line:
                line = line.replace('value="100000"', f'value="{step_size}"')
                changed_cps_file.write(line)
            elif 'taskType="timeCourse" separator="&#x09;" precision="6"' in line:
                line = line.replace(line, f'{line} \n'
                                          f'<Table printTitle="1"> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Reference=Time"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[PER Protein (unphosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[TIM Protein (unphosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[PER Protein (mono-phosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[TIM Protein (mono-phosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[PER Protein (bi-phosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[TIM Protein (bi-phosphorylated)],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[Cytosolic PER-TIM Complex],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[nucleus],Vector=Metabolites[Nuclear PER-TIM Complex],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[PER mRNA],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Compartments[cytoplasm],Vector=Metabolites[TIM mRNA],Reference=Concentration"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Values[Total Per],Reference=Value"/> \n'
                                          f'<Object cn="CN=Root,Model={model_name},Vector=Values[Total Tim],Reference=Value"/> \n'
                                          f'<Object cn="CN=Root,Timer=CPU Time"/> \n'
                                          f'<Object cn="CN=Root,Timer=Wall Clock Time"/> \n'
                                          f'</Table>')
                changed_cps_file.write(line)
            else:
                changed_cps_file.write(line)
        changed_cps_file.close()
    cps_file.close()


############# call functions

# paths
correct_amici_models = '../sbml2amici/correct_amici_models_paper'
correct_amici_models_16 = '../sbml2amici/correct_amici_models_paper_16'

# 2
iModel = 'aguda1999_fig5c'
iFile = 'model0_aguda1'
changeCpsFile(iModel, iFile)
a = 4


# 1
counter = 0
correct_models = sorted(os.listdir(correct_amici_models))
correct_models_16 = sorted(os.listdir(correct_amici_models_16))
correct_trajectories = correct_models + correct_models_16
for iModel in correct_trajectories:
    if iModel in correct_models:
        sbmls = sorted(os.listdir(correct_amici_models + '/' + iModel))
    elif iModel in correct_models_16:
        sbmls = sorted(os.listdir(correct_amici_models_16 + '/' + iModel))
    for iFile in sbmls:
        #iModel = 'aguda1999_fig5c'
        #iFile = 'model0_aguda1'
        createCpsFiles(iModel, iFile)
        counter += 1
    print('Model: ' + iModel + ' done!')
print('Final Number : ' + str(counter))
