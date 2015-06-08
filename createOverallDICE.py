import os,argparse

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('lowerCaseNumber',help='start with this case')
parser.add_argument('upperCaseNumber',help='end with this case')
args = parser.parse_args()
lowerCaseNumber = int(args.lowerCaseNumber)
upperCaseNumber = int(args.upperCaseNumber)

summaryBefore=[]
summaryAfter=[]


for case in range(lowerCaseNumber,upperCaseNumber):
    if case==14:
        continue
    # dice before
    pathToFile=('/Users/peterbehringer/MyStudies/TempDir/Case'+str(case)+'_dice_before.log')
    f=open(pathToFile,'r')
    for line in f:
      last=line
    splitted=last.split(',')
    summaryBefore.append(splitted)

    # dice after
    pathToFile=('/Users/peterbehringer/MyStudies/TempDir/Case'+str(case)+'_dice_after.log')
    f=open(pathToFile,'r')
    for line in f:
      last=line
    splitted=last.split(',')
    summaryAfter.append(splitted)

print summaryBefore
print summaryAfter

avg_dice_before=0
avg_dice_after=0

for i in range(0,len(summaryBefore)):
  avg_dice_before =avg_dice_before+float(summaryBefore[i][1])

for i in range(0,len(summaryAfter)):
  avg_dice_after =avg_dice_after+float(summaryAfter[i][1])

avg_dice_before=avg_dice_before/len(summaryBefore)
avg_dice_after=avg_dice_after/len(summaryAfter)


print 'avg_dice_before : '+str(avg_dice_before)
print 'avg_dice_after : '+str(avg_dice_after)

cmd=('touch /Users/peterbehringer/MyStudies/Verification/OverallSummary_DICE.txt')
print ('about to run '+cmd)
os.system(cmd)
f = open('/Users/peterbehringer/MyStudies/Verification/OverallSummary_DICE.txt', 'w')
f.write('Overall Summary created, showing [avg_dice_before,avg_dice_after')
f.write("\n"+str(avg_dice_before)+', '+str(avg_dice_after))

diceCoeffBefore=[]
for i in range(0,len(summaryBefore)):
  print summaryBefore[i][1]
  diceCoeffBefore.append(summaryBefore[i][1])

print 'diceCoeffBefore'
print diceCoeffBefore

diceCoeffAfter=[]
for i in range(0,len(summaryAfter)):
  print summaryAfter[i][1]
  diceCoeffAfter.append(summaryAfter[i][1])

print 'diceCoeffAfter'
print diceCoeffAfter

# create the plot
from pylab import *

fig=plt.figure()
rect=fig.patch
rect.set_facecolor('white')
ax1= fig.add_subplot(1,1,1)
x=[0,1,2]
y=[0,1,2]

plt.plot(diceCoeffBefore,diceCoeffAfter,'ko',x,y,'b--')

# plt.title('DICE Coefficients')
ax1.set_xlabel('DICE before registration',labelpad=20)
ax1.set_ylabel('DICE after registration',labelpad=20)
plt.axis([0,1,0,1])

plt.show()