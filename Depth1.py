# script to analyse depth1

import numpy as np
from decomposeFormula import *
from opposingBracket import *
from Depth1_KinLaw import *


def depth1(formula, list_of_categories, iSpecId, sbml_file, iReact):

    # replace all brackets and commas by themselfes and spaces before and after + add spaces in front of and behind the category
    for iCat in range(0, len(list_of_categories)):
        list_of_categories[iCat] = list_of_categories[iCat].replace('(', '( ')
        list_of_categories[iCat] = list_of_categories[iCat].replace(')', ' )')
        list_of_categories[iCat] = list_of_categories[iCat].replace(',', ' ,')
        list_of_categories[iCat] = list_of_categories[iCat].rjust(len(list_of_categories[iCat]) + 1)
        list_of_categories[iCat] = list_of_categories[iCat].ljust(len(list_of_categories[iCat]) + 1)

    # assign number of 0 - 8 ///   assign True(1) or False(0)
    kinetic_list = []
    if not iSpecId in formula:
        kinetic_list.append(0)
    else:
        spec_list = []
        for iCat in range(0, len(list_of_categories)):
            if not iSpecId in list_of_categories[iCat]:
                'Do nothing'
            else:
                if not '/' in list_of_categories[iCat]:
                    if not 'pow(' in list_of_categories[iCat]:
                        spec_list.append(1)
                        print('Categorie: ' + str(1))  # 1
                        print('Variable ' + iSpecId + ' is linear!')
                    else:
                        num_comma = list_of_categories[iCat].count(', ')
                        if num_comma == 1:
                            _, b = list_of_categories[iCat].split(', ')
                            exp, _ = b.split(')', 1)
                        else:
                            for iComma in range(0, num_comma):
                                list_of_splits = list_of_categories[iCat].split(', ', iComma + 1)
                                if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                    break
                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                        spec_list.append(kinlaw)
                        '''            
                        if exp == str(2) + ' ':
                            spec_list.append(2)
                            print('Categorie: ' + str(2))  # 2
                            print('Species ' + iSpecId + ' is quadratic!')
                        else:
                            try:
                                int(exp)
                                spec_list.append(3)
                                print('Categorie: ' + str(3))  # 3
                                print('Species ' + iSpecId + ' has a natural exponent!')
                            except:
                                spec_list.append(4)
                                print('Categorie: ' + str(4))  # 4
                                print('Species ' + iSpecId + ' has a rational exponent!')
                        '''
                else:
                    if '(' in list_of_categories[iCat]:
                        if list_of_categories[iCat][1] == '(':  # [1], because 0 is a white space!
                            matching_index = getIndex(list_of_categories[iCat], 1)
                            slash_index = matching_index + 2
                            nominator = list_of_categories[iCat][1: matching_index + 1]
                            denominator = list_of_categories[iCat][slash_index + 1: len(list_of_categories[iCat])]
                            if iSpecId in nominator and iSpecId not in denominator:

                                ##### posiibility: more '/' in nominator  => e.g. (A + B/C) / D   =>   KinLaw(C ) == 5 (!= 1)
                                # repeat whole categories again + pow(A + B/C) also possible!
                                # get rid of starting brackets
                                if '/' in nominator:
                                    nominator = nominator[1 : len(nominator) - 1]
                                    list_of_categories2 = decomposition(nominator)
                                    kinlaw = depth1(nominator, list_of_categories2, iSpecId, sbml_file, iReact)
                                    spec_list.append(kinlaw)
                                    print('Species ' + iSpecId + ' had to go in depth!')
                                else:
                                    if not 'pow(' in nominator:
                                        spec_list.append(1)
                                        print('Categorie: ' + str(1))  # 1
                                        print('Variable ' + iSpecId + ' is linear!')
                                    else:
                                        close_power_index = getIndex(nominator, nominator.find('pow(') + 3)
                                        if not iSpecId in nominator[nominator.find('pow(') + 3: close_power_index + 1]:
                                            spec_list.append(1)
                                            print('Categorie: ' + str(1))  # 1
                                            print('Variable ' + iSpecId + ' is linear!')
                                        else:
                                            num_comma = nominator.count(', ')
                                            if num_comma == 1:
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                            else:
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = nominator.split(', ', iComma + 1)
                                                    if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        break
                                            kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                            spec_list.append(kinlaw)
                                            '''            
                                            if exp == str(2) + ' ':
                                                spec_list.append(2)
                                                print('Categorie: ' + str(2))  # 2
                                                print('Species ' + iSpecId + ' is quadratic!')
                                            else:
                                                try:
                                                    int(exp)
                                                    spec_list.append(3)
                                                    print('Categorie: ' + str(3))  # 3
                                                    print('Species ' + iSpecId + ' has a natural exponent!')
                                                except:
                                                    spec_list.append(4)
                                                    print('Categorie: ' + str(4))  # 4
                                                    print('Species ' + iSpecId + ' has a rational exponent!')
                                            '''
                            elif iSpecId not in nominator and iSpecId in denominator:
                                if not 'pow(' in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))  # 5
                                    print('Variable ' + iSpecId + ' is linear!')
                                else:
                                    close_power_index = getIndex(nominator, nominator.find('pow(') + 3)
                                    if not iSpecId in nominator[nominator.find('pow(') + 3: close_power_index + 1]:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + iSpecId + ' is linear!')
                                    else:
                                        num_comma = denominator.count(', ')
                                        if num_comma == 1:
                                            _, b = denominator.split(', ')
                                            exp, _ = b.split(')', 1)
                                        else:
                                            for iComma in range(0, num_comma):
                                                list_of_splits = denominator.split(', ', iComma + 1)
                                                if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    break
                                        kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                        spec_list.append(kinlaw)
                                        '''            
                                        if exp == str(2) + ' ':
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))  # 6
                                            print('Species ' + iSpecId + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))  # 7
                                                print('Species ' + iSpecId + ' has a natural exponent!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))  # 8
                                                print('Species ' + iSpecId + ' has a rational exponent!')
                                        '''
                            elif iSpecId in nominator and iSpecId in denominator:
                                spec_list.append(9)  # 9
                                print('What to do with species ' + iSpecId + ' from Depth1 ?')
                        elif list_of_categories[iCat][1:5] == 'pow(' and '/' in list_of_categories[iCat][5: getIndex(list_of_categories[iCat],4)]:
                            matching_index = getIndex(list_of_categories[iCat], 4)
                            if matching_index + 2 < len(list_of_categories[iCat]) and list_of_categories[iCat][matching_index + 2] == '/':
                                nominator = list_of_categories[iCat][0: matching_index + 2]
                                denominator = list_of_categories[iCat][
                                              matching_index + 3: len(list_of_categories[iCat])]
                                if iSpecId in nominator and iSpecId not in denominator:
                                    if not 'pow(' in nominator:
                                        spec_list.append(1)
                                        print('Categorie: ' + str(1))  # 1
                                        print('Variable ' + iSpecId + ' is linear!')
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
                                            else:
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = nominator.split(', ', iComma + 1)
                                                    if iSpecId in list_of_splits[0: len(list_of_splits) - 1][
                                                        iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        break
                                            nominator = nominator[5: len(nominator) - 4]
                                            list_of_categories4 = decomposition(nominator)
                                            kinlaw = depth1(nominator, list_of_categories4, iSpecId, sbml_file, iReact)

                                            # call function to get the right kinetic law for the special case
                                            kinlaw = depthKineticLaw(kinlaw, exp, sbml_file, iReact)

                                            spec_list.append(kinlaw)
                                            print('Species ' + iSpecId + ' had to go in depth!')
                                        else:
                                            num_comma = nominator.count(', ')
                                            if num_comma == 1:
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                            else:
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = nominator.split(', ', iComma + 1)
                                                    if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        break
                                            kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                            spec_list.append(kinlaw)
                                            '''            
                                            if exp == str(2) + ' ':
                                                spec_list.append(2)
                                                print('Categorie: ' + str(2))  # 2
                                                print('Species ' + iSpecId + ' is quadratic!')
                                            else:
                                                try:
                                                    int(exp)
                                                    spec_list.append(3)
                                                    print('Categorie: ' + str(3))  # 3
                                                    print('Species ' + iSpecId + ' has a natural exponent!')
                                                except:
                                                    spec_list.append(4)
                                                    print('Categorie: ' + str(4))  # 4
                                                    print('Species ' + iSpecId + ' has a rational exponent!')
                                            '''
                                elif iSpecId not in nominator and iSpecId in denominator:
                                    if not 'pow(' + iSpecId in denominator:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + iSpecId + ' is linear!')
                                    else:
                                        close_power_index = getIndex(nominator, nominator.find('pow(') + 3)
                                        if not iSpecId in nominator[nominator.find('pow(') + 3: close_power_index + 1]:
                                            spec_list.append(5)
                                            print('Categorie: ' + str(5))  # 5
                                            print('Variable ' + iSpecId + ' is linear!')
                                        else:
                                            num_comma = denominator.count(', ')
                                            if num_comma == 1:
                                                _, b = denominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                            else:
                                                for iComma in range(0, num_comma):
                                                    list_of_splits = denominator.split(', ', iComma + 1)
                                                    if iSpecId in list_of_splits[0: len(list_of_splits) - 1][
                                                        iComma]:
                                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                        break
                                            kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                            spec_list.append(kinlaw)
                                            '''            
                                            if exp == str(2) + ' ':
                                                spec_list.append(6)
                                                print('Categorie: ' + str(6))  # 6
                                                print('Species ' + iSpecId + ' is quadratic!')
                                            else:
                                                try:
                                                    int(exp)
                                                    spec_list.append(7)
                                                    print('Categorie: ' + str(7))  # 7
                                                    print('Species ' + iSpecId + ' has a natural exponent!')
                                                except:
                                                    spec_list.append(8)
                                                    print('Categorie: ' + str(8))  # 8
                                                    print('Species ' + iSpecId + ' has a rational exponent!')
                                            '''
                                elif iSpecId in nominator and iSpecId in denominator:
                                    spec_list.append(9)
                                    print('What to do with species ' + iSpecId + ' from depth1 ?')
                            else:
                                num_comma = list_of_categories[iCat].count(', ')
                                if num_comma == 1:
                                    _, b = list_of_categories[iCat].split(', ')
                                    exp, _ = b.split(')', 1)
                                else:
                                    for iComma in range(0, num_comma):
                                        list_of_splits = list_of_categories[iCat].split(', ', iComma + 1)
                                        if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            break
                                comma_index = list_of_categories[iCat].find(',')
                                nominator = list_of_categories[iCat][5: comma_index]
                                list_of_categories3 = decomposition(nominator)
                                kinlaw = depth1(nominator, list_of_categories3, iSpecId, sbml_file, iReact)

                                # call function to get the right kinetic law for the special case
                                kinlaw = depthKineticLaw(kinlaw, exp, sbml_file, iReact)

                                spec_list.append(kinlaw)
                                print('Species ' + iSpecId + ' had to go in depth!')
                        else:
                            slash_index = list_of_categories[iCat].find('/')
                            nominator = list_of_categories[iCat][0: slash_index]
                            denominator = list_of_categories[iCat][slash_index + 1: len(list_of_categories[iCat])]
                            if iSpecId in nominator and iSpecId not in denominator:
                                if not 'pow(' in nominator:
                                    spec_list.append(1)
                                    print('Categorie: ' + str(1))  # 1
                                    print('Variable ' + iSpecId + ' is linear!')
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
                                        else:
                                            for iComma in range(0, num_comma):
                                                list_of_splits = nominator.split(', ', iComma + 1)
                                                if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    break
                                        nominator = nominator[5: len(nominator) - 4]
                                        list_of_categories3 = decomposition(nominator)
                                        kinlaw = depth1(nominator, list_of_categories3, iSpecId, sbml_file, iReact)

                                        # call function to get the right kinetic law for the special case
                                        kinlaw = depthKineticLaw(kinlaw, exp, sbml_file, iReact)

                                        spec_list.append(kinlaw)
                                        print('Species ' + iSpecId + ' had to go in depth!')
                                    else:
                                        num_comma = nominator.count(', ')
                                        if num_comma == 1:
                                            _, b = nominator.split(', ')
                                            exp, _ = b.split(')', 1)
                                        else:
                                            for iComma in range(0, num_comma):
                                                list_of_splits = nominator.split(', ', iComma + 1)
                                                if iSpecId in list_of_splits[0: len(list_of_splits) - 1][
                                                    iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    break
                                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                        spec_list.append(kinlaw)
                                        '''            
                                        if exp == str(2) + ' ':
                                            spec_list.append(2)
                                            print('Categorie: ' + str(2))  # 2
                                            print('Species ' + iSpecId + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(3)
                                                print('Categorie: ' + str(3))  # 3
                                                print('Species ' + iSpecId + ' has a natural exponent!')
                                            except:
                                                spec_list.append(4)
                                                print('Categorie: ' + str(4))  # 4
                                                print('Species ' + iSpecId + ' has a rational exponent!')
                                        '''
                            elif iSpecId not in nominator and iSpecId in denominator:
                                if not 'pow(' + iSpecId in denominator:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))  # 5
                                    print('Variable ' + iSpecId + ' is linear!')
                                else:
                                    close_power_index = getIndex(nominator, nominator.find('pow(') + 3)
                                    if not iSpecId in nominator[nominator.find('pow(') + 3: close_power_index + 1]:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + iSpecId + ' is linear!')
                                    else:
                                        num_comma = denominator.count(', ')
                                        if num_comma == 1:
                                            _, b = denominator.split(', ')
                                            exp, _ = b.split(')', 1)
                                        else:
                                            for iComma in range(0, num_comma):
                                                list_of_splits = denominator.split(', ', iComma + 1)
                                                if iSpecId in list_of_splits[0: len(list_of_splits) - 1][
                                                    iComma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    break
                                        kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                        spec_list.append(kinlaw)
                                        '''
                                        if exp == str(2) + ' ':
                                            spec_list.append(6)
                                            print('Categorie: ' + str(6))  # 6
                                            print('Species ' + iSpecId + ' is quadratic!')
                                        else:
                                            try:
                                                int(exp)
                                                spec_list.append(7)
                                                print('Categorie: ' + str(7))  # 7
                                                print('Species ' + iSpecId + ' has a natural exponent!')
                                            except:
                                                spec_list.append(8)
                                                print('Categorie: ' + str(8))  # 8
                                                print('Species ' + iSpecId + ' has a rational exponent!')
                                        '''
                            elif iSpecId in nominator and iSpecId in denominator:
                                spec_list.append(9)
                                print('What to do with species ' + iSpecId + ' from depth1 ?')
                    else:
                        slash_index = list_of_categories[iCat].find('/')
                        nominator = list_of_categories[iCat][0: slash_index]
                        denominator = list_of_categories[iCat][slash_index + 1: len(list_of_categories[iCat])]
                        if iSpecId in nominator and iSpecId not in denominator:
                            if not 'pow(' in nominator:
                                spec_list.append(1)
                                print('Categorie: ' + str(1))  # 1
                                print('Variable ' + iSpecId + ' is linear!')
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
                                    else:
                                        for iComma in range(0, num_comma):
                                            list_of_splits = nominator.split(', ', iComma + 1)
                                            if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                break
                                    nominator = nominator[5: len(nominator) - 4]
                                    list_of_categories4 = decomposition(nominator)
                                    kinlaw = depth1(nominator, list_of_categories4, iSpecId, sbml_file, iReact)

                                    # call function to get the right kinetic law for the special case
                                    kinlaw = depthKineticLaw(kinlaw, exp, sbml_file, iReact)

                                    spec_list.append(kinlaw)
                                    print('Species ' + iSpecId + ' had to go in depth!')
                                else:
                                    num_comma = nominator.count(', ')
                                    if num_comma == 1:
                                        _, b = nominator.split(', ')
                                        exp, _ = b.split(')', 1)
                                    else:
                                        for iComma in range(0, num_comma):
                                            list_of_splits = nominator.split(', ', iComma + 1)
                                            if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                break
                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                    spec_list.append(kinlaw)
                                    '''
                                    if exp == str(2) + ' ':
                                        spec_list.append(2)
                                        print('Categorie: ' + str(2))  # 2
                                        print('Species ' + iSpecId + ' is quadratic!')
                                    else:
                                        try:
                                            int(exp)
                                            spec_list.append(3)
                                            print('Categorie: ' + str(3))  # 3
                                            print('Species ' + iSpecId + ' has a natural exponent!')
                                        except:
                                            spec_list.append(4)
                                            print('Categorie: ' + str(4))  # 4
                                            print('Species ' + iSpecId + ' has a rational exponent!')
                                    '''
                        elif iSpecId not in nominator and iSpecId in denominator:
                            if not 'pow(' in denominator:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 5
                                print('Variable ' + iSpecId + ' is linear!')
                            else:
                                num_comma = denominator.count(', ')
                                if num_comma == 1:
                                    _, b = denominator.split(', ')
                                    exp, _ = b.split(')', 1)
                                else:
                                    for iComma in range(0, num_comma):
                                        list_of_splits = denominator.split(', ', iComma + 1)
                                        if iSpecId in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            break
                                kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                spec_list.append(kinlaw)
                                '''
                                if exp == str(2) + ' ':
                                    spec_list.append(6)
                                    print('Categorie: ' + str(6))  # 6
                                    print('Species ' + iSpecId + ' is quadratic!')
                                else:
                                    try:
                                        int(exp)
                                        spec_list.append(7)
                                        print('Categorie: ' + str(7))  # 7
                                        print('Species ' + iSpecId + ' has a natural exponent!')
                                    except:
                                        spec_list.append(8)
                                        print('Categorie: ' + str(8))  # 8
                                        print('Species ' + iSpecId + ' has a rational exponent!')
                                '''
                        elif iSpecId in nominator and iSpecId in denominator:
                            spec_list.append(9)
                            print('What to do with species ' + iSpecId + ' from depth1 ?')

        kinetic_list.append(spec_list)

    # check how often the species appears
    conc_kinetic_list = []
    for iList in range(0, len(kinetic_list)):
        conc_kinetic_list = conc_kinetic_list + kinetic_list[iList]

    if np.count_nonzero(conc_kinetic_list) == 0:
        kinlaw = 0
    elif np.count_nonzero(conc_kinetic_list) == 1:
        non_zero_index = [i for i, e in enumerate(conc_kinetic_list) if e != 0][0]
        kinlaw = conc_kinetic_list[non_zero_index]
    else:
        kinlaw = 9

    return kinlaw