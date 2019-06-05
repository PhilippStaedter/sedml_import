# Add Parameter / State / Reaction values
import os
import libsbml
import pandas as pd
from loadModels import *
import libsedml

# important paths
models_path = '../sbml2amici/amici_models'
models_base_path = '../sbml2amici'
base_path = './sedml_models'
tsv_file_path = '../sbml2amici/table.tsv'

# list of all directories + SBML files
list_directory = os.listdir(base_path)
list_directory = sorted(list_directory)

# read in table + new column in correct order
tsv_file = pd.read_csv(tsv_file_path, sep='\t')
tsv_file['parameters'] = pd.Series()
tsv_file['t_start'] = pd.Series()
tsv_file['t_end'] = pd.Series()
tsv_file['t_steps'] = pd.Series()
columnTitels = ['id', 'states', 'reactions', 'parameters', 't_start', 't_end', 't_steps', 'error_message']
tsv_file = tsv_file.reindex(columns=columnTitels)

# add parameter
for models in list_directory:
    list_files = os.listdir(base_path + '/' + models + '/sbml_models')
    list_files = sorted(list_files)

    for files in list_files:
        sbml_file = base_path + '/' + models + '/sbml_models/' + files
        model_name, other_stuff = files.split(".", 1)
        model_output_dir = models_path + '/' + models + '/' + model_name

        try:
            # define id
            id = '{' + models + '}' + '_' + '{' + files + '}'

            # read accompanying sbml file
            file = libsbml.readSBML(sbml_file)
            all_properties = file.getModel()
            num_parameters = len(all_properties.getListOfParameters())
            # num_states = len(all_properties.getListOfSpecies())
            # num_reactions = len(all_properties.getListOfReactions())

            # set counter
            counter = 0

            # assign value to matching row
            while id != tsv_file['id'][counter]:
                counter = counter + 1
            else:
                tsv_file.loc[counter, 'parameters'] = num_parameters
                # tsv_file.loc[counter, 'states'] = num_states
                # tsv_file.loc[counter, 'reactions'] = num_reactions

        except:
            # error message
            print('Parameter value could not be saved!')
            # print('State value could not be saved!')
            # print('Reaction value could not be saved!')

# add time points
for iModel in list_directory:

    if os.path.exists(models_path + '/' + iModel):
        list_files = os.listdir(models_path+ '/' + iModel)
        list_files = sorted(list_files)                                                                                          # sorted() could maybe change the order needed for later

        for iFile in list_files:

            try:
                # run function
                model = load_specific_model(iModel, iFile)

                # open sedml to get tasks + time courses
                sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'

                # tasks
                sedml_file = libsedml.readSedML(sedml_path)
                for iSBMLModel in range(0, sedml_file.getNumTasks()):
                    all_tasks = sedml_file.getTask(iSBMLModel)
                    tsk_Id = all_tasks.getId()
                    task_name = all_tasks.getName()
                    task_modRef = all_tasks.getModelReference()
                    task_simReference = all_tasks.getSimulationReference()
                    # time courses
                    all_simulations = sedml_file.getSimulation(iSBMLModel)
                    sim_Id = all_simulations.getId()

                    while task_simReference != sim_Id:
                        iSBMLModel = iSBMLModel + 1                                                         # only works if the list of models are somehow chronological and not random [iff task1 appears before task2]
                        all_simulations = sedml_file.getSimulation(iSBMLModel)
                        sim_Id = all_simulations.getId()

                    sim_start_time = all_simulations.getOutputStartTime()
                    sim_end_time = all_simulations.getOutputEndTime()
                    sim_num_time_points = all_simulations.getNumberOfPoints()

                    # define id
                    id = '{' + iModel + '}' + '_' + '{' + task_modRef + '.sbml}'

                    # set counter
                    counter = 0

                    # assign value to matching row
                    while id != tsv_file['id'][counter]:
                        counter = counter + 1
                    else:
                        tsv_file.loc[counter, 't_start'] = sim_start_time
                        tsv_file.loc[counter, 't_end'] = sim_end_time
                        tsv_file.loc[counter, 't_steps'] = sim_num_time_points

            except:
                # error message
                print('Time vector could not be saved!')

# save tsv_file
tsv_file.to_csv(path_or_buf=models_base_path + '/table_with_parameter_and_time.tsv', sep='\t', index=False)
