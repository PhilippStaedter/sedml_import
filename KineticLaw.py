# script to determine what kinetic law a formel has

import libsbml
import pandas as pd


iModel = 'bachmann2011'
iFile = 'bachmann'


#def getKineticLaw(iModel, iFile):

# important path
sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'

# open SBML file
sbml_file = libsbml.readSBML(sbml_path)

# get number of tasks, observables and variables
num_spec = sbml_file.getModel().getNumSpecies()
num_reac = sbml_file.getModel().getNumReactions()

# get all species
all_spec = []
for iSpec in range(0, num_spec):
    all_spec.append(sbml_file)

###### get kinetic law
for iReact in range(0, num_reac):

    # get MathMl formula as string
    formula = libsbml.formulaToString(sbml_file.getModel().getReactions(iReact).getKineticLaw().getMath())

    # assign number of 0 - 8  ///   assign True(1) or False(0)
    kinetic_list = []
    for iSpec in range(0, len(all_spec)):
        if not all_spec[iSpec] in formula:
            kinetic_list.append(0)
            print('Categorie: ' + str(0))
            print('Variable ' + all_spec[iSpec] + ' is not in the formula!')
        else:
            if '/' in formula:                                                                          # for how many denominators should be looked for?
                index1 = formula.find('/')
                if formula.find(all_spec[iSpec], index1 + 1, len(formula)) != -1:
                    print('We have a variable in a denominator! => We have a Kinetic!')
                    if formula.find('/', index1 + 1, len(formula)) != -1:
                        index2 = formula.find('/', index1 + 1, len(formula))
                        if formula.find(all_spec[iSpec], index2 + 1, len(formula)) != -1:
                            kinetic_list.append('5/6/7')
                        else:
                            print('Variable could be in a nominator!')
                            kinetic_list.append('5/6/7')
                    else:
                        print('Variable could be in a nominator!')
                        kinetic_list.append('5/6/7')
                else:
                    print('No variable in denominator!')
                    kinetic_list.append('1/2/3/4')
            else:
                print('No denominator!')
                kinetic_list.append('1/2/3/4')

# give total kinetic number from 1 - 7
kin = sorted(kinetic_list, reverse=True)[0]
