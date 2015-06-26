import os

# 0. delete the last transforms
cmd=('rm -rfv /Users/peterbehringer/MyTesting/ProjectWeek15/Data/Case15/Slicer4Registration/*')
os.system(cmd)

# 1. ProcessCase.py
cmd = ('python projectWeekExperiments.py '+str(15))
print ('about to run : '+cmd)
os.system(cmd)

# 2. ResampleCase.py
cmd = ('python projectWeekExperiments-ResampleCase.py '+str(15))
print ('about to run : '+cmd)
os.system(cmd)


