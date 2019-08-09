# script to set the timepoints for all benchmark models
# always the exact intervals

import numpy as np
import os
import pandas as pd


def timePointsBenchmarkModels(iModel, iFile):


    # important paths
    benchmark_path = '../benchmark-models/hackathon_contributions_new_data_format'

    # list of all directories + SBML files
    list_directory_sedml = sorted(os.listdir(benchmark_path))  # (base_path_sedml)
    list_directory_sedml = list_directory_sedml[0:26]
    list_directory_sedml.remove('ReadMe.MD')

    # list only specific models ---- should only simulate those models where sbml to amicic worked!
    for iBenchmarkModel in list_directory_sedml:

        if iBenchmarkModel == iModel:

            list_directory_xml = [filename for filename in sorted(os.listdir(benchmark_path + '/' + iBenchmarkModel)) if filename.startswith('model_')]
            for iBenchmarkFile in list_directory_xml:
                iBenchmarkFile,_ = iBenchmarkFile.split('.',1)


                if iBenchmarkFile == iFile:
                    _,iFile = iFile.split('_',1)

                    # open measurmentData file
                    try:
                        tsv_file = pd.read_csv(benchmark_path + '/' + iModel + '/measurementData_' + iFile + '.tsv', sep='\t')
                        time_array = list(tsv_file['time'])
                        sim_start_time = time_array[0]
                    except:
                        print('No concrete time course known for model ' + iModel + '_' + iFile)


                    ######### doesn't work for unequal time intervals ########
                    ### what about negative timepoints?
                    ### what about constant time vector?
                    for iElement in range(1, len(time_array)):
                        if sim_start_time != 'inf':
                            if sim_start_time != time_array[iElement]:
                                if sim_start_time in time_array[iElement:]:
                                    index = time_array[iElement:].index(sim_start_time)
                                    time_array_2 = time_array[:index + iElement]
                                    break
                                else:
                                    time_array_2 = time_array
                                    break
                        else:
                            # simulation by hand from 0 to steady state in n time steps (n = len(time_array))
                            if iFile == 'model_Becker_Science2010__binding':
                                time_array = np.linspace(0, 0.05, 12)

                            elif iFile == 'model_Blasi_CellSystems2016':
                                time_array = np.linspace(0, 10, 18)

                            elif iFile == 'model_Blasi_CellSystems2016_allCombinations':
                                time_array = np.linspace(0, 10, 18)     # no measurment data file...

            break

    return time_array_2