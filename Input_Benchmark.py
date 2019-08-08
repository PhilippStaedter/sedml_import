# script to get the input and output vector for the predictor model

import sklearn
import os
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from averageTime import *
from KineticLaw import *
import libsbml

# important paths
output_data_path = '../bachelor_thesis/SolverAlgorithm/Test_Data.tsv'
benchmark_collection_path = '../benchmark-models/hackathon_contributions_new_data_format'
tsv_save_path = '../bachelor_thesis/SolverAlgorithm'

# open output data file
output_data_file = pd.read_csv(output_data_path, sep='\t')


######### create data frame for all models #############
all_columns = ['model', 'num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o', 'combinations']
new_df = pd.DataFrame(columns=all_columns, data=[])

################ get INPUT data ################
# set counter
counter = 0

list_directory_benchmark = sorted(os.listdir(benchmark_collection_path))
list_directory_benchmark = list_directory_benchmark[0:26]
list_directory_benchmark.remove('ReadMe.MD')
for iModel in list_directory_benchmark:

    #iModel = 'Becker_Science2010'

    mod_Benchmark = '{' + iModel + '}'
    print(mod_Benchmark)

    # list_directory_xml = sorted(os.listdir(benchmark_collectin_path + '/' + iModel))
    list_directory_xml = [filename for filename in sorted(os.listdir(benchmark_collection_path + '/' + iModel)) if filename.startswith('model_')]
    for iXML in list_directory_xml:

        # new data frame
        df = pd.DataFrame(columns=all_columns, data=[])

        # Append additional row in .tsv file
        df = df.append({}, ignore_index=True)

        # XML file
        xml_file = libsbml.readSBML(benchmark_collection_path + '/' + iModel + '/' + iXML)

        #### get type of kinetic
        all_kinetics = getKineticLaw(iModel, iXML)

        #### get num_x, num_p, num_r
        num_x = xml_file.getModel().getNumSpecies()
        num_r = xml_file.getModel().getNumReactions()
        num_p = xml_file.getModel().getNumParameters()

        p_n = all_kinetics[0]
        p_l = all_kinetics[1]
        p_q = all_kinetics[2]
        p_p = all_kinetics[3]
        p_e = all_kinetics[4]
        p_L = all_kinetics[5]  # <==> Michaelis Menten ?
        p_Q = all_kinetics[6]  # <==
        p_P = all_kinetics[7]  # ==
        p_E = all_kinetics[8]  # ==> Hill ?
        p_o = all_kinetics[9]
        all_data = [num_x, num_r, num_p, p_n, p_l, p_q, p_p, p_e, p_L, p_Q, p_P, p_E, p_o]

        #### save all_data in data frame
        df['model'][counter] = mod_Benchmark
        df['num_x'][counter] = num_x
        df['num_r'][counter] = num_r
        df['num_p'][counter] = num_p
        df['p_n'][counter] = p_n
        df['p_l'][counter] = p_l
        df['p_q'][counter] = p_q
        df['p_p'][counter] = p_p
        df['p_e'][counter] = p_e
        df['p_L'][counter] = p_L
        df['p_Q'][counter] = p_Q
        df['p_P'][counter] = p_P
        df['p_E'][counter] = p_E
        df['p_o'][counter] = p_o

        # duplicate the newly created row 40 times for all different combinations
        df = pd.concat([df] * len(output_data_file['combinations']), ignore_index=True)
        for iComb in range(0, len(output_data_file['combinations'])):
            df.loc[counter].combinations = output_data_file['combinations'][iComb]
            counter = counter + 1

        # reset counter
        counter = 0

        # append df to new_df
        new_df = new_df.append(df, ignore_index=True)


############ save data frames as .tsv file ###############
new_df.to_csv(path_or_buf=tsv_save_path + '/Benchmark_Input_Data.tsv', sep='\t', index=False)
