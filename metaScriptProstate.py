#
# This is a metaScript to process a whole series of cases with all necessary steps
#
# You'll have to install the following packages:
# - python pandas package to use h5py
# - simpleITK as package for DICE-computation
# - binary: BRAINSConstellationLandmarksTransform for transforming the fiducials
#
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

SegDir = '/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/'
# expects file(s) : 'Case'+case+'-ManualSegmentations'

RegDir='/Users/peterbehringer/MyStudies/Data/'
# expects file(s) : Case'+case+'/Slicer4registration'

IntraDir = '/Users/peterbehringer/MyStudies/Data/'
# expects file(s) : Case'+case+'/IntraopImages'

ResDir='/Users/peterbehringer/MyStudies/Verification/'
# expects file(s) : Case'+case

TempDir='/Users/peterbehringer/MyStudies/TempDir'

# ________________________________________________________________________________________________________________ #


for case in range(lowercaseNumber,upperCaseNumber,1):

    if case == 14:
        continue


    # 1. ProcessCase.py
    cmd = ('python ProcessCase.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)


    # 2. ResampleCase.py
    cmd = ('python ResampleCase.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 3. MakeConfig.py
    cmd = ('python MakeConfig.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 6. PlotExecutionTimeSummary.py
    cmd = ('python PlotExecutionTimeSummary.py '+str(case))
    print ('about to run : '+cmd)
    # os.system(cmd)

    # 7. DiceCase.py
    cmd = ('python DiceCase.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 8. transformFiducials.py
    cmd = ('python TransformFiducials.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    # 8. MakeFiducialSummaryTable.py
    cmd = ('python MakeFiducialsSummaryTable.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

    print ('done with case '+str(case))

cmd = ('python createOverallFiducialSummary.py '+str(lowercaseNumber)+' '+str(upperCaseNumber))
print ('about to run : '+cmd)
os.system(cmd)

cmd = ('python createOverallDICE.py '+str(lowercaseNumber)+' '+str(upperCaseNumber))
print ('about to run : '+cmd)
os.system(cmd)