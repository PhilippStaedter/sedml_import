# script to get the .csv file of experimental data

import os
import libsedml
import urllib.request

iModel = 'bachmann2011'

# list all models
list_directory_sedml = sorted(os.listdir('./sedml_models'))

# for iModel in list_directory_sedml:

# def experimentalData():

# important paths
base_path = './sedml_models/' + iModel
sedml_path = './sedml_models/' + iModel + '/' + iModel + '.sedml'

# create new folder to save experimental data file
if not os.path.exists(base_path + '/experimental_data'):
    os.makedirs(base_path + '/experimental_data')

# load sedml
sedml_file = libsedml.readSedML(sedml_path)

# get all experimental data files
for iData in range(0, sedml_file.getNumDataDescriptions()):
    try:
        # parse source url from data description
        data = sedml_file.getDataDescription(iData)
        data_id = data.getId()
        data_source = data.getSource()

        # download file
        urllib.request.urlretrieve(data_source, base_path + '/experimental_data/' + data_id + '.xls')

    except:
        print('Model ' + iModel + ' has no file for experimental data!')