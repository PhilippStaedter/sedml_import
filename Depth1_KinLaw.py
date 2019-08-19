# determine kinetic law after in depth1 analysis of special cases


def depthKineticLaw(kinlaw, exp, sbml_file, iReact):

    group1 = [1,2,3,4]
    group2 = [5,6,7,8]

    if kinlaw in group1:
        counter = 0
    elif kinlaw in group2:
        counter = 4

    # 0
    if kinlaw == 0:
        kinlaw = 0
    # 9
    elif kinlaw == 9:
        kinlaw = 9

    # 1 && 5
    elif kinlaw == 1 + counter:  # only 1-4 because if A only in denominator no cases
        try:
            if exp == str(2) + ' ':
                kinlaw = 2 + counter
            else:
                float(exp)
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    kinlaw = 4 + counter
        except:
            # the exponent is most likely a parameter with some numerical value
            num_par = sbml_file.getModel().getReaction(iReact).getKineticLaw().getNumParameters()
            all_parameters = []
            for iPar in range(0, num_par):
                all_parameters.append(
                    sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(iPar).getId() + ' ')
            for iPar in range(0, len(all_parameters)):
                if exp == all_parameters[iPar]:
                    if int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) == sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue():
                        exp = str(int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue())) + ' '
                        break
                    else:
                        exp = str(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) + ' '
                        break
            if exp == str(1) + ' ':
                kinlaw = 1 + counter
            elif exp == str(2) + ' ':
                kinlaw = 2 + counter
            else:
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    kinlaw = 4 + counter
    # 2 && 6
    elif kinlaw == 2 + counter:
        try:
            if exp == str(2) + ' ':
                kinlaw = 3 + counter
            else:
                float(exp)
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    if int(exp.split('.')[1]) == 5:                                                                     # if exp == 1.5 => exp * kinlaw = 3 => category 3
                        kinlaw = 3 + counter
                    else:
                        kinlaw = 4 + counter
        except:
            # the exponent is most likely a parameter with some numerical value
            num_par = sbml_file.getModel().getReaction(iReact).getKineticLaw().getNumParameters()
            all_parameters = []
            for iPar in range(0, num_par):
                all_parameters.append(
                    sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(iPar).getId() + ' ')
            for iPar in range(0, len(all_parameters)):
                if exp == all_parameters[iPar]:
                    if int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) == sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue():
                        exp = str(int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue())) + ' '
                        break
                    else:
                        exp = str(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) + ' '
                        break
            if exp == str(1) + ' ':
                kinlaw = 2 + counter
            elif exp == str(2) + ' ':
                kinlaw = 3 + counter
            else:
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    if int(exp.split('.')[1]) == 5:  # if exp == 1.5 => exp * kinlaw = 3 => category 3
                        kinlaw = 3 + counter
                    else:
                        kinlaw = 4 + counter
    # 3 && 7
    elif kinlaw == 3 + counter:
        try:
            if exp == str(2) + ' ':
                kinlaw = 3 + counter
            else:
                float(exp)
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    kinlaw = 4 + counter
        except:
            # the exponent is most likely a parameter with some numerical value
            num_par = sbml_file.getModel().getReaction(iReact).getKineticLaw().getNumParameters()
            all_parameters = []
            for iPar in range(0, num_par):
                all_parameters.append(
                    sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(iPar).getId() + ' ')
            for iPar in range(0, len(all_parameters)):
                if exp == all_parameters[iPar]:
                    if int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) == sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue():
                        exp = str(int(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue())) + ' '
                        break
                    else:
                        exp = str(sbml_file.getModel().getReaction(iReact).getKineticLaw().getParameter(
                            iPar).getValue()) + ' '
                        break
            if exp == str(1) + ' ':
                kinlaw = 3 + counter
            elif exp == str(2) + ' ':
                kinlaw = 3 + counter
            else:
                try:
                    int(exp)
                    kinlaw = 3 + counter
                except:
                    kinlaw = 4 + counter
    # 4 && 8
    elif kinlaw == 4 + counter:
        kinlaw = 4 + counter


    return kinlaw
