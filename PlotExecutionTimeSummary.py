from pylab import *
import os, sys, string, glob, re, numpy

allTimesSlicer4 = []
allTimesSlicer3 = []
allTimesArr = numpy.array([])

caseTimes=[]

for c in range(11,35):
  regTimeLog = open('/Users/peterbehringer/MyStudies/Data/Case'+str(c)+'/Slicer4registration/'+str(c)+'_registration_times.log','r')
  log = regTimeLog.readline()
  items = string.split(log, ';')
  print items
  # format for the log entry: case;nid;attempt;endTime-startTime;
  
  timesSlicer4 = []
  # print items
  for i in range(len(items)/4):
    timesSlicer4.append(float(items[i*4+3]))


  print 'TIMES SLICER4'
  print timesSlicer4
  print 'LAENGE TIMES SLICER4'
  print str(len(timesSlicer4))
  allTimesSlicer4.append(timesSlicer4)
  allTimesArr = numpy.append(allTimesArr, timesSlicer4)


for c in range(11,35):
  regTimeLog = open('/Users/peterbehringer/MyStudies/Data/Case'+str(c)+'/Slicer3registration/'+str(c)+'_registration_times.log','r')
  log = regTimeLog.readline()
  items = string.split(log, ';')
  print items
  # format for the log entry: case;nid;attempt;endTime-startTime;

  timesSlicer3 = []
  # print items
  for i in range(len(items)/4):
    timesSlicer3.append(float(items[i*4+3]))


  print 'TIMES SLICER3'
  print timesSlicer3
  print 'LAENGE TIMES SLICER3'
  print str(len(timesSlicer3))
  allTimesSlicer3.append(timesSlicer3)
  allTimesArr = numpy.append(allTimesArr, timesSlicer3)

print 'Total number of registrations: ',len(allTimesArr)
print 'Mean: ',numpy.mean(allTimesArr)
print 'Max: ',numpy.max(allTimesArr)
print 'Min: ',numpy.min(allTimesArr)
print 'STD: ',numpy.std(allTimesArr)

averagesSlicer4=[]
avg=0

print 'meine freundin ist suess'

for i in range(len(allTimesSlicer4)):
  #print 'listentry['+str(i)+'] : '+str(allTimesSlicer4[i])
  for time in range(len(allTimesSlicer4[i])):
    print allTimesSlicer4[i][time]
    avg=avg+float(allTimesSlicer4[i][time])
  avg=avg/float(len(allTimesSlicer4[i]))
  #print 'avg for listentry '+str(i)+' = '+str(avg)
  averagesSlicer4.append(avg)

averagesSlicer3=[]
avg=0
for i in range(len(allTimesSlicer3)):
  #print 'listentry['+str(i)+'] : '+str(allTimesSlicer3[i])
  for time in range(len(allTimesSlicer3[i])):
    #print allTimesSlicer3[i][time]
    avg=avg+float(allTimesSlicer3[i][time])
  avg=avg/float(len(allTimesSlicer3[i]))
  # print 'avg for listentry '+str(i)+' = '+str(avg)
  averagesSlicer3.append(avg)


print 'meine freundin ist immer noch suess'

print 'averages Slicer 4'
print averagesSlicer4


print 'averages Slicer 3'
print averagesSlicer3

# create the plot
from pylab import *

fig=plt.figure()
rect=fig.patch
rect.set_facecolor('white')
# ax1= fig.add_subplot(1,1,1)
x=[0,50]
y=[0,50]

# plt.plot(diceCoeffBefore,diceCoeffAfter,'ko',x,y,'b--')
plt.plot(averagesSlicer3, averagesSlicer4,'ko',mfc='none',color="blue")
plt.plot(x,y,'k--')

# plt.title('DICE Coefficients')
plt.xlabel('timesSlicer3',labelpad=15)
plt.ylabel('timesSlicer4',labelpad=15)
#plt.axis([0,1,0,1])

plt.show()

"""

fig=plt.figure()
rect=fig.patch
rect.set_facecolor('white')
ax1=fig.add_subplot(111)
bp=boxplot(allTimes)
setp(range(11,12))
xlabel('case ID')
ylabel('registration time, sec')
show()
"""

