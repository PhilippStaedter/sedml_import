# copy all observables from sedml to sbml + save new sbml with observables

import libsedml
import libsbml
import sys
import os
import importlib
from getObservables import *


# important paths
sedml_path = './sedml_models'

# iModel = 'bachmann2011'
# iFile = 'bachmann'

sedml_models = sorted(os.listdir(sedml_path))
for iModel in sedml_models:

#for iModel in ['perelson1996_fig1b_top']: #['adlung2017_fig2bto2e']:

    if os.path.exists(sedml_path + '/' + iModel + '/experimental_data_rearranged'):

        sbml_models = sorted(os.listdir(sedml_path + '/' + iModel + '/sbml_models'))
        for iFile in sbml_models:
            iFile,_ = iFile.split('.')

            # call function from 'getObservables.py'
            getAllObservables(iModel, iFile)
