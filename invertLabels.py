import SimpleITK as sitk
import sys, os, glob, string

for case in range(11,51):
  #case = sys.argv[1]

  inputDir= ('/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/Case'+str(case)+'-ManualSegmentations')

  inputLabelNames =os.listdir(inputDir)
  # print inputLabelNames

  for name in range(len(inputLabelNames)):
    if "-label.nrrd" in os.listdir(inputDir)[name]:
      if not "Prostate" in os.listdir(inputDir)[name]:
        inputLabelName = os.listdir(inputDir)[name]

  print 'inputLabelName of case '+str(case)+' '+str(inputLabelName)

  labelname=inputLabelName[:len(inputLabelName)-5]
  print 'labelname : '+labelname
  outputLabelName = labelname+'-inverted.nrrd'
  print 'outputLabelName : '+outputLabelName
  outputDir=inputDir+'/'+outputLabelName

  IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'
  outputLabelName = labelname+'-NONTG.nrrd'
  outputDir=IntraDir+'/'+outputLabelName

  # TODO: maybe save directly in IntraopDir as nidID-NONTG.nrrd

  inputLabel = sitk.ReadImage(inputDir+'/'+inputLabelName)

  changeFilter = sitk.ChangeLabelImageFilter()
  changeMap = sitk.DoubleDoubleMap()
  
  changeMap[0] = 1
  changeMap[1] = 0
  
  changedLabel = changeFilter.Execute(inputLabel, changeMap)
  sitk.WriteImage(changedLabel, outputDir, True)

  print(str(case)+' done')
