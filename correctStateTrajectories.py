# check for correctness of state trajectories

import os
import pandas as pd

# important paths
json_path = './json_files'
sedml_path = './sedml_models'

# set counter
counter_true = 0
counter_model = 0

# open all .csv files
list_directory_sedml = sorted(os.listdir(json_path))

for iModel in list_directory_sedml:

    list_directory_sbml = sorted(os.listdir(sedml_path + '/' + iModel + '/sbml_models'))

    for iFile in list_directory_sbml:

         iFile_name, rest = iFile.split('.',1)

         # check if file exists
         if os.path.exists(json_path + '/' + iModel + '/' + iFile_name):
            csv_file = pd.read_csv(json_path + '/' + iModel + '/' + iFile_name + '/whole_error.csv', sep='\t')
            counter_model = counter_model + 1

            # check for True
            if csv_file['trajectories_match'][0] == True:
                counter_true = counter_true + 1
            else:
                counter_true = counter_true
         else:
            print(iModel + '_' + iFile_name + ' does not exist!')
            counter_true = counter_true
            counter_model = counter_model + 1

print(counter_true)
print(counter_model)
counter_difference = counter_model - counter_true
print('Difference: ' + str(counter_difference))