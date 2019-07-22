# goal: open a git repository for all sbml to amici error messages

import pandas as pd
import os
import numpy as np


# important paths
error_path = '../sbml2amici/table_modified.tsv'
save_path = '../sbml2amici'

# open .tsv file
error_file = pd.read_csv(error_path, sep='\t')

# get id and error message column
del error_file['states']
del error_file['reactions']

# remove 'OK' rows
for iRow in range(0, len(error_file['id'])):
    if error_file['error_message'][iRow] == 'OK':
        error_file = error_file.drop(iRow, axis=0)

# rearrange all errors
error_file = error_file.sort_values(by ='error_message')
new_index = pd.Series([i for i in range(len(error_file['id']))])
error_file = error_file.set_index(new_index)

# get list of all unique error messages
unique_error = []
counter = 1
for iError in range(0, len(error_file['id'])):
    if iError == 0:
        unique_error.append(error_file['error_message'][iError])
    else:
        if not error_file['error_message'][iError] in unique_error:
            if not error_file['error_message'][iError].split(' ',1)[0] in unique_error[iError - counter]:
                unique_error.append(error_file['error_message'][iError])
            else:
                counter = counter + 1
                continue
        else:
            counter = counter + 1

# get absolute frequency in new column
error_file['absolute frequency (descending order)'] = pd.Series(np.zeros(len(error_file['id']), dtype=int))
c1 = 0; c2 = 0; c3 = 0; c4 = 0
c5 = 0; c6 = 0; c7 = 0; c8 = 0
for iError in range(0, len(error_file['id'])):
    if error_file['error_message'][iError].split(' ',1)[0] == unique_error[0].split(' ',1)[0]:
        c1 = c1 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[1].split(' ',1)[0]:
        c2 = c2 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[2].split(' ',1)[0]:
        c3 = c3 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[3].split(' ',1)[0]:
        c4 = c4 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[4].split(' ',1)[0]:
        c5 = c5 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[5].split(' ',1)[0]:
        c6 = c6 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[6].split(' ',1)[0]:
        c7 = c7 + 1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[7].split(' ',1)[0]:
        c8 = c8 + 1
for iError in range(0, len(error_file['id'])):
    if error_file['error_message'][iError].split(' ',1)[0] == unique_error[0].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c1
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[1].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c2
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[2].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c3
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[3].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c4
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[4].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c5
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[5].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c6
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[6].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c7
    elif error_file['error_message'][iError].split(' ',1)[0] == unique_error[7].split(' ',1)[0]:
        error_file['absolute frequency (descending order)'][iError] = c8

# sort one final time after absolute frequency
error_file = error_file.sort_values(by ='absolute frequency (descending order)', ascending=False)
error_file = error_file.set_index(new_index)

# save new table
error_file.to_csv(path_or_buf=save_path + '/error_table.tsv', sep='\t', index=False)