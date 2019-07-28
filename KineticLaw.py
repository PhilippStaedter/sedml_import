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

###### change all Ids in the formula to the unique MetaIds
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

# change Ids again!!! for uniqueness
for iMeta in range(0, len(all_metaid)):
    if len(all_metaid[iMeta].split('_')[1]) == 1:
        all_metaid[iMeta] = all_metaid[iMeta].split('_')[0] + '_A_' + all_metaid[iMeta].split('_')[1]
    elif len(all_metaid[iMeta].split('_')[1]) == 2:
        all_metaid[iMeta] = all_metaid[iMeta].split('_')[0] + '_B_' + all_metaid[iMeta].split('_')[1]
    elif len(all_metaid[iMeta].split('_')[1]) == 3:
        all_metaid[iMeta] = all_metaid[iMeta].split('_')[0] + '_C_' + all_metaid[iMeta].split('_')[1]


# get only the species MetaIds()
all_spec_metaids = []
for iMeta in range(0, num_spec):
    all_spec_metaids.append(sbml_file.getModel().getSpecies(iMeta).getMetaId())

# change species Ids as previously shown
for iSpecMeta in range(0, len(all_spec_metaids)):
    if len(all_spec_metaids[iSpecMeta].split('_')[1]) == 1:
        all_spec_metaids[iSpecMeta] = all_spec_metaids[iSpecMeta].split('_')[0] + '_A_' + all_spec_metaids[iSpecMeta].split('_')[1]
    elif len(all_spec_metaids[iSpecMeta].split('_')[1]) == 2:
        all_spec_metaids[iSpecMeta] = all_spec_metaids[iSpecMeta].split('_')[0] + '_B_' + all_spec_metaids[iSpecMeta].split('_')[1]
    elif len(all_spec_metaids[iSpecMeta].split('_')[1]) == 3:
        all_spec_metaids[iSpecMeta] = all_spec_metaids[iSpecMeta].split('_')[0] + '_C_' + all_spec_metaids[iSpecMeta].split('_')[1]


###### get Kinetic Law
all_formulas_kinetics = [[] for i in range(0,num_reac)]
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
    for iMetaId in range(0, len(all_spec_metaids)):
        spec_list = []
        for iCat in range(0, len(list_of_categories)):
            if not all_spec_metaids[iMetaId] in list_of_categories[iCat]:
                spec_list.append(0)
                print('Categorie: ' + str(0))                                                                           # 0
                print('Species ' + all_spec_metaids[iMetaId] + ' is not in the compartment!')
            else:
                if not '/' in list_of_categories[iCat]:
                    if not 'pow(' in list_of_categories[iCat]:
                        spec_list.append(1)
                        print('Categorie: ' + str(1))                                                                   # 1
                        print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                    else:
                        _, b = list_of_categories[iCat].split(', ')
                        exp, _ = b.split(')', 1)
                        if exp == str(2):
                            spec_list.append(2)
                            print('Categorie: ' + str(2))                                                               # 2
                            print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                        else:
                            try:
                                int(exp)
                                spec_list.append(3)
                                print('Categorie: ' + str(3))                                                           # 3
                                print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                            except:
                                spec_list.append(4)
                                print('Categorie: ' + str(4))                                                           # 4
                                print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                else:
                    if '(' in list_of_categories[iCat]:
                        if list_of_categories[iCat][0] == '(':
                            matching_index = getIndex(list_of_categories[iCat], 0)
                            slash_index = matching_index + 2
                            nominator = list_of_categories[iCat][0 : matching_index + 1]
                            denominator = list_of_categories[iCat][slash_index + 2 : len(list_of_categories[iCat])]
                            if all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] not in denominator:
                                if not 'pow(' in nominator:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))  # 1
                                    print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                else:
                                    close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                    if not all_spec_metaids[iMetaId] in nominator[nominator.find('pow(') + 4 : close_power_index + 1]:
                                        spec_list.append(1)
                                        print('Categorie: ' + str(1))  # 1
                                        print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                    else:
                                        _, b = nominator.split(', ')
                                        exp, _ = b.split(')', 1)
                                        if exp == str(2):
                                            spec_list.append(2)
                                            print('Categorie: ' + str(2))  # 2
                                            print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(3)
                                                print('Categorie: ' + str(3))  # 3
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                            except:
                                                spec_list.append(4)
                                                print('Categorie: ' + str(4))  # 4
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                            elif all_spec_metaids[iMetaId] not in nominator and all_spec_metaids[iMetaId] in denominator:
                                if not 'pow(' in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))                                                       # 5
                                    print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                else:
                                    close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                    if not all_spec_metaids[iMetaId] in nominator[nominator.find('pow(') + 4: close_power_index + 1]:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                    else:
                                        _, b = denominator.split(', ')
                                        exp, _ = b.split(')', 1)
                                        if exp == str(2):
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))                                                   # 6
                                            print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))                                               # 7
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))                                               # 8
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                            elif all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] in denominator:
                                print('What to do with species ' + all_spec_metaids[iMetaId] + ' ?')
                        else:
                            slash_index = list_of_categories[iCat].find('/')
                            nominator = list_of_categories[iCat][0: slash_index - 1]
                            denominator = list_of_categories[iCat][slash_index + 2: len(list_of_categories[iCat])]
                            if all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] not in denominator:
                                if not 'pow(' in nominator:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))  # 1
                                    print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                else:
                                    _, b = nominator.split(', ')    #all_spec_metaids[iMetaId] +
                                    exp, _ = b.split(')', 1)
                                    if exp == str(2):
                                        spec_list.append(2)
                                        print('Categorie: ' + str(2))  # 2
                                        print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(3)
                                            print('Categorie: ' + str(3))  # 3
                                            print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                        except:
                                            spec_list.append(4)
                                            print('Categorie: ' + str(4))  # 4
                                            print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                            elif all_spec_metaids[iMetaId] not in nominator and all_spec_metaids[iMetaId] in denominator:
                                if not 'pow(' + all_spec_metaids[iMetaId] in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))                                                       # 5
                                    print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                else:
                                    close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                    if not all_spec_metaids[iMetaId] in nominator[nominator.find('pow(') + 4: close_power_index + 1]:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                                    else:
                                        _, b = denominator.split(', ')
                                        exp, _ = b.split(')', 1)
                                        if exp == str(2):
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))                                                   # 6
                                            print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))                                               # 7
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))                                               # 8
                                                print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                            elif all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] in denominator:
                                print('What to do with species ' + all_spec_metaids[iMetaId] + ' ?')
                    else:
                        slash_index = list_of_categories[iCat].find('/')
                        nominator = list_of_categories[iCat][0 : slash_index - 1]
                        denominator = list_of_categories[iCat][slash_index + 2 : len(list_of_categories[iCat])]
                        if all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] not in denominator:
                            if not 'pow(' in nominator:
                                spec_list.append(1)
                                print('Categorie: ' + str(1))  # 1
                                print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                            else:
                                _, b = nominator.split(', ')
                                exp, _ = b.split(')', 1)
                                if exp == str(2):
                                    spec_list.append(2)
                                    print('Categorie: ' + str(2))  # 2
                                    print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(3)
                                        print('Categorie: ' + str(3))  # 3
                                        print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                    except:
                                        spec_list.append(4)
                                        print('Categorie: ' + str(4))  # 4
                                        print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                        elif all_spec_metaids[iMetaId] not in nominator and all_spec_metaids[iMetaId] in denominator:
                            if not 'pow(' in denominator:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 5
                                print('Variable ' + all_spec_metaids[iMetaId] + ' is linear!')
                            else:
                                _, b = denominator.split(', ')
                                exp, _ = b.split(')', 1)
                                if exp == str(2):
                                    spec_list.append(6)
                                    print('Categorie: ' + str(6))  # 6
                                    print('Species ' + all_spec_metaids[iMetaId] + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(7)
                                        print('Categorie: ' + str(7))  # 7
                                        print('Species ' + all_spec_metaids[iMetaId] + ' has a natural exponent!')
                                    except:
                                        spec_list.append(8)
                                        print('Categorie: ' + str(8))  # 8
                                        print('Species ' + all_spec_metaids[iMetaId] + ' has a rational exponent!')
                        elif all_spec_metaids[iMetaId] in nominator and all_spec_metaids[iMetaId] in denominator:
                            print('What to do with species ' + all_spec_metaids[iMetaId] + ' ?')

        kinetic_list.append(spec_list)

    # check what kinetics are available by concatenating all elements of 'kinetic_list'
    conc_kinetic_list = []
    for iList in range(0, len(kinetic_list)):
        conc_kinetic_list = conc_kinetic_list + kinetic_list[iList]

    for item in [0,1,2,3,4,5,6,7,8,9]:
        if item in conc_kinetic_list:
            all_formulas_kinetics[iReact].append(1)
        else:
            all_formulas_kinetics[iReact].append(0)


# give total kinetic number from 0 - 9
total_kinetics = [sum(x) for x in zip(*all_formulas_kinetics)]
for iKinetic in range(0, len(total_kinetics)):
    if total_kinetics[iKinetic] > 0:
        total_kinetics[iKinetic] = 1
    else:
        total_kinetics[iKinetic] = 0

only_for_debugging = 'just_debugging'

#return total_kinetics