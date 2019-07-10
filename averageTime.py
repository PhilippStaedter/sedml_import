# script to average simulation time of specific models

import os
import pandas as pd


tolerance_path = '../bachelor_thesis/LinearSolver'

next_tsv = pd.read_csv(tolerance_path + '/1_08_06.tsv', sep='\t')

# create data frame with new values
columns = next_tsv.columns
new_df = pd.DataFrame(columns=columns, data=[])

# get new names
new_list = []
for iFile in range(0, len(next_tsv['id'])):
    new_id = next_tsv['id'][iFile].split('_{')[0]
    new_list.append(new_id)
next_tsv['id'] = new_list

# get old but still valid data to new data frame
# repeat for round(max(repetition_of_else)/2) --- find out by hand for efficiency, otherwise high number will do as well
for iEffcy in range(0, 10):
    # define iter object
    repetition = 0
    iter_object = iter(range(0, len(next_tsv['id'])))
    for iFile in iter_object:
        new_df = new_df.append({}, ignore_index=True)
        if not iFile == len(next_tsv['id']) - 1:
            if next_tsv['id'][iFile] == next_tsv['id'][iFile + 1] and next_tsv['state_variables'][iFile] == next_tsv['state_variables'][iFile + 1]:
                # find all exceptions by hand and type them in manually --- no clear rule existing
                if next_tsv['id'][iFile] == '{kolodkin2010_figure2b}':
                    new_df.loc[iFile - repetition].id = next_tsv['id'][iFile]
                    new_df.loc[iFile - repetition].t_intern_ms = next_tsv['t_intern_ms'][iFile]
                    new_df.loc[iFile - repetition].t_extern_ms = next_tsv['t_extern_ms'][iFile]
                    new_df.loc[iFile - repetition].state_variables = next_tsv['state_variables'][iFile]
                    new_df.loc[iFile - repetition].parameters = next_tsv['parameters'][iFile]
                    new_df.loc[iFile - repetition].status = next_tsv['status'][iFile]
                    new_df.loc[iFile - repetition].error_message = next_tsv['error_message'][iFile]
                else:
                    new_df.loc[iFile - repetition].id = next_tsv['id'][iFile]
                    new_df.loc[iFile - repetition].t_intern_ms = ''
                    new_df.loc[iFile - repetition].t_extern_ms = ''
                    new_df.loc[iFile - repetition].state_variables = next_tsv['state_variables'][iFile]
                    new_df.loc[iFile - repetition].parameters = ''
                    new_df.loc[iFile - repetition].status = next_tsv['status'][iFile]
                    new_df.loc[iFile - repetition].error_message = next_tsv['error_message'][iFile]

                    # jump over one file
                    for counter in range(0, 1):
                        iFile = next(iter_object)
                        repetition = repetition + 1
            else:
                new_df.loc[iFile - repetition].id = next_tsv['id'][iFile]
                new_df.loc[iFile - repetition].t_intern_ms = next_tsv['t_intern_ms'][iFile]
                new_df.loc[iFile - repetition].t_extern_ms = next_tsv['t_extern_ms'][iFile]
                new_df.loc[iFile - repetition].state_variables = next_tsv['state_variables'][iFile]
                new_df.loc[iFile - repetition].parameters = next_tsv['parameters'][iFile]
                new_df.loc[iFile - repetition].status = next_tsv['status'][iFile]
                new_df.loc[iFile - repetition].error_message = next_tsv['error_message'][iFile]
        else:                                                                                                           # last element of the list --- can't be dublicate any more
            new_df.loc[iFile - repetition].id = next_tsv['id'][iFile]
            new_df.loc[iFile - repetition].t_intern_ms = next_tsv['t_intern_ms'][iFile]
            new_df.loc[iFile - repetition].t_extern_ms = next_tsv['t_extern_ms'][iFile]
            new_df.loc[iFile - repetition].state_variables = next_tsv['state_variables'][iFile]
            new_df.loc[iFile - repetition].parameters = next_tsv['parameters'][iFile]
            new_df.loc[iFile - repetition].status = next_tsv['status'][iFile]
            new_df.loc[iFile - repetition].error_message = next_tsv['error_message'][iFile]


# get new values
list_160_forward = []
list_160_reverse = []
for iFile in range(0, len(next_tsv['id']) - 1):
    if next_tsv['id'][iFile] == next_tsv['id'][iFile + 1] and next_tsv['state_variables'][iFile] == next_tsv['state_variables'][iFile + 1]:
        list_160_forward.append(1)
    else:
        list_160_forward.append(0)
if next_tsv['id'][len(next_tsv['id']) - 1] == next_tsv['id'][len(next_tsv['id']) - 2] and next_tsv['state_variables'][len(next_tsv['id']) - 1] == next_tsv['state_variables'][len(next_tsv['id']) - 2]:
    list_160_forward.append(1)
else:
    list_160_forward.append(0)

if next_tsv['id'][0] == next_tsv['id'][1] and next_tsv['state_variables'][0] == next_tsv['state_variables'][1]:
    list_160_forward.append(1)
else:
    list_160_reverse.append(0)
for iFile in range(1, len(next_tsv['id'])):
    if next_tsv['id'][iFile] == next_tsv['id'][iFile - 1] and next_tsv['state_variables'][iFile] == next_tsv['state_variables'][iFile - 1]:
        list_160_reverse.append(1)
    else:
        list_160_reverse.append(0)

list_160 = []  # add lists together
for i, j in zip(list_160_forward, list_160_reverse):
    if i == j:
        list_160.append(i)
    else:
        list_160.append(i + j)

dublicate = list_160 * next_tsv['t_intern_ms']


output = []
temp = []
for item in dublicate:
    if item != 0:
        temp.append(item)
    if item == 0:
        output.append(temp)
        #if output[0] == []:
         #   del output[0]
        if output[len(output) - 1] == []:
            del output[len(output) - 1]
        temp = []
if temp:
    output.append(temp)

print(output)
print(len(output))