# script to check if trajectories and data are simulated correctly

import pandas as pd
import os
import matplotlib.pyplot as plt
from setObservables import *


# important paths
sedml_path = './sedml_models'


##### get data
#sedml_models = sorted(os.listdir(sedml_path))
#for iModel in sedml_models:

for iModel in ['adlung2017_fig2bto2e']:

    # new folder for all figures
    if not os.path.exists(sedml_path + '/' + iModel + '/figures_observables'):
        os.makedirs(sedml_path + '/' + iModel + '/figures_observables')

    if os.path.exists(sedml_path + '/' + iModel + '/experimental_data_rearranged'):

        sbml_models = sorted(os.listdir(sedml_path + '/' + iModel + '/sbml_models'))
        for iFile in sbml_models:
            iFile,_ = iFile.split('.')

            all_expdata_files = sorted(os.listdir(sedml_path + '/' + iModel + '/experimental_data'))
            all_petab_files = sorted(os.listdir(sedml_path + '/' + iModel + '/experimental_data_rearranged'))
            for iFi in range(0, len(all_petab_files)):
                # open expdata file
                xls_file = pd.ExcelFile(sedml_path + '/' + iModel + '/experimental_data/' + all_expdata_files[iFi])
                if len(xls_file.sheet_names) > 1:
                    expdata_file = pd.read_excel(xls_file, 'Data')
                else:
                    expdata_file = pd.read_excel(sedml_path + '/' + iModel + '/experimental_data/' + all_expdata_files[iFi])
                # open petab file
                petab_file = pd.read_csv(sedml_path + '/' + iModel + '/experimental_data_rearranged/' + all_petab_files[iFi], sep='\t')

                # extend folder structure
                if not os.path.exists(sedml_path + '/' + iModel + '/figures_observables/' + iFile):
                    os.makedirs(sedml_path + '/' + iModel + '/figures_observables/' + iFile)

                # get time and measurment column
                species = list(expdata_file.columns)
                del species[0]
                df = []
                for iDataFrame in range(0, len(species)):
                    df.append(pd.DataFrame())
                for iSpecies in range(0, len(species)):
                    time_data = []
                    measurment_data = []
                    for iData in range(0, len(petab_file['observableId'])):
                        if petab_file['observableId'][iData] == species[iSpecies]:
                            time_data.append(petab_file['time'][iData])
                            measurment_data.append(petab_file['measurment'][iData])
                    df[iSpecies]['time'] = time_data
                    df[iSpecies]['data'] = measurment_data


                ##### get trajectories
                # get whole input
                model = plotObservables(iModel,iFile)                                                                   # call function 'setObservables'

                # Create solver instance
                solver = model.getSolver()

                # do one simulation + check for status
                sim_data = amici.runAmiciSimulation(model, solver)
                status = sim_data['status']


                ##### plot observable trajectories
                #left = 0.15
                #bottom = 0.7
                #width = 0.3
                #height = 0.2
                #row_counter = 0.4
                #bottom_counter = 0.3

                obs_data = sim_data['y'].transpose()
                for iObs in range(0, len(obs_data)):

                    _, ax = plt.subplots()
                    # first plot
                    #if iObs == 0 or iObs == 1:
                     #   ax = plt.axes([left + iObs * row_counter, bottom, width, height])
                    #if iObs == 2 or iObs == 3:
                      #  ax = plt.axes([left + (iObs - 2) * row_counter, bottom - bottom_counter, width, height])
                    #if iObs == 4 or iObs == 5:
                      #  ax = plt.axes([left + (iObs - 4) * row_counter, bottom - 2 * bottom_counter, width, height])
                    amici.plotting.plotObservableTrajectories(sim_data, observable_indices=range(0,len(obs_data))[iObs:iObs+1], ax=ax)
                    ax.scatter(df[iObs]['time'], df[iObs]['data'], c='red')
                    ax.set_title(species[iObs])
                    #ax.set_xlim([-0.5, 240])
                    #ax.set_ylim([-0.01, 1.1])
                    plt.tight_layout()
                    plt.savefig(sedml_path + '/' + iModel + '/figures_observables/' + iFile + '/' + iFile)
                    #plt.show()

debug = 4