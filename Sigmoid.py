# returns a data frame with all not-round values of the sigmoid function

import pandas as pd
import numpy as np

def valuesSigmoid(ExpSigmoid, data_file, loop):

    all_exponents = list(ExpSigmoid)

    # create data frame for all not-rounded results
    if loop == 0:
        id = data_file['model'][:5280]
    elif loop == 1:
        id = pd.Series(np.concatenate((data_file['model'][:1320], data_file['model'][2640:])))
    elif loop == 2:
        id = pd.Series(np.concatenate((data_file['model'][:2640], data_file['model'][3960:])))
    elif loop == 3:
        id = pd.Series(np.concatenate((data_file['model'][:3960], data_file['model'][5280:])))
    elif loop == 4:
        id = data_file['model'][1320:]

    df_results = pd.DataFrame(columns=['model', 'h(x)'], data=[])
    df_results['model'] = id

    counter = 0
    for iExp in range(0, len(all_exponents)):

        result = 1 / (1 + np.exp(-all_exponents[iExp]))

        if result < 0 or result > 1:
            print('Error: The result ' + result + ' is negative or bigger then one!')

        df_results['h(x)'][counter] = result
        counter = counter + 1


    return df_results