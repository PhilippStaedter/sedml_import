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
    # create .tsv file
    tsv_table = pd.DataFrame(columns=['id', 't_intern', 't_extern'])

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

                try:
                    # Append additional row in .tsv file
                    tsv_table = tsv_table.append({}, ignore_index=True)

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
                    end_time = []

                    try:
                        for iSim in range(0,99):
                            start_time = time.time()

                            sim_data = amici.runAmiciSimulation(model, solver)

                            end_time.append(time.time())

                            external_time.append(end_time[iSim] - start_time)
                            # built_in_time = built_in_time.append(sim_data['cpu_time'])                # internal data

                        # take median of time_vector
                        # internal = statistics.median(built_in_time)                                   # median internal data
                        external = statistics.median(external_time)

                        # save data in .tsv
                        tsv_table.loc[counter].id = '{' + iModel + '}' + '_' + '{' + iFile + '}'
                        # tsv_table.loc[counter].t_intern = internal                                    # add internal to .tsv file
                        tsv_table.loc[counter].t_extern = external

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

                    except:
                        print('Model ' + iModel + '_' + iFile + ' could not be simulated with this setting!')

                except:
                    print('Loading Model ' + iModel + '_' + iFile + ' did not work!')

            else:
                print('Model ' + iModel + ' import to amici did not work!')

    # save data frame as .tsv file
    tsv_table.to_csv(path_or_buf=tsv_file_path + '/simulation_table.tsv', sep='\t', index=False)