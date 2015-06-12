#
# This is a metaScript to process a whole series of cases with all necessary steps
#
# You'll have to install the following packages:
# - python pandas package to use h5py
# - simpleITK as package for DICE-computation
# - binary: BRAINSConstellationLandmarksTransform for transforming the fiducials
#
#
# FOR ALL PROSTATE CASES do
# 1. ProcessCase.py
# 2. ResampleCase.py
# 3. makeConfig.py
# 4. load Config within Slicer VisAIRe, make snapshots
# 5. makeGIFs.py
# 6. PlotExecutionTimeSummary.py
# 7. DiceCase.py
# 8. transformFiducials.py (we are transforming only the centroids right now)
# 9. MakeFiducialSummaryTable
#
# THEN FOR ALL CASES TOGETHER DO:
# 10. createOverallDICE.py
# 11. createOverallFiducialSummary.py

import os

# ________________________________________________________________________________________________________________ #
# PARAMETER YOU NEED TO SET:

lowercaseNumber = 11
upperCaseNumber = 36


# ________________________________________________________________________________________________________________ #

for case in range(lowercaseNumber,upperCaseNumber+1,1):
    # 1. ProcessCase.py
    cmd = ('python ProcessCaseWithAffine_CH-TG.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 2. ResampleCase.py
    cmd = ('python ResampleCase_CH-TG.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 3. MakeConfig.py
    cmd = ('python MakeConfig_CH-TG.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 7. DiceCase.py
    cmd = ('python DiceCase_CH-TG.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    print ('done with case '+str(case))

cmd = ('python createOverallFiducialSummary.py '+str(lowercaseNumber)+' '+str(upperCaseNumber))
print ('about to run : '+cmd)
os.system(cmd)

cmd = ('python createOverallDICE.py '+str(lowercaseNumber)+' '+str(upperCaseNumber))
print ('about to run : '+cmd)
os.system(cmd)

cmd = ('python PlotExecutionTimeSummary.py '+str(lowercaseNumber)+' '+str(upperCaseNumber))
print ('about to run : '+cmd)
os.system(cmd)