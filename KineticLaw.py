# script to determine what kinetic law a formel has

import libsbml
import pandas as pd
from opposingBracket import *


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
    all_spec.append(sbml_file.getModel().getSpecies(iSpec).getId())

###### get kinetic law
for iReact in range(0, num_reac):

    # get MathMl formula as string
    formula = libsbml.formulaToString(sbml_file.getModel().getReaction(iReact).getKineticLaw().getMath())

    # assign number of 0 - 9 ///   assign True(1) or False(0)
    kinetic_list = []
    for iSpec in range(0, len(all_spec)):
        if not all_spec[iSpec] in formula:
            kinetic_list.append(0)
            print('Categorie: ' + str(0))                                                                               # 0
            print('Species ' + all_spec[iSpec] + ' is not in the formula!')
        else:
            spec_list = []
            if '(' in formula:
                num_bracket = formula.count('(')
                index_bracket = formula.find('(')
                matching_bracket_index = getIndex(formula, index_bracket)
                if '/' in formula:
                    num_slash = formula.count('/')
                    if formula[index_bracket - 2] == '/':
                    for iSlash in range(0, num_slash):
                        if iSlash == 0:
                            index_slash = formula.find('/')
                            if all_spec[iSpec] in formula[0:index_slash]:
                                if 'pow' in formula[0:index_slash]:
                                    _,b = formula[0:index_slash].split(all_spec[iSpec] + ', ')
                                    exp,_ = b.split(')',1)
                                    if exp == 2:
                                        spec_list.append(2)
                                        print('Categorie: ' + str(2))                                                       # 2
                                        print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(3)
                                            print('Categorie: ' + str(3))                                                   # 3
                                            print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(4)
                                            print('Categorie: ' + str(4))                                                   # 4
                                            print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                                else:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))                                                           # 1
                                    print('Variable ' + all_spec[iSpec] + ' is linear!')
                        elif iSlash != 0:
                            index_1 = formula.find('/')
                            index_2 = formula.find('/', formula.find('/') + 1)
                            subformula = formula[index_1 + 2 : index_2 - 1]
                            if subformula[0] == '(':
                                matching_bracket_index = getIndex(subformula,0)
                                if all_spec[iSpec] in subformula[0:matching_bracket_index + 1]:
                                    if 'pow' in subformula[0:matching_bracket_index + 1]:
                                        _, b = subformula[0:matching_bracket_index + 1].split(all_spec[iSpec] + ', ')
                                        exp, _ = b.split(')', 1)
                                        if exp == 2:
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))                                                   # 6
                                            print('Species ' + all_spec[iSpec] + ' has a quadratic Hill Kinetic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))                                               # 7
                                                print('Species ' + all_spec[iSpec] + ' has a polynomial Hill Kinetic!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))                                               # 8
                                                print('Species ' + all_spec[iSpec] + ' has a rational Hill Kinetic!')
                                    else:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))                                                       # 5
                                        print('Species ' + all_spec[iSpec] + ' has a Michaelis-Menten Kinetic!')
                kinetic_list.append(spec_list)

# give total kinetic number from 1 - 7
kin = sorted(kinetic_list, reverse=True)[0]


# if formula.find(all_spec[iSpec], index + 1, len(formula)) != -1