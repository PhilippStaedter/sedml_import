# script to rearrange experimnetal data .csv file

import os
import pandas as pd
import numpy as np
import libsedml
import libsbml




# build new data frame
df = pd.DataFrame(columns=['observableId', 'preequilibrationConditionId', 'simulationConditionId',
                           'measurment', 'time', 'observableParameters', 'noiseParameters',
                           'observableTransformation', 'noiseDistribution'], data=[])

# get all experimental data files
list_directory_sedml = sorted(os.listdir('./sedml_models'))

for iModel in list_directory_sedml:

    iModel = 'bachmann2011'

    # create new folder for all new dataframes
    if not os.path.exists('./sedml_models/' + iModel + '/experimental_data_rearranged'):
        os.makedirs('./sedml_models/' + iModel + '/experimental_data_rearranged')

    if os.path.exists('./sedml_models/' + iModel + '/experimental_data'):
        list_directory_expdata = sorted(os.listdir('./sedml_models/' + iModel + '/experimental_data'))
        del list_directory_expdata[0]

        for iData in list_directory_expdata:

            # read .xls file
            xls_file_path = './sedml_models/' + iModel + '/experimental_data/'+ iData
            expdata_name, rest = iData.split('.',1)
            expdata_file = pd.read_excel(xls_file_path)

            # time column
            time_data = expdata_file['time']
            del time_data[0]
            time_data.reset_index(inplace=True, drop=True)

            # get data frames as functions
            columns = list(expdata_file.columns)

            for iDataFrame in range(0, len(columns) - 1):

                # build new data frame
                df_new = pd.DataFrame(columns=['observableId', 'preequilibrationConditionId', 'simulationConditionId',
                                           'measurment', 'time', 'observableParameters', 'noiseParameters',
                                           'observableTransformation', 'noiseDistribution'], data=[])

                ############# get input
                ###### species
                new_species = []
                for iNumber in range(0, len(time_data)):
                    new_species.append(columns[iDataFrame + 1])
                new_species = pd.Series(new_species)

                ###### measurment
                new_measurment = expdata_file[columns[iDataFrame + 1]]
                del new_measurment[0]
                new_measurment.reset_index(inplace=True, drop=True)                                                     # need reindexing from e.g. [1:14] to [0:13]

                ###### observable parameters
                new_observables = []

                sedml_file = libsedml.readSedML('./sedml_models/' + iModel + '/' + iModel + '.sedml')

                # get number of tasks and observables
                num_task = sedml_file.getNumTasks()
                num_obs = sedml_file.getNumDataGenerators()

                for iTask in range(0, num_task):
                    task_id = sedml_file.getTask(iTask).getId()

                    # create list with all parameter-ids to check for uniqueness
                    almost_all_par_id = []

                    for iObservable in range(0, num_obs):
                        # get important formula
                        obs_Formula = libsedml.formulaToString(sedml_file.getDataGenerator(iObservable).getMath())
                        obs_Id = sedml_file.getDataGenerator(iObservable).getId()
                        # SBML_model_Id,Observable_Id = obs_Id.split('_',1)
                        new_obs_Id = 'observable_' + obs_Id

                        # get list of parameters
                        list_par_id = []
                        list_par_value = []
                        num_par = sedml_file.getDataGenerator(iObservable).getNumParameters()
                        if num_par == 0:
                            print(obs_Id + ' has no parameters as observables!')
                        else:
                            data_generator_name = sedml_file.getDataGenerator(iObservable).getName()
                            for iCount in range(0, num_par):
                                list_par_id.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getId())
                                list_par_value.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getValue())
                                almost_all_par_id.append(sedml_file.getDataGenerator(iObservable).getParameter(iCount).getId())

                                # check for uniqueness of parameter-ids
                                for iNum in range(0, len(almost_all_par_id)):
                                    all_par_id = almost_all_par_id[iNum]
                                    almost_all_par_id.remove(almost_all_par_id[len(almost_all_par_id) - 1])
                                    last_element = list(all_par_id[len(all_par_id) - 1])
                                    intersection = [i for i in last_element if i in almost_all_par_id]
                                    if len(intersection) != 0:
                                        print('Two or more parameters have the same Id!')
                                        # sys.exit(1)

                            # get correct observables
                            if data_generator_name == new_species[0]:
                                correct_string = list_par_id[0]
                                del list_par_id[0]
                                for iObs in list_par_id:
                                    correct_string = correct_string + ';' + iObs
                                for iNumber in range(0, len(time_data)):
                                    new_observables.append(correct_string)
                                new_observables = pd.Series(new_observables)



                # set input
                df_new['observableId'] = new_species
                df_new['measurment'] = new_measurment
                df_new['time'] = time_data
                df_new['observableParameters'] = new_observables


                # concatenate data frames
                df = df.append(df_new, ignore_index=True)

            #### save data frame as .tsv
            df.to_csv('./sedml_models/' + iModel + '/experimental_data_rearranged/' + iModel + '.tsv', sep='\t', index=False)

    else:
        print(iModel + ' has no experimental data file!')