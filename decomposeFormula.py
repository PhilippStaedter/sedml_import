# script to decompose formula in smaller compartments:
# not robust against more special cases!!!

import sys
from opposingBracket import *

##formula = 'pow(FFF, 4) / (A() + Q) + D / A * (AA + DD) * V * Y + ABCABC * B - C * (ZZZZ + R) * pow(X, 3)'

def decomposition(formula):

    formula = formula.replace('( ', '(')
    formula = formula.replace(' )', ')')
    formula = formula.replace(' ,', ',')
    formula = formula[1:]
    formula = formula[:len(formula) - 1]

    # exception:  formula starts with -
    if formula[0] == '-':
        formula = formula[1:]
        if formula[0] == '(':
            matching_index = getIndex(formula,0)
            if matching_index + 2 < len(formula):
                if formula[matching_index + 2] == '+' or formula[matching_index + 2] == '-':                            # for '*' or '/' have the brackets to stay
                    formula = formula[:matching_index] + formula[matching_index + 1:]
                    formula = formula[1:]
            else:
                formula = formula[:len(formula)]
                formula = formula[1:]

    list_of_compartments = []

    iter_object = len(formula)
    iElement = 0
    next_white_space = 0
    while iElement < iter_object:

        # case 1: brackets                                                  # no case for '+' or '-' necessary! (otherwise brackets would be unnecessary)
        if formula[iElement] == '(':
            matching_index = getIndex(formula, iElement)
            if matching_index + 2 < iter_object and next_white_space != -1:
                if formula[matching_index + 2] == '/':

                    # everything all over again
                    if formula[matching_index + 4] == '(':
                        matching_index = getIndex(formula, matching_index + 4)
                        list_of_compartments.append(formula[iElement : matching_index + 1])
                        formula = formula[matching_index + 4 :]
                        iter_object = len(formula)

                    else:
                        next_white_space = formula.find(' ', matching_index + 4)
                        if next_white_space != -1:
                            list_of_compartments.append(formula[iElement: next_white_space])
                            formula = formula[next_white_space + 3:]
                            iter_object = len(formula)
                        else:
                            list_of_compartments.append(formula[iElement : len(formula)])
                            # get to return value
                            iElement = iter_object

                elif formula[matching_index + 2] == '*':
                    list_of_compartments.append(formula[iElement : matching_index + 1])
                    formula = formula[matching_index + 4 :]
                    iter_object = len(formula)

                else:
                    print('This case 1 must not happen ... Something is wrong!')
                    sys.exit()
            else:
                list_of_compartments.append(formula[iElement : len(formula)])
                # get to return value
                iElement = iter_object

        # (special) case 2: starts with 'pow(' without brackets
        elif formula[iElement : iElement + 4] == 'pow(':
            matching_index = getIndex(formula, iElement + 3)
            if matching_index + 2 < iter_object and next_white_space != -1:
                if formula[matching_index + 2] == '+' or formula[matching_index + 2] == '-' or formula[matching_index + 2] == '*':
                    list_of_compartments.append(formula[iElement : matching_index + 1])
                    formula = formula[matching_index + 4:]
                    iter_object = len(formula)

                elif formula[matching_index + 2] == '/':

                    # desaster
                    if formula[matching_index + 4] == '(':
                        matching_index = getIndex(formula, matching_index + 4)
                        list_of_compartments.append(formula[iElement : matching_index + 1])
                        formula = formula[matching_index + 4 :]
                        iter_object = len(formula)

                    else:
                        next_white_space = formula.find(' ', matching_index + 4)
                        if next_white_space != -1:
                            list_of_compartments.append(formula[iElement: next_white_space])
                            formula = formula[next_white_space + 3:]
                            iter_object = len(formula)
                        else:
                            list_of_compartments.append(formula[iElement: len(formula)])
                            # get to return value
                            iElement = iter_object

                else:
                    print('This case 2 must not happen ... Something is wrong!')
                    sys.exit()

            else:
                list_of_compartments.append(formula[iElement: len(formula)])
                # get to return value
                iElement = iter_object

        # case 3: no brackets, no special cases
        elif formula[iElement] != '(' and formula[iElement : iElement + 4] != 'pow(':
            next_white_space = formula.find(' ')
            if next_white_space != -1:
                if formula[next_white_space + 1] == '+' or formula[next_white_space + 1] == '-' or formula[next_white_space + 1] == '*':
                    list_of_compartments.append(formula[iElement : next_white_space])
                    formula = formula[next_white_space + 3 :]
                    iter_object = len(formula)

                elif formula[next_white_space + 1] == '/':

                    # everything all over again
                    if formula[next_white_space + 3] == '(':
                        matching_index = getIndex(formula, next_white_space + 3)
                        list_of_compartments.append(formula[iElement: matching_index + 1])
                        formula = formula[matching_index + 4:]
                        iter_object = len(formula)

                    else:
                        next_white_space = formula.find(' ', next_white_space + 3)
                        if next_white_space != -1:
                            list_of_compartments.append(formula[iElement: next_white_space])
                            formula = formula[next_white_space + 3:]
                            iter_object = len(formula)
                        else:
                            list_of_compartments.append(formula[iElement: len(formula)])
                            # get to return value
                            iElement = iter_object

                else:
                    print('This case 3 must not happen ... Something is wrong!')
                    sys.exit()
            else:
                list_of_compartments.append(formula[iElement : len(formula)])
                # get to return value
                iElement = iter_object

    return list_of_compartments



'''     
        elif formula[next_white_space + 1] == '*':
            list_of_compartments.append(formula[iElement : next_white_space])
            formula = formula[next_white_space + 3 :]
            iter_object = len(formula)
            
        elif formula[next_white_space + 1] == '*' and formula[next_white_space + 3] == '(':
            matching_index = getIndex(formula, next_white_space + 3)
            list_of_compartments.append(formula[iElement : matching_index + 1])
            formula = formula[matching_index + 3:]
            iter_object = len(formula)
'''