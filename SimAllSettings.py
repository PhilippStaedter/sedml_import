# run all models with defiined settings

from execute_loadModels import *
import amici.plotting
import numpy as np
import matplotlib.pyplot as plt
import libsedml
import time
import statistics
import pandas as pd


def simulate(atol, rtol, linSol, solAlg):

    # Create new folder structure for study                                                                             # tolerance study
    tolerance_path = '../bachelor_thesis/Tolerance'
    if not os.path.exists(tolerance_path):
        os.makedirs(tolerance_path)

    # save name
    s_atol = str(atol).split('-')[1]
    s_rtol = str(rtol).split('-')[1]
    s_linSol = str(linSol)
    s_solAlg = str(solAlg)

    # create .tsv file
    tsv_table = pd.DataFrame(columns=['id', 't_intern_ms', 't_extern_ms', 'state_variables', 'error_message'])

    # set row counter for .tsv file
    counter = 0

    # insert specific model properties as strings, e.g.:
    base_path_sbml2amici = '../sbml2amici/amici_models'
    base_path_sedml = './sedml_models'
    tsv_file_path = '../sbml2amici'

    # list of all directories + SBML files
    list_directory_sedml = os.listdir(base_path_sedml)
    list_directory_sedml = sorted(list_directory_sedml)

    # list only specific models ---- should only simulate those models where sbml to amicic worked!
    for iModel in list_directory_sedml:

        if os.path.exists(base_path_sbml2amici + '/' + iModel):
            list_files = os.listdir(base_path_sbml2amici + '/' + iModel)
            list_files = sorted(list_files)                                                      # sorted() could maybe change the order needed for later

            for iFile in list_files:

                # Append additional row in .tsv file
                tsv_table = tsv_table.append({}, ignore_index=True)

                # save id in .tsv
                tsv_table.loc[counter].id = '{' + iModel + '}' + '_' + '{' + iFile + '}'

                try:
                    # read in SBML file for state variables
                    file = libsbml.readSBML(base_path_sedml + '/' + iModel + '/sbml_models/' + iFile + '.sbml')
                    all_properties = file.getModel()
                    num_states = len(all_properties.getListOfSpecies())
                    tsv_table.loc[counter].state_variables = num_states

                    # read in model
                    model = all_settings(iModel, iFile)                                         # call function from 'lexecute_loadModels.py'

                    # Create solver instance
                    solver = model.getSolver()

                    # set all settings
                    solver.setAbsoluteTolerance(atol)
                    solver.setRelativeTolerance(rtol)
                    solver.setLinearSolver(linSol)
                    solver.setLinearMultistepMethod(solAlg)

                    # clock simulation time while running the simulation using pre-defined settings
                    built_in_time = []
                    external_time = []
                    ind_time = []
                    end_time = []

                    try:
                        for iSim in range(0,99):
                            start_time = time.time()

                            sim_data = amici.runAmiciSimulation(model, solver)

                            end_time.append(time.time())                             # x1000 for milliseconds
                            ind_time.append(sim_data['cpu_time'])

                            external_time.append(1000*(end_time[iSim] - start_time))
                            if iSim == 0:
                                built_in_time.append(ind_time[iSim])                                # internal data
                            else:
                                built_in_time.append(ind_time[iSim] - ind_time[iSim - 1])

                        # take median of time_vector
                        # built_in_time.append(sim_data['cpu_time'])
                        internal = statistics.median(built_in_time)                                   # median internal data
                        external = statistics.median(external_time)

                        # save time data in .tsv
                        tsv_table.loc[counter].t_intern_ms = internal                                    # add internal to .tsv file
                        tsv_table.loc[counter].t_extern_ms = external

                        # np.set_printoptions(threshold=8, edgeitems=2)
                        # for key, value in sim_data.items():
                        #    print('%12s: ' % key, value)

                        # plot sim_data
                        # amici.plotting.plotStateTrajectories(sim_data)
                        # amici.plotting.plotObservableTrajectories(sim_data)

                        # save plot in therefore created folder
                        # if not os.path.exists('../sbml2amici/Figures/' + iModel + '/' + iModel):
                        #   os.makedirs('../sbml2amici/Figures/' + iModel + '/' + iModel)
                        # plt.savefig('../sbml2amici/Figures/' + iModel + '/' + iModel + '/' + iFile + '.png')

                        # show plot
                        # plt.show()

                        # raise counter
                        counter = counter + 1

                    except Exception as e:
                        error_info_3 = str(e)
                        # print('Model ' + iModel + '_' + iFile + ' could not be simulated with this setting!')
                        tsv_table.loc[counter].t_intern_ms = 'nan'
                        tsv_table.loc[counter].t_extern_ms = 'nan'
                        tsv_table.loc[counter].error_message = 'Error_3: ' + error_info_3

                        # raise counter
                        counter = counter + 1

                except Exception as e:
                    error_info_2 = str(e)
                    # print('Error_2: Loading Model ' + iModel + '_' + iFile + ' did not work!')
                    tsv_table.loc[counter].t_intern_ms = 'nan'
                    tsv_table.loc[counter].t_extern_ms = 'nan'
                    tsv_table.loc[counter].error_message = 'Error_2: ' + error_info_2

                    # raise counter
                    counter = counter + 1

        else:
            print('Error_1: Model ' + iModel + ' import to amici did not work!')

    # save data frame as .tsv file
    tsv_table.to_csv(path_or_buf=tolerance_path + '/' + s_atol + '_' + s_rtol + '.tsv', sep='\t', index=False)