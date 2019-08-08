# script to get the Y-testing vector for the predictor model

import pandas as pd
import os
import numpy as np


def sortby(x):
    try:
        return int(x[0])
    except ValueError:
        return float('inf')


def bestFit(X, Y, X_testing):

    # important paths
    benchmark_collection_path = '../benchmark-models/hackathon_contributions_new_data_format'

    ######### create data frame for all models #############
    all_columns = ['model', 'value']
    Y_testing = pd.DataFrame(columns=all_columns, data=[])
    all_categories = ['num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o']

    ######### get same Study data for all iterations ###########
    # set counter
    counter = 0

    # create a data frame for each category
    df_list = [pd.DataFrame(columns=['model', 'num_x'], data=[]),
               pd.DataFrame(columns=['model', 'num_r'], data=[]),
               pd.DataFrame(columns=['model', 'num_p'], data=[]),
               pd.DataFrame(columns=['model', 'p_n'], data=[]),
               pd.DataFrame(columns=['model', 'p_l'], data=[]),
               pd.DataFrame(columns=['model', 'p_q'], data=[]),
               pd.DataFrame(columns=['model', 'p_p'], data=[]),
               pd.DataFrame(columns=['model', 'p_e'], data=[]),
               pd.DataFrame(columns=['model', 'p_L'], data=[]),
               pd.DataFrame(columns=['model', 'p_Q'], data=[]),
               pd.DataFrame(columns=['model', 'p_P'], data=[]),
               pd.DataFrame(columns=['model', 'p_E'], data=[]),
               pd.DataFrame(columns=['model', 'p_o'], data=[])]

    for iStudyModel in range(0, len(X['model'])):

        # get right values into right data frame
        if iStudyModel == 0:
            # Append additional row in each data frame
            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame] = df_list[iDataFrame].append({}, ignore_index=True)

            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame]['model'][counter] = X['model'][iStudyModel]
                df_list[iDataFrame][all_categories[iDataFrame]][counter] = X[all_categories[iDataFrame]][iStudyModel]
            counter = counter + 1

        elif X['model'][iStudyModel - 1] != X['model'][iStudyModel]:
            # Append additional row in each data frame
            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame] = df_list[iDataFrame].append({}, ignore_index=True)

            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame]['model'][counter] = X['model'][iStudyModel]
                df_list[iDataFrame][all_categories[iDataFrame]][counter] = X[all_categories[iDataFrame]][iStudyModel]
            counter = counter + 1

        elif X['model'][iStudyModel - 1] == X['model'][iStudyModel] and X['num_x'][iStudyModel - 1] != X['num_x'][
            iStudyModel]:  # 'Levchenko case'
            # Append additional row in each data frame
            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame] = df_list[iDataFrame].append({}, ignore_index=True)

            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame]['model'][counter] = X['model'][iStudyModel]
                df_list[iDataFrame][all_categories[iDataFrame]][counter] = X[all_categories[iDataFrame]][iStudyModel]
            counter = counter + 1

    ######### Iterate over all Benchmark models and minimize category values ##########
    list_directory_benchmark = sorted(os.listdir(benchmark_collection_path))
    list_directory_benchmark = list_directory_benchmark[0:26]
    list_directory_benchmark.remove('ReadMe.MD')
    for iModel in list_directory_benchmark:

        #iModel = 'Becker_Science2010'

        list_directory_xml = [filename for filename in sorted(os.listdir(benchmark_collection_path + '/' + iModel)) if filename.startswith('model_')]
        for iXML in range(0, len(list_directory_xml)):

            #iXML = 1

            # print current model
            print(iModel + '_' + str(iXML))

            # reset counter
            counter = 0

            # create data frame as short version of Y_testing
            new_df = pd.DataFrame(columns=all_columns, data=[])



            mod_Benchmark = '{' + iModel + '}'

            for iBenchmarkModel in range(0, len(X_testing['model'])):
                if iModel != 'Becker_Science2010':
                    if X_testing['model'][iBenchmarkModel] == mod_Benchmark:
                        num_x_Benchmark = X_testing['num_x'][iBenchmarkModel]
                        num_r_Benchmark = X_testing['num_r'][iBenchmarkModel]
                        num_p_Benchmark = X_testing['num_p'][iBenchmarkModel]
                        p_n_Benchmark = X_testing['p_n'][iBenchmarkModel]
                        p_l_Benchmark = X_testing['p_l'][iBenchmarkModel]
                        p_q_Benchmark = X_testing['p_q'][iBenchmarkModel]
                        p_p_Benchmark = X_testing['p_p'][iBenchmarkModel]
                        p_e_Benchmark = X_testing['p_e'][iBenchmarkModel]
                        p_L_Benchmark = X_testing['p_L'][iBenchmarkModel]
                        p_Q_Benchmark = X_testing['p_Q'][iBenchmarkModel]
                        p_P_Benchmark = X_testing['p_P'][iBenchmarkModel]
                        p_E_Benchmark = X_testing['p_E'][iBenchmarkModel]
                        p_o_Benchmark = X_testing['p_o'][iBenchmarkModel]
                        break
                elif iModel == 'Becker_Science2010' and iXML == 0:
                    iBenchmarkModel = 40
                    num_x_Benchmark = X_testing['num_x'][iBenchmarkModel]
                    num_r_Benchmark = X_testing['num_r'][iBenchmarkModel]
                    num_p_Benchmark = X_testing['num_p'][iBenchmarkModel]
                    p_n_Benchmark = X_testing['p_n'][iBenchmarkModel]
                    p_l_Benchmark = X_testing['p_l'][iBenchmarkModel]
                    p_q_Benchmark = X_testing['p_q'][iBenchmarkModel]
                    p_p_Benchmark = X_testing['p_p'][iBenchmarkModel]
                    p_e_Benchmark = X_testing['p_e'][iBenchmarkModel]
                    p_L_Benchmark = X_testing['p_L'][iBenchmarkModel]
                    p_Q_Benchmark = X_testing['p_Q'][iBenchmarkModel]
                    p_P_Benchmark = X_testing['p_P'][iBenchmarkModel]
                    p_E_Benchmark = X_testing['p_E'][iBenchmarkModel]
                    p_o_Benchmark = X_testing['p_o'][iBenchmarkModel]
                    break
                elif iModel == 'Becker_Science2010' and iXML == 1:
                    iBenchmarkModel = 80
                    num_x_Benchmark = X_testing['num_x'][iBenchmarkModel]
                    num_r_Benchmark = X_testing['num_r'][iBenchmarkModel]
                    num_p_Benchmark = X_testing['num_p'][iBenchmarkModel]
                    p_n_Benchmark = X_testing['p_n'][iBenchmarkModel]
                    p_l_Benchmark = X_testing['p_l'][iBenchmarkModel]
                    p_q_Benchmark = X_testing['p_q'][iBenchmarkModel]
                    p_p_Benchmark = X_testing['p_p'][iBenchmarkModel]
                    p_e_Benchmark = X_testing['p_e'][iBenchmarkModel]
                    p_L_Benchmark = X_testing['p_L'][iBenchmarkModel]
                    p_Q_Benchmark = X_testing['p_Q'][iBenchmarkModel]
                    p_P_Benchmark = X_testing['p_P'][iBenchmarkModel]
                    p_E_Benchmark = X_testing['p_E'][iBenchmarkModel]
                    p_o_Benchmark = X_testing['p_o'][iBenchmarkModel]
                    break



            all_benchmark = [num_x_Benchmark, num_r_Benchmark, num_p_Benchmark, p_n_Benchmark, p_l_Benchmark,
                             p_q_Benchmark, p_p_Benchmark, p_e_Benchmark, p_L_Benchmark, p_Q_Benchmark,
                             p_P_Benchmark, p_E_Benchmark, p_o_Benchmark]


            # compare values
            list_all = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
            for iCat in range(0, len(list_all)):
                for iElement in range(0, len(df_list[0]['model'])):
                    num_x_diff = np.abs(all_benchmark[iCat] - df_list[iCat][all_categories[iCat]][iElement])
                    model = df_list[iCat]['model'][iElement]
                    list_all[iCat].append([num_x_diff, model])

            for iCat in range(0, len(list_all)):
                list_all[iCat].sort(key=sortby)

            # rank models
            total_ranking = []
            for iStudyModel in range(0, len(list_all[0])):
                model_rankings = []
                for iCat in range(0, len(list_all)):
                    for iElement in range(0, len(list_all[0])):
                        if X['model'][iStudyModel * 40] in list_all[iCat][iElement]:
                            model_rankings.append(iElement)
                            break
                total_ranking.append([sum(model_rankings), X['model'][iStudyModel * 40]])

            # best fit
            total_ranking.sort(key=sortby)

            ######## fill in Y_tesing vector
            # set new counter
            counter = 0

            # Append additional row in each data frame
            new_df = new_df.append({}, ignore_index=True)
            new_df['model'][0] = total_ranking[0][1]
            new_df = pd.concat([new_df] * 40, ignore_index=True)
            for iValue in range(0,len(Y['model'])):
                if Y['model'][iValue] == total_ranking[0][1]:
                    new_df['value'][counter] = Y['value'][iValue]
                    counter = counter + 1

            # build the y_testing vector by appending data frames
            Y_testing = Y_testing.append(new_df, ignore_index=True)



    return Y_testing