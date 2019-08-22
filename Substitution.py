# substitute different parts of a formula

import re
import pandas as pd
import os
import numpy as np
from opposingBracket import *
import sys


def replacePower(formula):

    if 'pow(' in formula:

        max_num_powers = len([m.start() for m in re.finditer('pow', formula)])
        for iPower in range(0, max_num_powers):

            index_start_pow = formula.find('pow(')
            if index_start_pow == -1:
                break
            index_end_power = getIndex(formula, index_start_pow + 3)
            power = formula[index_start_pow : index_end_power]

            a,b = power.split(',')
            _,Basis = a.split('pow(')
            Exponent = b

            formula = formula.replace(formula[index_start_pow : index_end_power + 1], '(' + Basis + ')' + '**' + Exponent)


    return formula


def replaceDoubleStar(formula):

    if '**' in formula:

        # max_num_doublestar = len([m.start() for m in re.finditer('**', formula)])
        new_find_index = 0
        for iPower in range(0, 1000):                                                                                   # range(0, max_num_doublestar)

            # case with brackets: C * ( A + B )**2
            if '(' in formula:
                index_start_doublestar = formula.find('**')
                if index_start_doublestar == -1:
                    break
                for iBracket in range(0, formula.count('(')):
                    start_bracket_index = formula.find('(', new_find_index)
                    end_bracket_index = getIndex(formula, start_bracket_index)
                    index_start_doublestar = formula.find('**')
                    if index_start_doublestar == -1:
                        break
                    if index_start_doublestar < start_bracket_index or start_bracket_index < 0:
                        index_start_doublestar = formula.find('**')
                        if index_start_doublestar == -1:
                            break
                        all_whitespaces_before = [m.start() for m in re.finditer(' ', formula[:index_start_doublestar])]
                        if all_whitespaces_before == []:
                            last_whitespace_before = -1
                        else:
                            last_whitespace_before = all_whitespaces_before[len(all_whitespaces_before) - 1]
                        all_whitespaces_after = [m.start() for m in
                                                 re.finditer(' ', formula[index_start_doublestar + 2:])]
                        if all_whitespaces_after == []:
                            first_whitespace_after = len(formula)
                        else:
                            first_whitespace_after = all_whitespaces_after[0]

                        Basis = formula[last_whitespace_before + 1: index_start_doublestar]
                        Exponent = formula[index_start_doublestar + 2: index_start_doublestar + 2 + first_whitespace_after]

                        formula = formula.replace(formula[last_whitespace_before + 1: index_start_doublestar + 2 + first_whitespace_after], 'pow(' + Basis + ', ' + Exponent + ')')
                        new_find_index = start_bracket_index + 4
                        break

                    # check if the bracket ends at the end of the formula
                    if end_bracket_index + 2 < len(formula):
                        if formula[end_bracket_index + 1] == '*' and formula[end_bracket_index + 2] == '*':
                            all_whitespaces_after = [m.start() for m in re.finditer(' ', formula[end_bracket_index + 3:])]
                            if all_whitespaces_after == []:
                                first_whitespace_after = len(formula)
                            else:
                                first_whitespace_after = all_whitespaces_after[0]

                            Basis = formula[start_bracket_index + 1 : end_bracket_index - 1]
                            Exponent = formula[end_bracket_index + 3 : end_bracket_index + 3 + first_whitespace_after]

                            formula = formula.replace(formula[start_bracket_index : end_bracket_index + 3 + first_whitespace_after], 'pow(' + Basis + ', ' + Exponent + ')')
                            new_find_index = start_bracket_index + 4
                            break
                        elif '**' in formula[start_bracket_index : end_bracket_index + 1]:                                      # e.g. ( A + ( B + C )**2 + D ) / F
                            formula2 = formula[start_bracket_index + 1 : end_bracket_index]
                            formula3 = replaceDoubleStar(formula2)
                            formula = formula.replace(formula2, formula3)
                            new_find_index = start_bracket_index + 1
                        else:
                            new_find_index = start_bracket_index + 1
                    else:
                        if '**' in formula[start_bracket_index + 1 : end_bracket_index]:
                            new_formula = formula[start_bracket_index + 1 : end_bracket_index]
                            new_formula = replaceDoubleStar(new_formula)
                            print('DoubleStar had to go in depth!')
                            formula = formula.replace(formula[start_bracket_index + 1 : end_bracket_index], new_formula)
                            new_find_index = start_bracket_index + 1
                            break
                        else:
                            print('This case must not happen!')
                            sys.exit()

            else:
                index_start_doublestar = formula.find('**')
                if index_start_doublestar == -1:
                    break
                all_whitespaces_before = [m.start() for m in re.finditer(' ', formula[:index_start_doublestar])]
                if all_whitespaces_before == []:
                    last_whitespace_before = -1
                else:
                    last_whitespace_before = all_whitespaces_before[len(all_whitespaces_before) - 1]
                all_whitespaces_after = [m.start() for m in re.finditer(' ', formula[index_start_doublestar+2:])]
                if all_whitespaces_after == []:
                    first_whitespace_after = len(formula)
                else:
                    first_whitespace_after = all_whitespaces_after[0]

                Basis = formula[last_whitespace_before + 1 : index_start_doublestar]
                Exponent = formula[index_start_doublestar + 2 : index_start_doublestar + 2 + first_whitespace_after]

                formula = formula.replace(formula[last_whitespace_before + 1 : index_start_doublestar + 2 + first_whitespace_after], 'pow(' + Basis + ', ' + Exponent +')')

    return formula