# script to determine what kinetic law a formel has

import libsbml
from decomposeFormula import *
from opposingBracket import *


iModel = 'bachmann2011'
iFile = 'bachmann'


#def getKineticLaw(iModel, iFile):

# important path
sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.sbml'

# open SBML file
sbml_file = libsbml.readSBML(sbml_path)

# get number of tasks, observables and variables
num_comp = sbml_file.getModel().getNumCompartments()
num_spec = sbml_file.getModel().getNumSpecies()
num_par = sbml_file.getModel().getNumParameters()
num_reac = sbml_file.getModel().getNumReactions()

# get all compartments
all_comp = []
for iComp in range(0, num_comp):
    all_comp.append(sbml_file.getModel().getCompartment(iComp).getId())

# get all species
all_spec = []
for iSpec in range(0, num_spec):
    all_spec.append(sbml_file.getModel().getSpecies(iSpec).getId())

# get all parameters
all_par = []
for iPar in range(0, num_par):
    all_par.append(sbml_file.getModel().getParameter(iPar).getId())

# sort all compartments, species and parameters after their length
all_sorted = sorted(all_comp + all_spec + all_par, key=len, reverse=True)

# get all MetaIds
all_metaid = []
for iSorted in range(0, len(all_sorted)):
    if all_sorted[iSorted] in all_spec:
        for iSpec in range(0, num_spec):
            if all_spec[iSpec] == all_sorted[iSorted]:
                all_metaid.append(sbml_file.getModel().getSpecies(iSpec).getMetaId())
    elif all_sorted[iSorted] in all_par:
        for iPar in range(0, num_par):
            if all_par[iPar] == all_sorted[iSorted]:
                all_metaid.append(sbml_file.getModel().getParameter(iPar).getMetaId())
    elif all_sorted[iSorted] in all_comp:
        for iComp in range(0, num_comp):
            if all_comp[iComp] == all_sorted[iSorted]:
                all_metaid.append(sbml_file.getModel().getCompartment(iComp).getMetaId())

###### get kinetic law
for iReact in range(0, num_reac):

    # get MathMl formula as string
    formula = libsbml.formulaToString(sbml_file.getModel().getReaction(iReact).getKineticLaw().getMath())

    # replace all species and parameters by their unique metaid-id
    for iSorted in range(0, len(all_sorted)):
        if all_sorted[iSorted] in formula:
            formula = formula.replace(all_sorted[iSorted], all_metaid[iSorted])

    # decompose math formula into categories
    list_of_categories = decomposition(formula)

    # assign number of 0 - 8 ///   assign True(1) or False(0)
    kinetic_list = []
    for iSpec in range(0, len(all_spec)):
        spec_list = []
        for iCat in range(0, len(list_of_categories)):
            if not all_spec[iSpec] in list_of_categories[iCat]:
                spec_list.append(0)
                print('Categorie: ' + str(0))                                                                           # 0
                print('Species ' + all_spec[iSpec] + ' is not in the compartment!')
            else:
                if not '/' in list_of_categories[iCat]:
                    if not 'pow(' in list_of_categories[iCat]:
                        spec_list.append(1)
                        print('Categorie: ' + str(1))                                                                   # 1
                        print('Variable ' + all_spec[iSpec] + ' is linear!')
                    else:
                        _, b = list_of_categories[iCat].split(all_spec[iSpec] + ', ')
                        exp, _ = b.split(')', 1)
                        if exp == 2:
                            spec_list.append(2)
                            print('Categorie: ' + str(2))                                                               # 2
                            print('Species ' + all_spec[iSpec] + ' is quadratic!')
                        else:
                            try:
                                int(exp)
                                spec_list.append(3)
                                print('Categorie: ' + str(3))                                                           # 3
                                print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                            except:
                                spec_list.append(4)
                                print('Categorie: ' + str(4))                                                           # 4
                                print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                else:
                    if '(' in list_of_categories[iCat]:
                        if list_of_categories[iCat][0] == '(':
                            matching_index = getIndex(list_of_categories[iCat], 0)
                            slash_index = matching_index + 2
                            nominator = list_of_categories[iCat][0 : matching_index + 1]
                            denominator = list_of_categories[iCat][slash_index + 2 : len(list_of_categories[iCat])]
                            if all_spec[iSpec] in nominator and all_spec[iSpec] not in denominator:
                                if not 'pow(' in nominator:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))  # 1
                                    print('Variable ' + all_spec[iSpec] + ' is linear!')
                                else:
                                    _, b = nominator.split(all_spec[iSpec] + ', ')
                                    exp, _ = b.split(')', 1)
                                    if exp == 2:
                                        spec_list.append(2)
                                        print('Categorie: ' + str(2))  # 2
                                        print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(3)
                                            print('Categorie: ' + str(3))  # 3
                                            print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(4)
                                            print('Categorie: ' + str(4))  # 4
                                            print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                            elif all_spec[iSpec] not in nominator and all_spec[iSpec] in denominator:
                                if not 'pow(' in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))                                                       # 5
                                    print('Variable ' + all_spec[iSpec] + ' is linear!')
                                else:
                                    _, b = denominator.split(all_spec[iSpec] + ', ')
                                    exp, _ = b.split(')', 1)
                                    if exp == 2:
                                        spec_list.append(6)
                                        print('Categorie: ' + str(6))                                                   # 6
                                        print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(7)
                                            print('Categorie: ' + str(7))                                               # 7
                                            print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(8)
                                            print('Categorie: ' + str(8))                                               # 8
                                            print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                            elif all_spec[iSpec] in nominator and all_spec[iSpec] in denominator:
                                print('What to do with species ' + all_spec[iSpec] + ' ?')
                        else:
                            slash_index = list_of_categories[iCat].find('/')
                            nominator = list_of_categories[iCat][0: slash_index - 1]
                            denominator = list_of_categories[iCat][slash_index + 2: len(list_of_categories[iCat])]
                            if all_spec[iSpec] in nominator and all_spec[iSpec] not in denominator:
                                if not 'pow(' in nominator:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))  # 1
                                    print('Variable ' + all_spec[iSpec] + ' is linear!')
                                else:
                                    _, b = nominator.split(all_spec[iSpec] + ', ')
                                    exp, _ = b.split(')', 1)
                                    if exp == 2:
                                        spec_list.append(2)
                                        print('Categorie: ' + str(2))  # 2
                                        print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(3)
                                            print('Categorie: ' + str(3))  # 3
                                            print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(4)
                                            print('Categorie: ' + str(4))  # 4
                                            print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                            elif all_spec[iSpec] not in nominator and all_spec[iSpec] in denominator:
                                if not 'pow(' in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))                                                       # 5
                                    print('Variable ' + all_spec[iSpec] + ' is linear!')
                                else:
                                    _, b = denominator.split(all_spec[iSpec] + ', ')
                                    exp, _ = b.split(')', 1)
                                    if exp == 2:
                                        spec_list.append(6)
                                        print('Categorie: ' + str(6))                                                   # 6
                                        print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(7)
                                            print('Categorie: ' + str(7))                                               # 7
                                            print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(8)
                                            print('Categorie: ' + str(8))                                               # 8
                                            print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                            elif all_spec[iSpec] in nominator and all_spec[iSpec] in denominator:
                                print('What to do with species ' + all_spec[iSpec] + ' ?')
                    else:
                        slash_index = list_of_categories[iCat].find('/')
                        nominator = list_of_categories[iCat][0 : slash_index - 1]
                        denominator = list_of_categories[iCat][slash_index + 2 : len(list_of_categories[iCat])]
                        if all_spec[iSpec] in nominator and all_spec[iSpec] not in denominator:
                            if not 'pow(' in nominator:
                                spec_list.append(1)
                                print('Categorie: ' + str(1))  # 1
                                print('Variable ' + all_spec[iSpec] + ' is linear!')
                            else:
                                _, b = nominator.split(all_spec[iSpec] + ', ')
                                exp, _ = b.split(')', 1)
                                if exp == 2:
                                    spec_list.append(2)
                                    print('Categorie: ' + str(2))  # 2
                                    print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(3)
                                        print('Categorie: ' + str(3))  # 3
                                        print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                    except:
                                        spec_list.append(4)
                                        print('Categorie: ' + str(4))  # 4
                                        print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                        elif all_spec[iSpec] not in nominator and all_spec[iSpec] in denominator:
                            if not 'pow(' in denominator:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 5
                                print('Variable ' + all_spec[iSpec] + ' is linear!')
                            else:
                                _, b = denominator.split(all_spec[iSpec] + ', ')
                                exp, _ = b.split(')', 1)
                                if exp == 2:
                                    spec_list.append(6)
                                    print('Categorie: ' + str(6))  # 6
                                    print('Species ' + all_spec[iSpec] + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(7)
                                        print('Categorie: ' + str(7))  # 7
                                        print('Species ' + all_spec[iSpec] + ' has a natural exponent!')
                                    except:
                                        spec_list.append(8)
                                        print('Categorie: ' + str(8))  # 8
                                        print('Species ' + all_spec[iSpec] + ' has a rational exponent!')
                        elif all_spec[iSpec] in nominator and all_spec[iSpec] in denominator:
                            print('What to do with species ' + all_spec[iSpec] + ' ?')

        kinetic_list.append(spec_list)


# give total kinetic number from 0 - 8
kin = sorted(kinetic_list, reverse=True)[0]


# if formula.find(all_spec[iSpec], index + 1, len(formula)) != -1

'''
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
'''
