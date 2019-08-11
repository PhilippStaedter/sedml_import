# substitute different parts of a formula

import re
import pandas as pd
import os
import numpy as np
from opposingBracket import *


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

            formula = formula.replace(formula[index_start_pow : index_end_power + 1], Basis + '**' + Exponent)


    return formula


def replaceDoubleStar(formula):

    if '**' in formula:

        # max_num_doublestar = len([m.start() for m in re.finditer('**', formula)])
        for iPower in range(0, 1000):                                                                                   # range(0, max_num_doublestar)

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

            formula = formula.replace(formula[last_whitespace_before + 1 : index_start_doublestar + 2 + first_whitespace_after], 'pow(' + Basis + ',' + Exponent +')')

    return formula