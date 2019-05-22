# execute script loadModels.py + simulate model

from loadModels import *
from changeValues import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt
import libsedml


def all_settings(iModel, iFile):

    # insert specific model properties as strings, e.g.:
    # model_name = 'bachmann2011'
    # explicit_model = 'bachmann'
    base_path_sbml2amici = '../sbml2amici/amici_models'
    base_path_sedml = './sedml_models'

    # run function
    model = load_specific_model(iModel, iFile)                                  # call function from 'loadModels.py'

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


    return model