# script to get the Y-testing vector for the predictor model

import pandas as pd
import os

def bestFit(X, Y, X_testing):

    # important paths
    benchmark_collection_path = '../benchmark-models/hackathon_contributions_new_data_format'

    ######### create data frame for all models #############
    all_columns = ['model', 'value']
    new_df = pd.DataFrame(columns=all_columns, data=[])
    all_categories = ['num_x', 'num_r', 'num_p', 'p_n', 'p_l', 'p_q', 'p_p', 'p_e', 'p_L', 'p_Q', 'p_P', 'p_E', 'p_o']

    ######### Iterate over all Benchmark models and minimize category values ##########
    # set counter
    counter = 0

    list_directory_benchmark = sorted(os.listdir(benchmark_collection_path))
    list_directory_benchmark = list_directory_benchmark[0:26]
    list_directory_benchmark.remove('ReadMe.MD')
    for iModel in list_directory_benchmark:

        # iModel = 'Becker_Science2010'

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

        mod_Benchmark = '{' + iModel + '}'
        for iBenchmarkModel in range(0, len(X_testing['model'])):
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

        for iStudyModel in range(0, len(X['model'])):

            # Append additional row in each data frame
            for iDataFrame in range(0, len(df_list)):
                df_list[iDataFrame] = df_list[iDataFrame].append({}, ignore_index=True)

            # get right values into right data frame
            if iStudyModel == 0:
                for iDataFrame in range(0, len(df_list)):
                    df_list[iDataFrame]['model'][counter] = X['model'][iStudyModel]
                    df_list[iDataFrame][all_categories[iDataFrame]][counter] = X[all_categories[iDataFrame]][iStudyModel]
                    counter = counter + 1

            elif X['model'][iStudyModel - 1] != X['model'][iStudyModel]:
                for iDataFrame in range(0, len(df_list)):
                    df_list[iDataFrame]['model'][counter] = X['model'][iStudyModel]
                    df_list[iDataFrame][all_categories[iDataFrame]][counter] = X[all_categories[iDataFrame]][iStudyModel]
                    counter = counter + 1

        # compare values and rank models







    return Y_testing



'''
                num_x_Study = num_x_Study.append({}, ignore_index=True)
                num_r_Study = num_r_Study.append({}, ignore_index=True)
                num_p_Study = num_p_Study.append({}, ignore_index=True)
                p_n_Study = p_n_Study.append({}, ignore_index=True)
                p_l_Study = p_l_Study.append({}, ignore_index=True)
                p_q_Study = p_q_Study.append({}, ignore_index=True)
                p_p_Study = p_p_Study.append({}, ignore_index=True)
                p_e_Study = p_e_Study.append({}, ignore_index=True)
                p_L_Study = p_L_Study.append({}, ignore_index=True)
                p_Q_Study = p_Q_Study.append({}, ignore_index=True)
                p_P_Study = p_P_Study.append({}, ignore_index=True)
                p_E_Study = p_E_Study.append({}, ignore_index=True)
                p_o_Study = p_o_Study.append({}, ignore_index=True)
'''