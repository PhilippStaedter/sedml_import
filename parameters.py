# Add Parameter / State / Reaction values
import os
import libsbml
import pandas as pd


# important paths
models_path = '../sbml2amici/amici_models'
models_base_path = '../sbml2amici'
base_path = './sedml_models'
tsv_file_path = '../sbml2amici/table.tsv'

# list of all directories + SBML files
list_directory = os.listdir(base_path)
list_directory = sorted(list_directory)

# read in table + new column in correct order
tsv_file = pd.read_csv(tsv_file_path, sep='\t')
tsv_file['parameters'] = pd.Series()
# tsv_file['states'] = pd.Series()
# tsv_file['reactions'] = pd.Series()
columnTitels = ['id', 'states', 'reactions', 'parameters', 'error_message']
tsv_file = tsv_file.reindex(columns=columnTitels)


for models in list_directory:
    list_files = os.listdir(base_path + '/' + models + '/sbml_models')
    list_files = sorted(list_files)
    for files in list_files:
        sbml_file = base_path + '/' + models + '/sbml_models/' + files
        model_name, other_stuff = files.split(".", 1)
        model_output_dir = models_path + '/' + models + '/' + model_name

        try:
            # define id
            id = '{' + models + '}' + '_' + '{' + files + '}'

            # read accompanying sbml file
            file = libsbml.readSBML(sbml_file)
            all_properties = file.getModel()
            num_parameters = len(all_properties.getListOfParameters())
            # num_states = len(all_properties.getListOfSpecies())
            # num_reactions = len(all_properties.getListOfReactions())


            # set counter
            counter = 0

            # assign value to matching row
            while id != tsv_file['id'][counter]:
                counter = counter + 1
            else:
                tsv_file.loc[counter, 'parameters'] = num_parameters
                # tsv_file.loc[counter, 'states'] = num_states
                # tsv_file.loc[counter, 'reactions'] = num_reactions

        except:
            # error message
            print('Parameter value could not be saved!')
            # print('State value could not be saved!')
            # print('Reaction value could not be saved!')

# save tsv_file
tsv_file.to_csv(path_or_buf=models_base_path + '/table_with_parameters.tsv', sep='\t', index=False)
