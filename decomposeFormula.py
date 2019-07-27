# script to decompose formula in smaller compartments:


from opposingBracket import *

formula = '(AA + DD) * V * Y + ABCABC * B - C * (ZZZZ + R) * X'

#def decomposition(formula):

list_of_compartments = []

iter_object = len(formula)
iElement = 0
while iElement < iter_object:

    # case 1: brackets  ->  ends after closing bracket
    if formula[iElement] == '(':
        matching_index = getIndex(formula, iElement)
        if formula[matching_index + 2] == '/':
            a = 4

        elif formula[matching_index + 2] == '*':
            list_of_compartments.append(formula[iElement: next_white_space])
            formula = formula[next_white_space + 3 :]
            iter_object = len(formula)

        else:
            print('This case must not happen ... Something is wrong!')


    # case 2: just one species
    else:
        next_white_space = formula.find(' ')
        if formula[next_white_space + 1] == '+' or formula[next_white_space + 1] == '-':
            list_of_compartments.append(formula[iElement : next_white_space])
            formula = formula[next_white_space + 3 :]
            iter_object = len(formula)

        elif formula[next_white_space + 1] == '*' and formula[next_white_space + 3] != '(':
            list_of_compartments.append(formula[iElement : next_white_space])
            formula = formula[next_white_space + 3 :]
            iter_object = len(formula)

        elif formula[next_white_space + 1] == '*' and formula[next_white_space + 3] == '(':
            matching_index = getIndex(formula, next_white_space + 3)
            if formula[matching_index + 2] == '/':

                # repeat whole text as before
                a = 4

            else:
                list_of_compartments.append(formula[iElement : matching_index + 1])
                formula = formula[matching_index + 3:]
                iter_object = len(formula)