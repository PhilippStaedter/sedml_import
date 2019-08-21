####### divide denominator into categories for better Investigation

from decomposeFormula import *
from Depth1_KinLaw import *


def decomposeDenominator(denominator, all_spec, iSpecId, sbml_file, iReact, iCat, spec_list):

    new_denominator = decomposition(denominator)
    for iCat2 in range(0, len(new_denominator)):
        if not all_spec[iSpecId] in new_denominator[iCat2]:
            'Do nothing'
        else:
            if not '/' in new_denominator[iCat2]:
                if not 'pow(' in new_denominator[iCat2]:
                    spec_list.append(5)
                    print('Categorie: ' + str(5))  # 5
                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                else:
                    close_power_index = getIndex(new_denominator[iCat2], new_denominator[iCat2].find('pow(') + 3)
                    if not all_spec[iSpecId] in new_denominator[iCat2][
                                                new_denominator[iCat2].find('pow(') + 3: close_power_index + 1]:
                        spec_list.append(5)
                        print('Categorie: ' + str(5))  # 5
                        print('Variable ' + all_spec[iSpecId] + ' is linear!')
                    else:
                        num_comma = new_denominator[iCat2].count(', ')
                        if num_comma == 1:
                            _, b = new_denominator[iCat2].split(', ')
                            exp, _ = b.split(')', 1)
                            kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                        else:
                            kinlaw = []
                            for iComma in range(0, num_comma):
                                list_of_splits = new_denominator[iCat2].split(', ', iComma + 1)
                                if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                    exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                    kinlaw.append(depthKineticLaw(5, exp, sbml_file, iReact))
                            kinlaw = sorted(kinlaw, reverse=True)[0]
                        spec_list.append(kinlaw)
            else:
                if '(' in new_denominator[iCat]:
                    if new_denominator[iCat][1] == '(':  # [1], because 0 is a white space!
                        matching_index = getIndex(new_denominator[iCat], 1)
                        slash_index = matching_index + 2
                        nominator2 = new_denominator[iCat][1: matching_index + 1]
                        denominator2 = new_denominator[iCat][slash_index + 1: len(new_denominator[iCat])]
                        if all_spec[iSpecId] in nominator2 and all_spec[iSpecId] not in denominator2:
                            if not 'pow(' in nominator2:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 1
                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                            else:
                                num_comma = new_denominator[iCat].count(', ')
                                if num_comma == 1:
                                    _, b = new_denominator[iCat].split(', ')
                                    exp, _ = b.split(')', 1)
                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                else:
                                    kinlaw = []
                                    for iComma in range(0, num_comma):
                                        list_of_splits = new_denominator[iCat].split(', ', iComma + 1)
                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                spec_list.append(kinlaw)
                        else:
                            spec_list.append(9)
                            print('The denominator has species ' + all_spec[
                                iSpecId] + ' in its own denominator')
                    elif new_denominator[iCat][1:5] == 'pow(' and '/' in new_denominator[iCat][
                                                                         5: getIndex(new_denominator[iCat], 4)]:
                        matching_index = getIndex(new_denominator[iCat], 4)
                        if matching_index + 2 < len(new_denominator[iCat]) and new_denominator[iCat][
                            matching_index + 2] == '/':
                            nominator2 = new_denominator[iCat][0: matching_index + 2]
                            denominator2 = new_denominator[iCat][matching_index + 3: len(new_denominator[iCat])]
                            if all_spec[iSpecId] in nominator2 and all_spec[iSpecId] not in denominator2:
                                if not 'pow(' in nominator2:
                                    spec_list.append(5)
                                    print('Categorie: ' + str(5))  # 1
                                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                else:
                                    num_comma = new_denominator[iCat].count(', ')
                                    if num_comma == 1:
                                        _, b = new_denominator[iCat].split(', ')
                                        exp, _ = b.split(')', 1)
                                        kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                    else:
                                        kinlaw = []
                                        for iComma in range(0, num_comma):
                                            list_of_splits = new_denominator[iCat].split(', ', iComma + 1)
                                            if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                                exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                                kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                        kinlaw = sorted(kinlaw, reverse=True)[0]
                                    spec_list.append(kinlaw)
                            else:
                                spec_list.append(9)
                                print('The denominator has species ' + all_spec[iSpecId] + ' in its own denominator')
                    else:
                        slash_index = new_denominator[iCat].find('/')
                        nominator2 = new_denominator[iCat][0: slash_index]
                        denominator2 = new_denominator[iCat][slash_index + 1: len(new_denominator[iCat])]
                        if all_spec[iSpecId] in nominator2 and all_spec[iSpecId] not in denominator2:
                            if not 'pow(' in nominator2:
                                spec_list.append(5)
                                print('Categorie: ' + str(5))  # 1
                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                            else:
                                num_comma = new_denominator[iCat].count(', ')
                                if num_comma == 1:
                                    _, b = new_denominator[iCat].split(', ')
                                    exp, _ = b.split(')', 1)
                                    kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                                else:
                                    kinlaw = []
                                    for iComma in range(0, num_comma):
                                        list_of_splits = new_denominator[iCat].split(', ', iComma + 1)
                                        if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                            exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                            kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                    kinlaw = sorted(kinlaw, reverse=True)[0]
                                spec_list.append(kinlaw)
                        else:
                            spec_list.append(9)
                            print('The denominator has species ' + all_spec[iSpecId] + ' in its own denominator')
                else:
                    slash_index = new_denominator[iCat].find('/')
                    nominator2 = new_denominator[iCat][0: slash_index]
                    denominator2 = new_denominator[iCat][slash_index + 1: len(new_denominator[iCat])]
                    if all_spec[iSpecId] in nominator2 and all_spec[iSpecId] not in denominator2:
                        if not 'pow(' in nominator2:
                            spec_list.append(5)
                            print('Categorie: ' + str(5))  # 1
                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                        else:
                            num_comma = new_denominator[iCat].count(', ')
                            if num_comma == 1:
                                _, b = new_denominator[iCat].split(', ')
                                exp, _ = b.split(')', 1)
                                kinlaw = depthKineticLaw(1, exp, sbml_file, iReact)
                            else:
                                kinlaw = []
                                for iComma in range(0, num_comma):
                                    list_of_splits = new_denominator[iCat].split(', ', iComma + 1)
                                    if all_spec[iSpecId] in list_of_splits[0: len(list_of_splits) - 1][iComma]:
                                        exp, _ = list_of_splits[len(list_of_splits) - 1].split(')', 1)
                                        kinlaw.append(depthKineticLaw(1, exp, sbml_file, iReact))
                                kinlaw = sorted(kinlaw, reverse=True)[0]
                            spec_list.append(kinlaw)
                    else:
                        spec_list.append(9)
                        print('The denominator has species ' + all_spec[iSpecId] + ' in its own denominator')

    return spec_list