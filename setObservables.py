# get observables for amici import

from transferObservables import *
import libsbml
import sys
import os
import importlib
import amici
import amici.plotting
import matplotlib.pyplot as plt
import numpy as np
import libsedml
from getObservables import *



def plotObservables(iModel,iFile):


    # call function 'getObservables()'
    getAllObservables(iModel,iFile)

    # create folder for models with observables
    if not os.path.exists('../sbml2amici/amici_models_with_observables'):
        os.makedirs('../sbml2amici/amici_models_with_observables')

    # loop over all models
    #list_directory_sedml = os.listdir('./sedml_models')

    #for iModel in list_directory_sedml:

     #   list_directory_sbml = os.listdir('./sedml_models' + iModel + '/sbml_models')

      #  for iFile in list_directory_sbml:

    if os.path.exists('./BioModelsDatabase_models/' + iModel):                                                      # no comparison for observables available, so no simulation needed
        # important paths
        model_output_dir = '../sbml2amici/amici_models_with_observables/' + iModel + '/' + iFile
        model_path = './sedml_models/' + iModel + '/sbml_models_with_observables/' + iFile + '_with_observabels.xml'       ##### needs automatisation

        # sbml2amici import
        sbml_importer = amici.SbmlImporter(model_path)
        sbml_importer.sbml2amici(iModel, model_output_dir, verbose=False)

    else:
        # important paths
        model_output_dir = '../sbml2amici/amici_models_with_observables/' + iModel + '/' + iFile
        model_path = './sedml_models/' + iModel + '/sbml_models_with_observables/' + iFile + '_with_observabels.xml'
        sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'

        # get observables
        sbml_doc = libsbml.readSBML(model_path)
        model = sbml_doc.getModel()
        observables = get_observables(model, False)

        # sbml2amici import
        sbml_importer = amici.SbmlImporter('./sedml_models/adlung2017_fig2bto2e/sbml_models_with_observables/model0_adlung1_with_observabels.xml')
        sbml_importer.sbml2amici(iModel, model_output_dir, observables=observables, verbose=False)

        # load specific model
        sys.path.insert(0, os.path.abspath(model_output_dir))
        model_module = importlib.import_module(iModel)
        model = model_module.getModel()

        # set time points
        sedml_file = libsedml.readSedML(sedml_path)
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

        model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

        # print observables
        #print("Model observables:   ", model.getObservableIds())

        # get solver instance
        #solver = model.getSolver()

        # simulate model once
        #sim_data = amici.runAmiciSimulation(model,solver)

        # np.set_printoptions(threshold=8, edgeitems=2)
        #for key, value in sim_data.items():
         #   print('%12s: ' % key, value)

        # plot observable trajectories
        #amici.plotting.plotObservableTrajectories(sim_data)
        # amici.plotting.plotStateTrajectories(sim_data)

        # show plot
        #plt.show()

        return model