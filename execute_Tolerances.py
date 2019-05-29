# execute simulation script with all TOLERANCE combinations

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
atol = [1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16]
rtol = [1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-16]
linSol = 9
solAlg = 2


for iAtol in range(0, len(atol)):
    for iRtol in range(0, len(rtol)):
        simulate(atol[iAtol], rtol[iRtol], linSol, solAlg)