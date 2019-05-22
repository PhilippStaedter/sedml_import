# execute script loadModels.py + simulate model

from loadModels import *
from changeValues import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt
import libsedml


# insert specific model properties as strings, e.g.:
# model_name = 'bachmann2011'
# explicit_model = 'bachmann'
base_path_sbml2amici = '../sbml2amici/amici_models'
base_path_sedml = './sedml_models'


# list of all directories + SBML files
list_directory_sedml = os.listdir(base_path_sedml)
list_directory_sedml = sorted(list_directory_sedml)

# list only specific models ---- should only simulate those models where sbml to amicic worked!
for iModel in list_directory_sedml:

    if os.path.exists(base_path_sbml2amici + '/' + iModel):
        list_files = os.listdir(base_path_sbml2amici + '/' + iModel)
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

                    # load script 'changeValues'
                    # model = changeValues(iModel, iFile)

                    # set timepoints for which we want to simulate the model
                    model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

                    # Create solver instance
                    solver = model.getSolver()

                    # Run simulation using default model parameters and solver options
                    sim_data = amici.runAmiciSimulation(model, solver)

                    # np.set_printoptions(threshold=8, edgeitems=2)
                    #for key, value in sim_data.items():
                    #    print('%12s: ' % key, value)

                    # plot sim_data
                    amici.plotting.plotStateTrajectories(sim_data)
                    # amici.plotting.plotObservableTrajectories(sim_data)

                    # save plot in therefore created folder
                    if not os.path.exists('../sbml2amici/Figures/' + iModel + '/' + iModel):
                        os.makedirs('../sbml2amici/Figures/' + iModel + '/' + iModel)
                    plt.savefig('../sbml2amici/Figures/' + iModel + '/' + iModel + '/' + iFile + '.png')

                    # show plot
                    # plt.show()
            except:
                print('Loading Model did not work!')

    else:
        print('Model import to amici did not work!')
