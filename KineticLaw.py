# script to determine what kinetic law a formal has

import libsbml
from decomposeFormula import *
from opposingBracket import *
from Depth1 import *

#iModel = 'Froehlich2018'
#iFile = 'Froehlich2018'


def getKineticLaw(iModel, iFile):

    # split for extension
    iFile,ext = iFile.split('.')

    # important path
    sbml_path = './sedml_models/' + iModel + '/sbml_models/' + iFile + '.' + ext  #'.xml'  #'.sbml'

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

    '''
    # get all compartments
    all_comp = []
    for iComp in range(0, num_comp):
        all_comp.append(sbml_file.getModel().getCompartment(iComp).getId())

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
    all_spec = []
    for iMeta in range(0, num_spec):
        all_spec.append(sbml_file.getModel().getSpecies(iMeta).getMetaId())
    
    # change species Ids as previously shown
    for iSpecMeta in range(0, len(all_spec)):
        if len(all_spec[iSpecMeta].split('_')[1]) == 1:
            all_spec[iSpecMeta] = all_spec[iSpecMeta].split('_')[0] + '_A_' + all_spec[iSpecMeta].split('_')[1]
        elif len(all_spec[iSpecMeta].split('_')[1]) == 2:
            all_spec[iSpecMeta] = all_spec[iSpecMeta].split('_')[0] + '_B_' + all_spec[iSpecMeta].split('_')[1]
        elif len(all_spec[iSpecMeta].split('_')[1]) == 3:
            all_spec[iSpecMeta] = all_spec[iSpecMeta].split('_')[0] + '_C_' + all_spec[iSpecMeta].split('_')[1]
    '''

    ###### get Kinetic Law
    all_formulas_kinetics = [[] for i in range(0,num_reac)]
    for iReact in range(0, num_reac):

        # get MathMl formula as string
        formula = libsbml.formulaToString(sbml_file.getModel().getReaction(iReact).getKineticLaw().getMath())

        formula = formula.replace('(', '( ')
        formula = formula.replace(')', ' )')
        formula = formula.replace(',', ' ,')
        formula = formula.rjust(len(formula) + 1)
        formula = formula.ljust(len(formula) + 1)

        '''
        # replace all species and parameters by their unique metaid-id
        for iSorted in range(0, len(all_sorted)):
            if all_sorted[iSorted] in formula:
                formula = formula.replace(all_sorted[iSorted], all_metaid[iSorted])
        '''

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
                                _, b = list_of_categories[iCat].split(', ')
                                exp, _ = b.split(')', 1)
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
                                        else:
                                            if not 'pow(' in nominator:
                                                spec_list.append(1)
                                                print('Categorie: ' + str(1))  # 1
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                                if not all_spec[iSpecId] in nominator[nominator.find('pow(') + 4 : close_power_index + 1]:
                                                    spec_list.append(1)
                                                    print('Categorie: ' + str(1))  # 1
                                                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                                else:
                                                    _, b = nominator.split(', ')
                                                    exp, _ = b.split(')', 1)
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
                                    elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                        if not 'pow(' in denominator:
                                            spec_list.append(5)
                                            print('Categorie: ' + str(5))                                                   # 5
                                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                        else:
                                            close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                            if not all_spec[iSpecId] in nominator[nominator.find('pow(') + 4: close_power_index + 1]:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                _, b = denominator.split(', ')
                                                exp, _ = b.split(')', 1)
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
                                    elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                        spec_list.append(9)                                                                 # 9
                                        print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')


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
                                                    _, b = nominator.split(', ')
                                                    exp, _ = b.split(')', 1)
                                                    nominator = nominator[5: len(nominator) - 4]
                                                    list_of_categories4 = decomposition(nominator)
                                                    kinlaw = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                    if kinlaw == 1:
                                                        if exp == 2:
                                                            kinlaw = exp
                                                        else:
                                                            try:
                                                                int(exp)
                                                                kinlaw = 3
                                                            except:
                                                                kinlaw = 4
                                                    elif kinlaw == 2:
                                                        kinlaw = 3
                                                    elif kinlaw == 5:
                                                        if exp == 2:
                                                            kinlaw = 6
                                                        else:
                                                            try:
                                                                int(exp)
                                                                kinlaw = 7
                                                            except:
                                                                kinlaw = 8
                                                    elif kinlaw == 6:
                                                        kinlaw = 7
                                                    spec_list.append(kinlaw)
                                                    print('Species ' + all_spec[iSpecId] + ' had to go in depth!')
                                                else:
                                                    _, b = nominator.split(', ')
                                                    exp, _ = b.split(')', 1)
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
                                        elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                            if not 'pow(' + all_spec[iSpecId] in denominator:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                                if not all_spec[iSpecId] in nominator[
                                                                  nominator.find('pow(') + 4: close_power_index + 1]:
                                                    spec_list.append(5)
                                                    print('Categorie: ' + str(5))  # 5
                                                    print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                                else:
                                                    _, b = denominator.split(', ')
                                                    exp, _ = b.split(')', 1)
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
                                        elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                            spec_list.append(9)
                                            print('What to do with species ' + all_spec[iSpecId] + ' from depth1 ?')
                                    else:
                                        _, b = list_of_categories[iCat].split(', ')
                                        exp, _ = b.split(')', 1)
                                        nominator = list_of_categories[iCat][5: matching_index - 4]
                                        list_of_categories3 = decomposition(nominator)
                                        kinlaw = depth1(nominator, list_of_categories3, all_spec[iSpecId], sbml_file, iReact)
                                        if kinlaw == 1:
                                            if exp == 2:
                                                kinlaw = exp
                                            else:
                                                try:
                                                    int(exp)
                                                    kinlaw = 3
                                                except:
                                                    kinlaw = 4
                                        elif kinlaw == 2:
                                            kinlaw = 3
                                        elif kinlaw == 5:
                                            if exp == 2:
                                                kinlaw = 6
                                            else:
                                                try:
                                                    int(exp)
                                                    kinlaw = 7
                                                except:
                                                    kinlaw = 8
                                        elif kinlaw == 6:
                                            kinlaw = 7
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
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
                                                nominator = nominator[5: len(nominator) - 4]
                                                list_of_categories4 = decomposition(nominator)
                                                kinlaw = depth1(nominator, list_of_categories4, all_spec[iSpecId], sbml_file, iReact)
                                                if kinlaw == 1:
                                                    if exp == 2:
                                                        kinlaw = exp
                                                    else:
                                                        try:
                                                            int(exp)
                                                            kinlaw = 3
                                                        except:
                                                            kinlaw = 4
                                                elif kinlaw == 2:
                                                    kinlaw = 3
                                                elif kinlaw == 5:
                                                    if exp == 2:
                                                        kinlaw = 6
                                                    else:
                                                        try:
                                                            int(exp)
                                                            kinlaw = 7
                                                        except:
                                                            kinlaw = 8
                                                elif kinlaw == 6:
                                                    kinlaw = 7
                                                spec_list.append(kinlaw)
                                                print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                            else:
                                                _, b = nominator.split(', ')
                                                exp, _ = b.split(')', 1)
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
                                    elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                        if not 'pow(' + all_spec[iSpecId] in denominator:
                                            spec_list.append(5)
                                            print('Categorie: ' + str(5))                                                   # 5
                                            print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                        else:
                                            close_power_index = getIndex(nominator, nominator.find('pow(') + 4)
                                            if not all_spec[iSpecId] in nominator[nominator.find('pow(') + 4: close_power_index + 1]:
                                                spec_list.append(5)
                                                print('Categorie: ' + str(5))  # 5
                                                print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                            else:
                                                _, b = denominator.split(', ')
                                                exp, _ = b.split(')', 1)
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
                                    elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                        spec_list.append(9)
                                        print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')
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
                                            _, b = nominator.split(', ')
                                            exp, _ = b.split(')', 1)
                                            nominator = nominator[5: len(nominator) - 4]
                                            list_of_categories5 = decomposition(nominator)
                                            kinlaw = depth1(nominator, list_of_categories5, all_spec[iSpecId], sbml_file, iReact)
                                            if kinlaw == 1:
                                                if exp == 2:
                                                    kinlaw = exp
                                                else:
                                                    try:
                                                        int(exp)
                                                        kinlaw = 3
                                                    except:
                                                        kinlaw = 4
                                            elif kinlaw == 2:
                                                kinlaw = 3
                                            elif kinlaw == 5:
                                                if exp == 2:
                                                    kinlaw = 6
                                                else:
                                                    try:
                                                        int(exp)
                                                        kinlaw = 7
                                                    except:
                                                        kinlaw = 8
                                            elif kinlaw == 6:
                                                kinlaw = 7
                                            spec_list.append(kinlaw)
                                            print('Species ' + all_spec[iSpec] + ' had to go in depth!')
                                        else:
                                            _, b = nominator.split(', ')
                                            exp, _ = b.split(')', 1)
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
                                elif all_spec[iSpecId] not in nominator and all_spec[iSpecId] in denominator:
                                    if not 'pow(' in denominator:
                                        spec_list.append(5)
                                        print('Categorie: ' + str(5))  # 5
                                        print('Variable ' + all_spec[iSpecId] + ' is linear!')
                                    else:
                                        _, b = denominator.split(', ')
                                        exp, _ = b.split(')', 1)
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
                                elif all_spec[iSpecId] in nominator and all_spec[iSpecId] in denominator:
                                    spec_list.append(9)
                                    print('What to do with species ' + all_spec[iSpecId] + ' from ' + iModel + '_' + iFile + ' ?')

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


    # give total kinetic number from 0 - 9
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

    return total_kinetics