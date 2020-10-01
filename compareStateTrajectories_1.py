# script 1 to compare state trajectories from JWS with trajectories of the AMICI simulation
# => creates two important .tsv files

# Attention:    boundary conditions are not being simulated by JWS!

from execute_loadModels import *
from JWS_changeValues import *
import amici.plotting
import numpy as np
import libsbml
import libsedml
import pandas as pd
import os
import urllib.request
import requests
import json
import itertools
import time



def compStaTraj(delete_counter, Algorithm, Iterative, Linear, Tolerances):
    # create new folder for all json files
    if not os.path.exists('./json_folder'):
        os.makedirs('./json_folder')

    # set settings for simulation
    algorithm = [1, 2]
    if Algorithm != '':
        Index_correct_algorithm = algorithm.index(Algorithm)
        algorithm = algorithm[Index_correct_algorithm:]
    for solAlg in algorithm:

        iterative = [1, 2]
        if Iterative != '':
            Index_correct_nonlinsol = iterative.index(Iterative)
            iterative = iterative[Index_correct_nonlinsol:]
        for nonLinSol in iterative:

            linearsol = [1, 6, 7]#, 8, 9]
            if Linear != '':
                Index_correct_linearsol = linearsol.index(Linear)
                linearsol = linearsol[Index_correct_linearsol:]
            for linSol in linearsol:

                Tolerance_combination = [[1e-6, 1e-8], [1e-8, 1e-6]]#, [1e-8, 1e-16], [1e-16, 1e-8],
                                         #[1e-10, 1e-12], [1e-12, 1e-10], [1e-14, 1e-14]]
                if Tolerances != '':
                    Index_correct_tolerances = Tolerance_combination.index(Tolerances)
                    Tolerance_combination = Tolerance_combination[Index_correct_tolerances :]
                for iTolerance in Tolerance_combination:
                    start = time.time()

                    # split atol and rtol for naming purposes
                    _,atol_exp = str(iTolerance[0]).split('-')
                    _,rtol_exp = str(iTolerance[1]).split('-')
                    if len(atol_exp) != 2:
                        atol_exp = '0' + atol_exp
                    if len(rtol_exp) != 2:
                        rtol_exp = '0' + rtol_exp

                    # get name of jws reference
                    url = "https://jjj.bio.vu.nl/rest/models/?format=json"
                    view_source = requests.get(url)
                    json_string = view_source.text
                    json_dictionary = json.loads(json_string)

                    # get all models
                    list_directory_amici = sorted(os.listdir('../sbml2amici/test'))
                    if delete_counter != 0:
                        del list_directory_amici[0:delete_counter]

                    for iMod in range(0, len(list_directory_amici)):

                        iModel = list_directory_amici[iMod]
                        #list_files = sorted(os.listdir('./sedml_models/' + iModel + '/sbml_models'))
                        list_files = sorted(os.listdir('../sbml2amici/0.10.19_without_correct/' + iModel))

                        for iFile in list_files:
                            # iFile without .sbml extension
                            #iFile, extension = iFile.split('.', 1)

                            '''
                            # if this file is part of '../sbml2amici/correct_amici_models_paper', omit it
                            list_directory_correct_amici = sorted(os.listdir('../sbml2amici/correct_amici_models_paper'))
                            if iModel in list_directory_correct_amici:
                                list_files_correct_amici = sorted(os.listdir('../sbml2amici/correct_amici_models_paper/' + iModel))
                                if iFile in list_files_correct_amici:
                                    break
                            '''

                            # important paths
                            json_save_path = './json_folder/' + f'json_files_{solAlg}_{nonLinSol}_{linSol}_{atol_exp}_{rtol_exp}' \
                                             + '/' + iModel + '/' + iFile
                            sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'
                            sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'
                            BioModels_path = './BioModelsDatabase_models'


                            if os.path.exists(BioModels_path + '/' + iModel):
                                print('Model is not part of JWS-database!')
                            else:
                                # Open SBML file
                                sbml_model = libsbml.readSBML(sbml_path)

                                # get right model reference from sbml model
                                parse_name_model = sbml_model.getModel().getId()
                                for iCount in range(0, len(json_dictionary)):
                                    parse_name_jws = json_dictionary[iCount]['slug']
                                    if parse_name_model == parse_name_jws:
                                        model_reference = json_dictionary[iCount]['slug']
                                        break
                                # elements in json_dictionary are only lower case --- the sbml model has upper case models
                                try:
                                    model_reference
                                except:
                                    wrong_model_name = ["".join(x) for _, x in itertools.groupby(parse_name_model,
                                                                                                 key=str.isdigit)]
                                    if wrong_model_name[0].islower() == False:
                                        correct_model_letters = wrong_model_name[0].lower()
                                        correct_model_name = correct_model_letters + wrong_model_name[1]
                                        for iCount in range(0, len(json_dictionary)):
                                            parse_name_jws = json_dictionary[iCount]['slug']
                                            if correct_model_name == parse_name_jws:
                                                model_reference = json_dictionary[iCount]['slug']
                                                break
                                # check if 'all_settings' works
                                try:
                                    # Get whole model
                                    model = all_settings(iModel, iFile)

                                    # create folder
                                    if not os.path.exists(json_save_path):
                                        os.makedirs(json_save_path)
                                except:
                                    print('Model ' + iModel + ' extension is missing!')
                                    continue


                                ######### jws simulation
                                # Get time data with num_time_points == 100
                                t_data = model.getTimepoints()
                                sim_start_time = t_data[0]
                                sim_end_time = t_data[len(t_data) - 1]
                                sim_num_time_points = 101
                                model.setTimepoints(np.linspace(sim_start_time, sim_end_time, sim_num_time_points))

                                # Open sedml file
                                sedml_model = libsedml.readSedML(sedml_path)

                                # import all changes from SEDML
                                list_of_strings = JWS_changeValues(iFile, sedml_model)

                                # Get Url with all changes
                                # <species 1>=<amount>
                                # <parameter 1>=<value>, compartment == parameter (in this case)
                                url = 'https://jjj.bio.vu.nl/rest/models/' + model_reference + '/time_evolution?time_end=' + \
                                      str(sim_end_time) + ';species=all;'

                                for iStr in list_of_strings:
                                    url = url + iStr

                                #### Save .json file
                                urllib.request.urlretrieve(url, json_save_path + '/' + iFile + '_JWS_simulation.json')

                                #### write as .csv file
                                json_2_csv = pd.read_json(json_save_path + '/' + iFile + '_JWS_simulation.json')
                                json_2_csv.to_csv(json_save_path + '/' + iFile + '_JWS_simulation.csv', sep='\t', index=False)

                                # open new .csv file
                                tsv_file = pd.read_csv(json_save_path + '/' + iFile + '_JWS_simulation.csv', sep='\t')

                                # columns names of .tsv file
                                column_names = list(tsv_file.columns)
                                column_names.remove('time')
                                del tsv_file['time']

                                ########## model simulation
                                # Create solver instance
                                solver = model.getSolver()

                                # set all settings
                                solver.setAbsoluteTolerance(iTolerance[0])
                                solver.setRelativeTolerance(iTolerance[1])
                                solver.setLinearSolver(linSol)
                                solver.setNonlinearSolverIteration(nonLinSol)
                                solver.setLinearMultistepMethod(solAlg)

                                # set stability flag for Adams-Moulton
                                if solAlg == 1:
                                    solver.setStabilityLimitFlag(False)

                                # Simulate model
                                sim_data = amici.runAmiciSimulation(model, solver)

                                # print some values
                                for key, value in sim_data.items():
                                    print('%12s: ' % key, value)

                                # Get state trajectory
                                state_trajectory = sim_data['x']

                                # Delete all trajectories for boundary conditions
                                delete_counter = 0
                                all_properties = sbml_model.getModel()
                                for iSpec in range(0, all_properties.getNumSpecies()):
                                    all_species = all_properties.getSpecies(iSpec)
                                    if all_species.getBoundaryCondition() == True:
                                        state_trajectory = state_trajectory.transpose()
                                        if delete_counter == 0:
                                            state_trajectory = np.delete(state_trajectory, iSpec, 0)
                                        else:
                                            state_trajectory = np.delete(state_trajectory, iSpec - delete_counter, 0)
                                        state_trajectory = state_trajectory.transpose()
                                        delete_counter = delete_counter + 1

                                # Convert ndarray 'state-trajectory' to data frame and save it
                                try:
                                    df_state_trajectory = pd.DataFrame(columns=column_names, data=state_trajectory)
                                except:
                                    print('Try again for model ' + list_directory_amici[iMod] + '_' + iFile)
                                    compStaTraj(iMod, solAlg, nonLinSol, linSol, iTolerance)
                                df_state_trajectory.to_csv(json_save_path + '/' + iFile + '_model_simulation.csv', sep='\t')
                    end = time.time()
                    print(end - start)

                # reset values - linear solver
                Algorithm = ''
                Iterative = ''
                Linear = ''
                Tolerances = ''

            # reset values - nonlinear solver
            Algorithm = ''
            Iterative = ''
            Linear = ''
            Tolerances = ''

        # reset values - solver algorithm
        Algorithm = ''
        Iterative = ''
        Linear = ''
        Tolerances = ''

    print('All combinations have been satisfied!')
    sys.exit()

# call function, starting with no models to delete
compStaTraj(0, '', '', '', '')
