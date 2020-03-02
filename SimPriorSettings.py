# python script to simulate all sbml and xml models using amici and extract necessary information

from execute_loadModels import *
import amici.plotting
import time
import statistics
import pandas as pd


def prior(atol, rtol, linSol, iter, solAlg, maxStep):

    # Create new folder structure for study
    tolerance_path = '../prior/WholeStudy'
    if not os.path.exists(tolerance_path):
        os.makedirs(tolerance_path)

    # save name

    # set row counter for .tsv file
    counter = 0

    # set number of repetitions for simulation
    sim_rep = 1

    # insert specific model properties as strings, e.g.:
    base_path_sbml2amici = '../sbml2amici/amici_models_newest_version_0.10.19'

    # list of all directories + SBML files
    list_directory_sedml = sorted(os.listdir(base_path_sbml2amici))
    #list_directory_sedml = list_directory_sedml[27:]
    #list_directory_sedml.remove('ReadMe.MD')

    # list only specific models ---- should only simulate those models where sbml to amici worked!
    for iModel in list_directory_sedml:

        # create subfolder if not already existing
        if not os.path.exists(tolerance_path + '/' + iModel):
            os.makedirs(tolerance_path + '/' + iModel)

        #iModel = 'Becker_Science2010'

        if os.path.exists(base_path_sbml2amici + '/' + iModel):
            list_files = sorted(os.listdir(base_path_sbml2amici + '/' + iModel))

            #list_directory_xml = [filename for filename in sorted(os.listdir(benchmark_path + '/' + iModel)) if filename.startswith('model_')]
            for iFile in list_files:                                                     #list_directory_xml:

                # create .tsv file
                tsv_table = pd.DataFrame(columns=[], data=[])

                try:
                    # read in model
                    model = all_settings(iModel, iFile)                                         ##################### call function from 'execute_loadModels.py'

                    # get time course
                    all_timepoints = list(model.getTimepoints())

                    # get number of species
                    num_species = model.getNumSpecies()
                    all_species_names = []
                    for iSpecies in range(0, num_species):
                        all_species_names.append(model.getSpecies(iSpecies).getId())

                    # add rows and rename index to species names
                    for iSpecies in range(0, num_species):
                        tsv_table = tsv_table.append({}, ignore_index=True)
                    for iSpecies in range(0, num_species):
                        tsv_table = tsv_table.rename(index={iSpecies:all_species_names[iSpecies]})

                    # add columns and rename to 'units' and timepoints
                    for iTimepoint in range(0, len(all_timepoints + 1)):
                        if iTimepoint == 0:
                            tsv_table['unit'] = pd.Series(index=tsv_table.index)
                        else:
                            tsv_table['t_' + f'{iTimepoint - 1}' + ' = ' + str(all_timepoints[iTimepoint])] = pd.Series(index=tsv_table.index)


                    # Create solver instance
                    solver = model.getSolver()

                    # set all settings
                    solver.setAbsoluteTolerance(atol)
                    solver.setRelativeTolerance(rtol)
                    solver.setLinearSolver(linSol)
                    solver.setNonlinearSolverIteration(iter)
                    solver.setLinearMultistepMethod(solAlg)
                    solver.setMaxSteps(maxStep)

                    # simulate model
                    try:
                        # set stability limit detection
                        solver.setStabilityLimitFlag(False)

                        # simulate model
                        sim_data = amici.runAmiciSimulation(model, solver)

                    except Exception as e:
                        print(str(e))
                        sys.exit(0)

                    # fill data into the data frame


                except Exception as e:
                    print(str(e))
                    sys.exit(0)

                # save data frame as .tsv file
                tsv_table.to_csv(path_or_buf=tolerance_path + '/' + iModel + '/' + iFile + '.tsv', sep='\t', index=False)