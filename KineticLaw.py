# script to determine what kinetic law a formal has

import libsbml
from decomposeFormula import *
from opposingBracket import *
from Depth1 import *
from Depth1_KinLaw import *
import os
from Substitution import *
import sympy as sym

#iModel = 'Froehlich2018'
#iFile = 'Froehlich2018'


def getKineticLaw(iModel, iFile):

    # error_file
    error_file = pd.DataFrame(columns=['model', 'error'], data=[])

    # split for extension
    iFile,ext = iFile.split('.')

    # important path
    if os.path.exists('./sedml_models/' + iModel):
        sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.' + ext  #'.xml'  #'.sbml'
    else:
        benchmark_collectin_path = '../benchmark-models/hackathon_contributions_new_data_format'
        sbml_path = benchmark_collectin_path + '/' + iModel + '/' + iFile + '.' + ext

    # open SBML file
    sbml_file = libsbml.readSBML(sbml_path)
    num_FuncDef = sbml_file.getModel().getNumFunctionDefinitions()

    ###### check for local functions defined exclusivly in sbml file and put them in the formula ######
    if num_FuncDef > 0:
        convertConfig = libsbml.SBMLFunctionDefinitionConverter().getDefaultProperties()
        sbml_file.convert(convertConfig)

    ###### change all Ids in the formula to the unique MetaIds
    # get number of tasks, observables and variables
    num_comp = sbml_file.getModel().getNumCompartments()
    num_spec = sbml_file.getModel().getNumSpecies()
    num_par = sbml_file.getModel().getNumParameters()
    num_reac = sbml_file.getModel().getNumReactions()


    # get all species
    all_spec = []
    for iSpec in range(0, num_spec):
        spec_id = sbml_file.getModel().getSpecies(iSpec).getId()
        all_spec.append(' ' + spec_id + ' ')


    ###### get Kinetic Law
    all_formulas_kinetics = [[] for i in range(0,num_reac)]
    for iReact in range(0, num_reac):

        #iReact = 40

        # get MathMl formula as string
        formula = libsbml.formulaToString(sbml_file.getModel().getReaction(iReact).getKineticLaw().getMath())

        # replace 'pow(X,k)' by 'X**k' or 'X^k'
        formula = replacePower(formula)

        # bring formula in better shape using sympy
        error_file = error_file.append({}, ignore_index=True)
        try:
            #formula = sym.simplify(formula)
            error_file['model'][iReact] = '{' + iModel + '}_{' + iFile + '}_' + str(iReact)
            error_file['error'][iReact] = 'Ok'
            formula = sym.expand(formula)
            formula = str(formula)
            formula = formula.replace('*', ' * ')
            formula = formula.replace('/', ' / ')
        except Exception as e:
            error_info = str(e)
            error_file['model'][iReact] = '{' + iModel + '}_{' + iFile + '}_' + str(iReact)
            error_file['error'][iReact] = error_info
            all_formulas_kinetics[iReact] = [0,0,0,0,0,0,0,0,0,0,True]
            continue

        # add more white spaces
        formula = formula.replace('(', '( ')
        formula = formula.replace(')', ' )')
        formula = formula.replace(',', ' ,')
        formula = formula.rjust(len(formula) + 1)
        formula = formula.ljust(len(formula) + 1)
        if ' *  * ' in formula:
            formula = formula.replace(' *  * ', '**')

        # re-replace 'X**k' by 'pow(X,k)'
        formula = replaceDoubleStar(formula)

        # decompose math formula into categories
        list_of_categories = decomposition(formula)

        # replace all brackets and commas by themselfes and spaces before and after + add spaces in front of and behind the category
        for iCat in range(0, len(list_of_categories)):
            list_of_categories[iCat] = list_of_categories[iCat].replace('(', '( ')
            list_of_categories[iCat] = list_of_categories[iCat].replace(')', ' )')
            list_of_categories[iCat] = list_of_categories[iCat].replace(',', ' ,')
            list_of_categories[iCat] = list_of_categories[iCat].rjust(len(list_of_categories[iCat]) + 1)
            list_of_categories[iCat] = list_of_categories[iCat].ljust(len(list_of_categories[iCat]) + 1)

        # assign number of 0 - 8 ///   assign True(1) or False(0)
        kinetic_list = []
        if not any(species in formula for species in all_spec) == True:
            kinetic_list.append(0)
        else:
            for iSpecId in range(0, len(all_spec)):
                spec_list = []
                for iCat in range(0, len(list_of_categories)):
                    if not all_spec[iSpecId] in list_of_categories[iCat]:
                        'Do nothing'
                    else:
                        if not '/' in list_of_categories[iCat]:
                            if not 'pow(' in list_of_categories[iCat]:
                                spec_list.append(1)
                                print('Categorie: ' + str(1))                                                               # 1
                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                            else:
                                num_comma = list_of_categories[iCat].count(', ')
                                if num_comma == 1:
                                    _, b = list_of_categories[iCat].split(', ')
                                    exp, _ = b.split(')', 1)
                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                else:
                                    kinlaw = []
                                    for iComma in range(0, num_comma):
                                        list_of_splits = list_of_categories[iCat].split(', ', iComma + 1)
                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                spec_list.append(kinlaw)
                                '''
                                if exp == str(2) + ' ':
                                    spec_list.append(2)
                                    print('Categorie: ' + str(2))                                                           # 2
                                    print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(3)
                                        print('Categorie: ' + str(3))                                                       # 3
                                        print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                    except:
                                        spec_list.append(4)
                                        print('Categorie: ' + str(4))                                                       # 4
                                        print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                '''
                        else:
                            if '(' in list_of_categories[iCat]:
                                if list_of_categories[iCat][1] == '(':                                                              # [1], because 0 is a white space!
                                    matching_index = getIndex(list_of_categories[iCat], 1)
                                    slash_index = matching_index + 2
                                    nominator = list_of_categories[iCat][1 : matching_index + 1]
                                    denominator = list_of_categories[iCat][slash_index + 1 : len(list_of_categories[iCat])]
                                    if all_spec[iSpecId] in nominator and all_spec[iSpecId] not in denominator:

                                        ##### possibility: more '/' in nominator  => e.g. (A + B/C) / D   =>   KinLaw(C ) == 5 (!= 1)
                                        # repeat whole categories again + pow(A + B/C) also possible!
                                        # get rid of starting brackets
                                        if '/' in nominator:
                                            nominator = nominator[1 : len(nominator) - 1]
                                            list_of_categories2 = decomposition(nominator)
                                            kinlaw = depth1(nominator, list_of_categories2, all_spec[iSpecId], sbml_file, iReact)
                                            spec_list.append(kinlaw)
                                            print('Species ' + all_spec[iSpec] + ' had to go in depth!')

                                        ######
                                        #elif '/' in denominator

                                        else:
                                            if not 'pow(' in nominator:
                                                spec_list.append(1)
                                                print('Categorie: ' + str(1))  # 1
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                close_power_index = getIndex(nominator, nominator.find('pow(') + 3)
                                                if not all_spec[iSpecId] in nominator[nominator.find('pow(') + 3 : close_power_index + 1]:
                                                    spec_list.append(1)
                                                    print('Categorie: ' + str(1))  # 1
                                                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                                else:
                                                    num_comma = nominator.count(', ')
                                                    if num_comma == 1:
                                                        _, b = nominator.split(', ')
                                                        exp, _ = b.split(')', 1)
                                                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                    else:
                                                        kinlaw = []
                                                        for iComma in range(0, num_comma):
                                                            list_of_splits = nominator.split(', ', iComma + 1)
                                                            if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                                kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                                        kinlaw = sorted(kinlaw, reverse=True)[0]
                                                    spec_list.append(kinlaw)

                                                    '''
                                                    if exp == str(2) + ' ':
                                                        spec_list.append(2)
                                                        print('Categorie: ' + str(2))  # 2
                                                        print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                    else:
                                                        try:
                                                            int(exp)
                                                            spec_list.append(3)
                                                            print('Categorie: ' + str(3))  # 3
                                                            print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                        except:
                                                            spec_list.append(4)
                                                            print('Categorie: ' + str(4))  # 4
                                                            print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                    '''
                                    elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                        if not 'pow(' in denominator:
                                            spec_list.append(5)
                                            print('Categorie: ' + str(5))                                                   # 5
                                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                        else:
                                            close_power_index = getIndex(denominator, denominator.find('pow(') + 3)
                                            if not all_spec[iSpecId] in denominator[denominator.find('pow(') + 3: close_power_index + 1]:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                num_comma = denominator.count(', ')
                                                if num_comma == 1:
                                                    _, b = denominator.split(', ')
                                                    exp, _ = b.split(')', 1)
                                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                else:
                                                    kinlaw = []
                                                    for iComma in range(0, num_comma):
                                                        list_of_splits = denominator.split(', ', iComma + 1)
                                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')',1)
                                                            kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                                spec_list.append(kinlaw)
                                                '''
                                                if exp == str(2) + ' ':
                                                    spec_list.append(6)
                                                    print('Categorie: ' + str(6))                                           # 6
                                                    print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                else:
                                                    try:
                                                        int(exp)
                                                        spec_list.append(7)
                                                        print('Categorie: ' + str(7))                                       # 7
                                                        print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                    except:
                                                        spec_list.append(8)
                                                        print('Categorie: ' + str(8))                                       # 8
                                                        print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                '''
                                    elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                        new_formula = nominator + '* 1 /' + denominator
                                        list_of_categories10 = decomposition(new_formula)
                                        kinlaw_1 = depth1(new_formula, list_of_categories10, all_spec[iSpecId], sbml_file, iReact)
                                        spec_list.append(kinlaw_1)
                                        print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                        #spec_list.append(9)                                                                 # 9
                                        #print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')


                                elif list_of_categories[iCat][1:5] == 'pow(' and '/' in list_of_categories[iCat][5: getIndex(list_of_categories[iCat], 4)]:
                                    matching_index = getIndex(list_of_categories[iCat], 4)
                                    if matching_index + 2 < len(list_of_categories[iCat]) and list_of_categories[iCat][matching_index + 2] == '/':
                                        nominator = list_of_categories[iCat][0: matching_index + 2]
                                        denominator = list_of_categories[iCat][matching_index + 3: len(list_of_categories[iCat])]
                                        if all_spec[iSpecId] in nominator and all_spec[iSpecId] not in denominator:
                                            if not 'pow(' in nominator:
                                                spec_list.append(1)
                                                print('Categorie: ' + str(1))  # 1
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                ##### possibility: more '/' in pow() in nominator  => e.g. pow((A + B)/C, 2) / D   =>   KinLaw(C) == 6 (!= 1)
                                                #                                                  => e.g. pow(A + B/C, 2) / D     =>   KinLaw(C) == 6 (!= 5, != 1)
                                                # repeat whole categories again + pow(A + B/C) also possible!
                                                # get rid of power and brackets
                                                if '/' in nominator:
                                                    num_comma = nominator.count(', ')
                                                    if num_comma == 1:
                                                        _, b = nominator.split(', ')
                                                        exp, _ = b.split(')', 1)
                                                        nominator = nominator[5: len(nominator) - 4]
                                                        list_of_categories4 = decomposition(nominator)
                                                        kinlaw_1 = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                        kinlaw = depthKineticLaw(kinlaw_1, exp, sbml_file, iReact)
                                                    else:
                                                        kinlaw = []
                                                        for iComma in range(0, num_comma):
                                                            list_of_splits = nominator.split(', ', iComma + 1)
                                                            if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                                nominator = nominator[5: len(nominator) - 4]
                                                                list_of_categories4 = decomposition(nominator)
                                                                kinlaw_1 = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                                kinlaw.append(depthKineticLaw(kinlaw_1, exp, sbml_file, iReact))
                                                            kinlaw = sorted(kinlaw, reverse=True)[0]
                                                    spec_list.append(kinlaw)
                                                    print('Species ' + all_spec[iSpecId] + ' had to go in depth!')
                                                else:
                                                    num_comma = nominator.count(', ')
                                                    if num_comma == 1:
                                                        _, b = nominator.split(', ')
                                                        exp, _ = b.split(')', 1)
                                                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                    else:
                                                        kinlaw = []
                                                        for iComma in range(0, num_comma):
                                                            list_of_splits = nominator.split(', ', iComma + 1)
                                                            if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                                kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                                        kinlaw = sorted(kinlaw, reverse=True)[0]
                                                    spec_list.append(kinlaw)
                                                    '''
                                                    if exp == str(2) + ' ':
                                                        spec_list.append(2)
                                                        print('Categorie: ' + str(2))  # 2
                                                        print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                    else:
                                                        try:
                                                            int(exp)
                                                            spec_list.append(3)
                                                            print('Categorie: ' + str(3))  # 3
                                                            print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                        except:
                                                            spec_list.append(4)
                                                            print('Categorie: ' + str(4))  # 4
                                                            print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                    '''
                                        elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                            if not 'pow(' in denominator:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                close_power_index = getIndex(denominator, denominator.find('pow(') + 3)
                                                if not all_spec[iSpecId] in denominator[denominator.find('pow(') + 3: close_power_index + 1]:
                                                    spec_list.append(5)
                                                    print('Categorie: ' + str(5))  # 5
                                                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                                else:
                                                    num_comma = denominator.count(', ')
                                                    if num_comma == 1:
                                                        _, b = denominator.split(', ')
                                                        exp, _ = b.split(')', 1)
                                                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                    else:
                                                        kinlaw = []
                                                        for iComma in range(0, num_comma):
                                                            list_of_splits = denominator.split(', ', iComma + 1)
                                                            if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                                kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                                        kinlaw = sorted(kinlaw, reverse=True)[0]
                                                    spec_list.append(kinlaw)
                                                    '''
                                                    if exp == str(2) + ' ':
                                                        spec_list.append(6)
                                                        print('Categorie: ' + str(6))  # 6
                                                        print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                    else:
                                                        try:
                                                            int(exp)
                                                            spec_list.append(7)
                                                            print('Categorie: ' + str(7))  # 7
                                                            print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                        except:
                                                            spec_list.append(8)
                                                            print('Categorie: ' + str(8))  # 8
                                                            print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                    '''
                                        elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                            new_formula = nominator + '* 1 /' + denominator
                                            list_of_categories11 = decomposition(new_formula)
                                            kinlaw_1 = depth1(new_formula, list_of_categories11, all_spec[iSpecId], sbml_file, iReact)
                                            spec_list.append(kinlaw_1)
                                            print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                            #spec_list.append(9)
                                            #print('What to do with species ' + all_spec[iSpecId] + ' from depth1 ?')
                                    else:
                                        num_comma = list_of_categories[iCat].count(', ')
                                        if num_comma == 1:
                                            _, b = list_of_categories[iCat].split(', ')
                                            exp, _ = b.split(')', 1)
                                            comma_index = list_of_categories[iCat].find(',')
                                            nominator = list_of_categories[iCat][5: comma_index]
                                            list_of_categories3 = decomposition(nominator)
                                            kinlaw_1 = depth1(nominator, list_of_categories3, all_spec[iSpecId], sbml_file, iReact)
                                            kinlaw = depthKineticLaw(kinlaw_1, exp, sbml_file, iReact)
                                        else:
                                            kinlaw = []
                                            for iComma in range(0, num_comma):
                                                list_of_splits = list_of_categories[iCat].split(', ', iComma + 1)
                                                if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    comma_index = list_of_categories[iCat].find(',')
                                                    nominator = list_of_categories[iCat][5: comma_index]
                                                    list_of_categories3 = decomposition(nominator)
                                                    kinlaw_1 = depth1(nominator, list_of_categories3, all_spec[iSpecId], sbml_file, iReact)
                                                    kinlaw.append(depthKineticLaw(kinlaw_1, exp, sbml_file, iReact))
                                            kinlaw = sorted(kinlaw, reverse=True)[0]
                                        spec_list.append(kinlaw)
                                        print('Species ' + all_spec[iSpecId] + ' had to go in depth!')

                                else:
                                    slash_index = list_of_categories[iCat].find('/')
                                    nominator = list_of_categories[iCat][0: slash_index]
                                    denominator = list_of_categories[iCat][slash_index + 1: len(list_of_categories[iCat])]
                                    if all_spec[iSpecId] in nominator and all_spec[iSpecId] not in denominator:
                                        if not 'pow(' in nominator:
                                            spec_list.append(1)
                                            print('Categorie: ' + str(1))  # 1
                                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                        else:

                                            ##### possibility: more '/' in pow() in nominator  => e.g. pow((A + B)/C, 2) / D   =>   KinLaw(C) == 6 (!= 1)
                                            #                                                  => e.g. pow(A + B/C, 2) / D     =>   KinLaw(C) == 6 (!= 5, != 1)
                                            # repeat whole categories again + pow(A + B/C) also possible!
                                            # get rid of power and brackets
                                            if '/' in nominator:
                                                num_comma = nominator.count(', ')
                                                if num_comma == 1:
                                                    _, b = nominator.split(', ')
                                                    exp, _ = b.split(')', 1)
                                                    nominator = nominator[5: len(nominator) - 4]
                                                    list_of_categories4 = decomposition(nominator)
                                                    kinlaw_1 = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                    kinlaw = depthKineticLaw(kinlaw_1, exp, sbml_file, iReact)
                                                else:
                                                    kinlaw = []
                                                    for iComma in range(0, num_comma):
                                                        list_of_splits = nominator.split(', ', iComma + 1)
                                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                            nominator = nominator[5: len(nominator) - 4]
                                                            list_of_categories4 = decomposition(nominator)
                                                            kinlaw_1 = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                            kinlaw.append(depthKineticLaw(kinlaw_1, exp, sbml_file, iReact))
                                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                                spec_list.append(kinlaw)
                                                print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                            else:
                                                num_comma = nominator.count(', ')
                                                if num_comma == 1:
                                                    _, b = nominator.split(', ')
                                                    exp, _ = b.split(')', 1)
                                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                else:
                                                    kinlaw = []
                                                    for iComma in range(0, num_comma):
                                                        list_of_splits = nominator.split(', ', iComma + 1)
                                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                            kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                                spec_list.append(kinlaw)
                                                '''            
                                                if exp == str(2) + ' ':
                                                    spec_list.append(2)
                                                    print('Categorie: ' + str(2))  # 2
                                                    print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                else:
                                                    try:
                                                        int(exp)
                                                        spec_list.append(3)
                                                        print('Categorie: ' + str(3))  # 3
                                                        print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                    except:
                                                        spec_list.append(4)
                                                        print('Categorie: ' + str(4))  # 4
                                                        print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                '''
                                    elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                        if not 'pow(' in denominator:
                                            spec_list.append(5)
                                            print('Categorie: ' + str(5))                                                   # 5
                                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                        else:
                                            close_power_index = getIndex(denominator, denominator.find('pow(') + 3)
                                            if not all_spec[iSpecId] in denominator[denominator.find('pow(') + 3: close_power_index + 1]:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                num_comma = denominator.count(', ')
                                                if num_comma == 1:
                                                    _, b = denominator.split(', ')
                                                    exp, _ = b.split(')', 1)
                                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                                else:
                                                    kinlaw = []
                                                    for iComma in range(0, num_comma):
                                                        list_of_splits = denominator.split(', ', iComma + 1)
                                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                            kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                                spec_list.append(kinlaw)
                                                '''
                                                if exp == str(2) + ' ':
                                                    spec_list.append(6)
                                                    print('Categorie: ' + str(6))                                           # 6
                                                    print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                                else:
                                                    try:
                                                        int(exp)
                                                        spec_list.append(7)
                                                        print('Categorie: ' + str(7))                                       # 7
                                                        print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                    except:
                                                        spec_list.append(8)
                                                        print('Categorie: ' + str(8))                                       # 8
                                                        print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                                '''
                                    elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                        new_formula = nominator + '* 1 /' + denominator
                                        list_of_categories12 = decomposition(new_formula)
                                        kinlaw_1 = depth1(new_formula, list_of_categories12, all_spec[iSpecId], sbml_file, iReact)
                                        spec_list.append(kinlaw_1)
                                        print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                        #spec_list.append(9)
                                        #print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')
                            else:
                                slash_index = list_of_categories[iCat].find('/')
                                nominator = list_of_categories[iCat][0 : slash_index]
                                denominator = list_of_categories[iCat][slash_index + 1 : len(list_of_categories[iCat])]
                                if all_spec[iSpecId] in nominator and all_spec[iSpecId] not in denominator:
                                    if not 'pow(' in nominator:
                                        spec_list.append(1)
                                        print('Categorie: ' + str(1))  # 1
                                        print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                    else:

                                        ##### possibility: more '/' in pow() in nominator  => e.g. pow((A + B)/C, 2) / D   =>   KinLaw(C) == 6 (!= 1)
                                        #                                                  => e.g. pow(A + B/C, 2) / D     =>   KinLaw(C) == 6 (!= 5, != 1)
                                        # repeat whole categories again + pow(A + B/C) also possible!
                                        # get rid of power and brackets
                                        if '/' in nominator:
                                            num_comma = nominator.count(', ')
                                            if num_comma == 1:
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                                nominator = nominator[5: len(nominator) - 4]
                                                list_of_categories5 = decomposition(nominator)
                                                kinlaw_1 = depth1(nominator, list_of_categories5, all_spec[iSpecId], sbml_file, iReact)
                                                kinlaw = depthKineticLaw(kinlaw_1, exp, sbml_file, iReact)
                                            else:
                                                kinlaw = []
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = nominator.split(', ', iComma + 1)
                                                    if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][
                                                        iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        nominator = nominator[5: len(nominator) - 4]
                                                        list_of_categories5 = decomposition(nominator)
                                                        kinlaw_1 = depth1(nominator, list_of_categories5, all_spec[iSpecId], sbml_file, iReact)
                                                        kinlaw.append(depthKineticLaw(kinlaw_1, exp, sbml_file, iReact))
                                                kinlaw = sorted(kinlaw, reverse=True)[0]
                                            spec_list.append(kinlaw)
                                            print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                        else:
                                            num_comma = nominator.count(', ')
                                            if num_comma == 1:
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                                kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                            else:
                                                kinlaw = []
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = nominator.split(', ', iComma + 1)
                                                    if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                                kinlaw = sorted(kinlaw, reverse=True)[0]
                                            spec_list.append(kinlaw)
                                            '''
                                            if exp == str(2) + ' ':
                                                spec_list.append(2)
                                                print('Categorie: ' + str(2))  # 2
                                                print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                            else:
                                                try:
                                                    int(exp)
                                                    spec_list.append(3)
                                                    print('Categorie: ' + str(3))  # 3
                                                    print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                                except:
                                                    spec_list.append(4)
                                                    print('Categorie: ' + str(4))  # 4
                                                    print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                            '''
                                elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                    if not 'pow(' in denominator:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                    else:
                                        num_comma = denominator.count(', ')
                                        if num_comma == 1:
                                            _, b = denominator.split(', ')
                                            exp, _ = b.split(')', 1)
                                            kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                        else:
                                            kinlaw = []
                                            for iComma in range(0, num_comma):
                                                list_of_splits = denominator.split(', ', iComma + 1)
                                                if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                            kinlaw = sorted(kinlaw, reverse=True)[0]
                                        spec_list.append(kinlaw)
                                        '''            
                                        if exp == str(2) + ' ':
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))  # 6
                                            print('Species ' + all_spec[iSpecId] + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))  # 7
                                                print('Species ' + all_spec[iSpecId] + ' has a natural exponent!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))  # 8
                                                print('Species ' + all_spec[iSpecId] + ' has a rational exponent!')
                                        '''
                                elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                    new_formula = nominator + '* 1 /' + denominator
                                    list_of_categories13 = decomposition(new_formula)
                                    kinlaw_1 = depth1(new_formula, list_of_categories13, all_spec[iSpecId], sbml_file, iReact)
                                    spec_list.append(kinlaw_1)
                                    print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                    #spec_list.append(9)
                                    #print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')

                kinetic_list.append(spec_list)

        # check what kinetics are available by concatenating all elements of 'kinetic_list'
        conc_kinetic_list = []
        if len(kinetic_list) == 1:
            conc_kinetic_list = kinetic_list
        else:
            for iList in range(0, len(kinetic_list)):
                conc_kinetic_list = conc_kinetic_list + kinetic_list[iList]

        for item in [0,1,2,3,4,5,6,7,8,9]:
            if item in conc_kinetic_list:
                all_formulas_kinetics[iReact].append(1)
            else:
                all_formulas_kinetics[iReact].append(0)
        # sym.expand() gave no error --> False
        all_formulas_kinetics[iReact].append(False)


    # give total kinetic number from 0 - 9 + 'NaN'
    total_kinetics = [sum(x) for x in zip(*all_formulas_kinetics)]
    for iKinetic in range(0, len(total_kinetics)):
        if total_kinetics[iKinetic] > 0:
            if int(total_kinetics[iKinetic]/num_reac) == total_kinetics[iKinetic]/num_reac:
                total_kinetics[iKinetic] = int(total_kinetics[iKinetic] / num_reac)
            else:
                total_kinetics[iKinetic] = total_kinetics[iKinetic] / num_reac
        else:
            total_kinetics[iKinetic] = 0

    only_for_debugging = 'just_debugging'

    return total_kinetics, error_file
