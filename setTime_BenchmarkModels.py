# script to set the timepoints for all benchmark models
# always the exact intervals

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

                if iBenchmarkFile == iFile:

                    # open measurmentData file
                    tsv_file = pd.read_csv(benchmark_path + '/' + iModel + '/measurementData_' + iFile + '.tsv')
                    time_array = list(tsv_file['time'])
                    sim_start_time = time_array[0]

                    if sim_start_time in time_array[1:]:
                        index = time_array[1:].index(sim_start_time)
                        time_array = time_array[:index-1]
                    else:
                        time_array = time_array



    return time_array