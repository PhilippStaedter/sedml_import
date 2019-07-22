# copy all observables from sedml to sbml + save new sbml with observables

import libsedml
import libsbml
import sys
import os
import importlib
from getObservables import *

iModel = 'bachmann2011'
iFile = 'bachmann'

getAllObservables(iModel, iFile)
