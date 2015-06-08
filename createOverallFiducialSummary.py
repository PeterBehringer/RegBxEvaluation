import os,argparse

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('lowerCaseNumber',help='start with this case')
parser.add_argument('upperCaseNumber',help='end with this case')
args = parser.parse_args()
lowerCaseNumber = int(args.lowerCaseNumber)
upperCaseNumber = int(args.upperCaseNumber)

summary=[]
for case in range(lowerCaseNumber,upperCaseNumber):
    if case==14:
        continue
    pathToFile=('/Users/peterbehringer/MyStudies/Verification/Case'+str(case)+'/summary_glandMotion.txt')
    f=open(pathToFile,'r')
    for line in f:
      last=line
    splitted=last.split(',')
    summary.append(splitted)

print summary

avgX=0
avgY=0
avgZ=0

for i in range(0,len(summary)):
  avgX =avgX+float(summary[i][1])
  avgY =avgY+float(summary[i][2])
  print ('avgY = '+str(avgY))
  print ('case = '+str(i))
  avgZ =avgZ+float(summary[i][3])

avgX=avgX/len(summary)
avgY=avgY/len(summary)
avgZ=avgZ/len(summary)

print avgX
print avgY
print avgZ

cmd=('touch /Users/peterbehringer/MyStudies/Verification/OverallSummary_glandMotion.txt')
print ('about to run '+cmd)
os.system(cmd)
f = open('/Users/peterbehringer/MyStudies/Verification/OverallSummary_glandMotion.txt', 'w')
f.write('Overall Summary created, showing [lastcase,averageMovement_x, averageMovement_y, averageMovement_z ')
f.write("\n"+str(case)+', '+str(avgX)+', '+str(avgY) + ', ' +str(avgZ))
