from pylab import *
import os, sys, string, glob, re, numpy

allTimesSlicer4 = []
allTimesSlicer3 = []
allTimesArrSlicer3 = numpy.array([])
allTimesArrSlicer4 = numpy.array([])

caseTimes=[]

for c in range(11,36):
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
  print 'LEN TIMES SLICER4'
  print str(len(timesSlicer4))
  allTimesSlicer4.append(timesSlicer4)
  allTimesArrSlicer4 = numpy.append(allTimesArrSlicer4, timesSlicer4)


for c in range(11,36):
  regTimeLog = open('/Users/peterbehringer/MyStudies/Data/Case'+str(c)+'/Slicer3registration/'+str(c)+'_registration_times.log','r')
  #regTimeLog = open('/Users/peterbehringer/MyStudies/Data/Case'+str(c)+'/Slicer4registration/CH-TG/'+str(c)+'_registration_times.log','r')
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
  print 'LEN TIMES SLICER3'
  print str(len(timesSlicer3))
  allTimesSlicer3.append(timesSlicer3)
  allTimesArrSlicer3 = numpy.append(allTimesArrSlicer3, timesSlicer3)

print 'SLICER 4: '
print 'Total number of registrations: ',len(allTimesArrSlicer4)
print 'Mean: ',numpy.mean(allTimesArrSlicer4)
print 'Max: ',numpy.max(allTimesArrSlicer4)
print 'Min: ',numpy.min(allTimesArrSlicer4)
print 'STD: ',numpy.std(allTimesArrSlicer4)

print 'SLICER 3: '
print 'Total number of registrations: ',len(allTimesArrSlicer3)
print 'Mean: ',numpy.mean(allTimesArrSlicer3)
print 'Max: ',numpy.max(allTimesArrSlicer3)
print 'Min: ',numpy.min(allTimesArrSlicer3)
print 'STD: ',numpy.std(allTimesArrSlicer3)

averagesSlicer4=[]
avg=0

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
plt.xlabel('computation time ITK3',labelpad=15)
plt.ylabel('computation time ITK4',labelpad=15)
#plt.axis([0,1,0,1])

plt.show()

print '*********'
print allTimesSlicer4


fig=plt.figure()
rect=fig.patch
rect.set_facecolor('white')
ax1=fig.add_subplot(111)
bp=boxplot(allTimesSlicer4)

xlabel('case ID')
ylabel('registration time, sec')

locs, labels = plt.xticks()
plt.xticks(locs, numpy.arange(11, 36))


show()


