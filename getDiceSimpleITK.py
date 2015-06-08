import SimpleITK as sitk

def getDice(reference,input):

  image_reference=sitk.ReadImage(reference)
  image_input=sitk.ReadImage(input)

  # make sure both labels have the same value
  threshold=sitk.BinaryThresholdImageFilter()
  threshold.SetUpperThreshold(100)
  threshold.SetLowerThreshold(1)
  threshold.SetInsideValue(1)
  image_reference=threshold.Execute(image_reference)
  image_input=threshold.Execute(image_input)

  measureFilter=sitk.LabelOverlapMeasuresImageFilter()
  if measureFilter.Execute(image_reference,image_input):
    print 'filter executed'
  value=measureFilter.GetDiceCoefficient()

  return value

print "starting here"

seg1='/Users/peterbehringer/Desktop/label1.nrrd'
seg2='/Users/peterbehringer/Desktop/label2.nrrd'
seg3='/Users/peterbehringer/Desktop/label3.nrrd'

value=getDice(seg1,seg2)

print ('value = '+str(value))

