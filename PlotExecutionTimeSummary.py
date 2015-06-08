from pylab import *
import os, sys, string, glob, re, numpy

allTimes = []
allTimesArr = numpy.array([])

for c in range(11,12):
  regTimeLog = open('/Users/peterbehringer/MyStudies/Data/Case'+str(c)+'/Slicer4registration/'+str(c)+'_registration_times.log','r')
  log = regTimeLog.readline()
  items = string.split(log, ';')
  
  # format for the log entry: case;nid;attempt;endTime-startTime;
  
  times = []
  print items
  for i in range(len(items)/4):
    times.append(float(items[i*4+3]))

  allTimes.append(times)
  allTimesArr = numpy.append(allTimesArr, times)


print 'Total number of registrations: ',len(allTimesArr)
print 'Mean: ',numpy.mean(allTimesArr)
print 'Max: ',numpy.max(allTimesArr)
print 'Min: ',numpy.min(allTimesArr)
print 'STD: ',numpy.std(allTimesArr)

fig=figure()
ax1=fig.add_subplot(111)
bp=boxplot(allTimes)
setp(range(11,12))
xlabel('case ID')
ylabel('registration time, sec')
show()


