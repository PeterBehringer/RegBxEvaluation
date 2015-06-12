import os

lowercaseNumber=11
upperCaseNumber=35


for case in range(lowercaseNumber,upperCaseNumber+1):

    # 2. ResampleCase.py
    cmd = ('python ResampleCaseSlicer3.py '+str(case))
    print ('about to run : '+cmd)
    #os.system(cmd)

    # 7. DiceCase.py
    cmd = ('python DiceCaseSlicer3.py '+str(case))
    print ('about to run : '+cmd)
    os.system(cmd)

# 7. DiceCase.py
cmd = ('python createOverallDICESlicer3.py '+str(lowercaseNumber)+' '+str(upperCaseNumber+1))
print ('about to run : '+cmd)
os.system(cmd)
