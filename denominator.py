####### divide denominator into categories for better Investigation

from decomposeFormula import *
from Depth1_KinLaw import *
import sys


def decomposeDenominator(denominator, all_spec, iSpecId, sbml_file, iReact, iCat, spec_list):

    ### eliminate first bracket if existent
    if denominator[1] == '(':
        end_bracket_index = getIndex(denominator, 1)
        denominator = denominator[2: end_bracket_index]

    new_denominator = decomposition(denominator)
    # replace all brackets and commas by themselfes and spaces before and after + add spaces in front of and behind the category
    for iCat2 in range(0, len(new_denominator)):
        new_denominator[iCat2] = new_denominator[iCat2].replace('(', '( ')
        new_denominator[iCat2] = new_denominator[iCat2].replace(')', ' )')
        new_denominator[iCat2] = new_denominator[iCat2].replace(',', ' ,')
        new_denominator[iCat2] = new_denominator[iCat2].rjust(len(new_denominator[iCat2]) + 1)
        new_denominator[iCat2] = new_denominator[iCat2].ljust(len(new_denominator[iCat2]) + 1)

    for iCat2 in range(0, len(new_denominator)):
        if not iSpecId in new_denominator[iCat2]:
           'Do nothing'
        else:
            if not '/' in new_denominator[iCat2]:
                if not 'pow(' in new_denominator[iCat2]:
                    spec_list.append(5)
                    print('Categorie: ' + str(5))  # 5
                    print('Variable ' + iSpecId + ' is linear!')
                else:
                    close_power_index = getIndex(new_denominator[iCat2], new_denominator[iCat2].find('pow(') + 3)
                    if not iSpecId in new_denominator[iCat2][new_denominator[iCat2].find('pow(') + 3: close_power_index + 1]:
                        spec_list.append(5)
                        print('Categorie: ' + str(5))  # 5
                        print('Variable ' + iSpecId + ' is linear!')
                    else:
                        num_comma = new_denominator[iCat2].count(', ')
                        if num_comma == 1:
                            _, b = new_denominator[iCat2].split(', ')
                            exp, _ = b.split(')', 1)
                            kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                        else:
                            kinlaw = []
                            all_kinlaw = []
                            for iComma in range(0, num_comma):
                                list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                if iSpecId in list_of_splits[0: len(list_of_splits)][iComma]:
                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                    all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                elif iComma == num_comma - 1:
                                    if iSpecId in list_of_splits[0: len(list_of_splits)][num_comma]:
                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                        all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                            for item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                if item in all_kinlaw:
                                    kinlaw.append(item)
                            # kinlaw = sorted(kinlaw, reverse=True)[0]
                        spec_list.append(kinlaw)
            else:
                if '(' in new_denominator[iCat2]:
                    if new_denominator[iCat2][1] == '(':  # [1], because 0 is a white space!
                        matching_index = getIndex(new_denominator[iCat2], 1)
                        slash_index = matching_index + 2
                        nominator2 = new_denominator[iCat2][1: matching_index + 1]
                        denominator2 = new_denominator[iCat2][slash_index + 1: len(new_denominator[iCat2])]
                        if iSpecId in nominator2 and iSpecId not in denominator2:
                            if not 'pow(' in nominator2:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 1
                                print('Variable ' + iSpecId + ' is linear!')
                            else:
                                num_comma = new_denominator[iCat2].count(', ')
                                if num_comma == 1:
                                    _, b = new_denominator[iCat2].split(', ')
                                    exp, _ = b.split(')', 1)
                                    kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                else:
                                    kinlaw = []
                                    all_kinlaw = []
                                    for iComma in range(0, num_comma):
                                        list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                        if iSpecId in list_of_splits[0: len(list_of_splits)][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                        elif iComma == num_comma - 1:
                                            if iSpecId in list_of_splits[0: len(list_of_splits)][num_comma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                    for item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                        if item in all_kinlaw:
                                            kinlaw.append(item)
                                   # kinlaw = sorted(kinlaw, reverse=True)[0]
                                spec_list.append(kinlaw)
                        else:
                            spec_list.append(9)
                            print('The denominator has species ' + all_spec[
                                iSpecId] + ' in its own denominator')
                    elif new_denominator[iCat2][1:5] == 'pow(' and '/' in new_denominator[iCat2][5: getIndex(new_denominator[iCat2], 4)]:
                        matching_index = getIndex(new_denominator[iCat2], 4)
                        if matching_index + 2 < len(new_denominator[iCat2]) and new_denominator[iCat2][matching_index + 2] == '/':
                            nominator2 = new_denominator[iCat2][0: matching_index + 2]
                            denominator2 = new_denominator[iCat2][matching_index + 3: len(new_denominator[iCat2])]
                            if iSpecId in nominator2 and iSpecId not in denominator2:
                                if not 'pow(' in nominator2:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))  # 1
                                    print('Variable ' + iSpecId + ' is linear!')
                                else:
                                    num_comma = new_denominator[iCat2].count(', ')
                                    if num_comma == 1:
                                        _, b = new_denominator[iCat2].split(', ')
                                        exp, _ = b.split(')', 1)
                                        kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                    else:
                                        kinlaw = []
                                        all_kinlaw = []
                                        for iComma in range(0, num_comma):
                                            list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                            if iSpecId in list_of_splits[0: len(list_of_splits)][iComma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                            elif iComma == num_comma - 1:
                                                if iSpecId in list_of_splits[0: len(list_of_splits)][num_comma]:
                                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                    all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                        for item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                            if item in all_kinlaw:
                                                kinlaw.append(item)
                                        # kinlaw = sorted(kinlaw, reverse=True)[0]
                                    spec_list.append(kinlaw)
                            else:
                                spec_list.append(9)
                                print('The denominator has species ' + iSpecId + ' in its own denominator')
                    else:
                        slash_index = new_denominator[iCat2].find('/')
                        nominator2 = new_denominator[iCat2][0: slash_index]
                        denominator2 = new_denominator[iCat2][slash_index + 1: len(new_denominator[iCat2])]
                        if iSpecId in nominator2 and iSpecId not in denominator2:
                            if not 'pow(' in nominator2:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 1
                                print('Variable ' + iSpecId + ' is linear!')
                            else:
                                num_comma = new_denominator[iCat2].count(', ')
                                if num_comma == 1:
                                    _, b = new_denominator[iCat2].split(', ')
                                    exp, _ = b.split(')', 1)
                                    kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                                else:
                                    kinlaw = []
                                    all_kinlaw = []
                                    for iComma in range(0, num_comma):
                                        list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                        if iSpecId in list_of_splits[0: len(list_of_splits)][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                        elif iComma == num_comma - 1:
                                            if iSpecId in list_of_splits[0: len(list_of_splits)][num_comma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                    for item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                        if item in all_kinlaw:
                                            kinlaw.append(item)
                                    # kinlaw = sorted(kinlaw, reverse=True)[0]
                                spec_list.append(kinlaw)
                        else:
                            spec_list.append(9)
                            print('The denominator has species ' + iSpecId + ' in its own denominator')
                else:
                    slash_index = new_denominator[iCat2].find('/')
                    nominator2 = new_denominator[iCat2][0: slash_index]
                    denominator2 = new_denominator[iCat2][slash_index + 1: len(new_denominator[iCat2])]
                    if iSpecId in nominator2 and iSpecId not in denominator2:
                        if not 'pow(' in nominator2:
                            spec_list.append(5)
                            print('Categorie: ' + str(5))  # 1
                            print('Variable ' + iSpecId + ' is linear!')
                        else:
                            num_comma = new_denominator[iCat2].count(', ')
                            if num_comma == 1:
                                _, b = new_denominator[iCat2].split(', ')
                                exp, _ = b.split(')', 1)
                                kinlaw = depthKineticLaw(5, exp, sbml_file, iReact)
                            else:
                                kinlaw = []
                                all_kinlaw = []
                                for iComma in range(0, num_comma):
                                    list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                    if iSpecId in list_of_splits[0: len(list_of_splits)][iComma]:
                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                        all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                    elif iComma == num_comma - 1:
                                        if iSpecId in list_of_splits[0: len(list_of_splits)][num_comma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            all_kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                                for item in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                                    if item in all_kinlaw:
                                        kinlaw.append(item)
                                # kinlaw = sorted(kinlaw, reverse=True)[0]
                            spec_list.append(kinlaw)
                    else:
                        spec_list.append(9)
                        print('The denominator has species ' + iSpecId + ' in its own denominator')

    return spec_list