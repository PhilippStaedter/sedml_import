# execute simulation script with all SOLVER ALGORITHMS

######################################################################################
# very important: linSol, nonLinSolIter, solAlg must be their corresponding integers #
#                                                                                    #
# linSol:           Dense == 1  GMRES == 6  BiCGStab == 7   SPTFQMR == 8    KLU 00 9 #
# nonLinSolIter:    Functional == 1     Newton-type == 2                             #
# solAlg:           Adams == 1      BDF == 2                                         #
#                                                                                    #
######################################################################################

from SimAllSettings import *

# settings
atol = [1e-6, 1e-8, 1e-10, 1e-12]                   # add 2 - 4 different interesting tolerance combinations from study 'Tolerances'
rtol = [1e-6, 1e-8, 1e-10, 1e-12]
linSol = [1, 7, 8]                                  # add 2 - 3 different interesting linear solvers from study 'Linear Solvers'
solAlg = [1, 2]


for iSolAlg in range(0, len(solAlg)):
    for iLinSol in range(0, len(linSol)):
        for iToleranceGroup in range(0, len(atol)):
            simulate(atol[iToleranceGroup], rtol[iToleranceGroup], linSol[iLinSol], solAlg[iSolAlg])