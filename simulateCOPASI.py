# script for all processes conserning the COPASI LSODA simulation of all models with correct state trajectories

import os
import sys
import numpy as np
import pandas as pd
import libsedml
import libsbml
from setTime_BioModels import *
from time import time


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
        model_name = xml_model.getModel().getName()
    else:
        sedml_file = libsedml.readSedML(sedml_path)
        sbml_file = libsbml.readSBML(sbml_path)
        model_name = sbml_file.getModel().getName()

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

            # replace 'sim_num_time_points' by default value 101 for trajectory comparison in the end
            sim_num_time_points = 101

    return model_name, sim_start_time, sim_end_time, sim_num_time_points


def getSimTable(iModel, iFile):
    # important paths
    sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
    biomodels_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.xml'

    # check for type of model and open sbml/xml file
    if os.path.exists(sbml_path):
        sbml_file = libsbml.readSBML(sbml_path)
    elif os.path.exists(biomodels_path):
        sbml_file = libsbml.readSBML(biomodels_path)
    else:
        print('Something with the paths went wrong!')
        sys.exit()

    # get compartments
    num_comp = sbml_file.getModel().getNumCompartments()
    comp_and_type = []
    for iComp in range(0, num_comp):
        if not sbml_file.getModel().getCompartment(iComp).getName() == '':
            comp_and_type.append([sbml_file.getModel().getCompartment(iComp).getId(), sbml_file.getModel().getCompartment(iComp).getName()])
        else:
            comp_and_type.append([sbml_file.getModel().getCompartment(iComp).getId(), sbml_file.getModel().getCompartment(iComp).getId()])

    # get species that use one of the compartments above
    num_spec = sbml_file.getModel().getNumSpecies()
    spec_and_type = []
    for iSpec in range(0, num_spec):
        spec_comp = sbml_file.getModel().getSpecies(iSpec).getCompartment()
        for iComp in range(0, len(comp_and_type)):
            if spec_comp == comp_and_type[iComp][0]:
                if not sbml_file.getModel().getSpecies(iSpec).getName() == '':
                    spec_and_type.append([comp_and_type[iComp][1], sbml_file.getModel().getSpecies(iSpec).getName(), 'Concentration'])
                else:
                    spec_and_type.append([comp_and_type[iComp][1], sbml_file.getModel().getSpecies(iSpec).getId(), 'Concentration'])

    # get parameters that are not constant
    num_par = sbml_file.getModel().getNumParameters()
    par_and_type = []
    for iPar in range(0, num_par):
        par_constant = sbml_file.getModel().getParameter(iPar).getConstant()
        if par_constant == False:
            if not sbml_file.getModel().getParameter(iPar).getName() == '':
                par_and_type.append([sbml_file.getModel().getParameter(iPar).getName(), 'Value'])
            else:
                par_and_type.append([sbml_file.getModel().getParameter(iPar).getId(), 'Value'])

    return spec_and_type, par_and_type


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

    # look for all necessary lines to alter the file - for every tolerance combination
    atol = [str(Tol).split('-')[1] for Tol in abs_tol]
    rtol = [str(Tol).split('-')[1] for Tol in rel_tol]
    for iTol in range(0, len(atol)):
        AbsTol = atol[iTol]
        RelTol = rtol[iTol]

        # open .cps as text file and save it as new .cps file
        cps_file = open(path_cps, 'r')
        changed_cps_file = open(new_path_cps + '/Changed_' + iModel + '_' + AbsTol + '_' + RelTol + '.cps', 'w')

        # get data for the simulation table
        spec_and_type, par_and_type = getSimTable(iModel, iFile)

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
                changed_cps_file.write(line)
                changed_cps_file.write(f'      <Table printTitle="1"> \n')
                changed_cps_file.write(f'        <Object cn="CN=Root,Model={model_name},Reference=Time"/> \n')
                for iLine in range(0, len(spec_and_type)):
                    changed_cps_file.write(f'        <Object cn="CN=Root,Model={model_name},Vector=Compartments[{spec_and_type[iLine][0]}],Vector=Metabolites[{spec_and_type[iLine][1]}],Reference={spec_and_type[iLine][2]}"/> \n')
                for iLine in range(0, len(par_and_type)):
                    changed_cps_file.write(f'        <Object cn="CN=Root,Model={model_name},Vector=Values[{par_and_type[iLine][0]}],Reference={par_and_type[iLine][1]}"/> \n')
                changed_cps_file.write(f'        <Object cn="CN=Root,Timer=CPU Time"/> \n')
                changed_cps_file.write(f'        <Object cn="CN=Root,Timer=Wall Clock Time"/> \n')
                changed_cps_file.write(f'      </Table> \n')
            else:
                changed_cps_file.write(line)
        changed_cps_file.close()
        cps_file.close()


def simLSODA(iModel, iFile):
    # create a data frame to save the results
    columns = ['setting', 'id', 't_intern_ms', 't_extern_ms']
    df = pd.DataFrame(columns=columns, data=[])

    # all settings
    abs_tol = [1e-08, 1e-6, 1e-12, 1e-10, 1e-14, 1e-16, 1e-8]
    rel_tol = [1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-8, 1e-16]

    # look for all necessary lines to alter the file - for every tolerance combination
    atol = [str(Tol).split('-')[1] for Tol in abs_tol]
    rtol = [str(Tol).split('-')[1] for Tol in rel_tol]
    for iTol in range(0, len(atol)):
        AbsTol = atol[iTol]
        RelTol = rtol[iTol]

        # add a row to the data frame
        df = df.append({}, ignore_index=True)

        # important paths
        path_copasiSE = '../Documents/Software/COPASI/bin/CopasiSE'
        path_cps = f'../copasi_sim/{iModel}/{iFile}/Changed_{iModel}_{AbsTol}_{RelTol}.cps'

        # simulation using COPASI's LSODA
        number_of_repetitions = 40
        intern_simulation_time = []
        extern_simulation_time = []
        for iRep in range(0, number_of_repetitions):
            start = time()
            os.system(f'{path_copasiSE} --report-file copasi_results_{iRep}.tsv {path_cps}')
            t = time() - start
            extern_simulation_time.append(t)

            # open .tsv file to get intern CPU simulation time + delete file to save space
            path_results_file = f'../copasi_sim/{iModel}/{iFile}/copasi_results_{iRep}.tsv'
            cps_sim_file = pd.read_csv(path_results_file, sep='\t')
            intern_simulation_time.append(cps_sim_file['(Timer)CPU Time'][100])
            os.remove(path_results_file)

        # write medians in the data frame
        df['setting'][iTol] = f'{AbsTol}_{RelTol}'
        df['id'][iTol] = '{' + iModel + '}_{' + iFile + '}'
        df['t_intern_ms'][iTol] = np.median(intern_simulation_time)
        df['t_extern_ms'][iTol] = np.median(extern_simulation_time)




############# call functions

# paths
correct_amici_models = '../sbml2amici/correct_amici_models_paper'
correct_amici_models_16 = '../sbml2amici/correct_amici_models_paper_16'

# 4

#'''
# 3
iModel = 'aguda1999_fig5c'
iFile = 'model0_aguda1'
#iModel = 'Leloup1999'
#iFile = 'Leloup1999'
simLSODA(iModel, iFile)
a = 4
#'''

# 2
iModel = 'aguda1999_fig5c'
iFile = 'model0_aguda1'
#iModel = 'Leloup1999'
#iFile = 'Leloup1999'
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
        iModel = 'Leloup1999'
        iFile = 'Leloup1999'
        #iModel = 'aguda1999_fig5c'
        #iFile = 'model0_aguda1'
        createCpsFiles(iModel, iFile)
        counter += 1
    print('Model: ' + iModel + ' done!')
print('Final Number : ' + str(counter))
