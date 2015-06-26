import os, argparse, string, re, sys, glob
from time import time

def GetDice(reference,moving,case):

  import SimpleITK as sitk
  image_reference=sitk.ReadImage(reference)
  image_input=sitk.ReadImage(moving)

  # make sure both labels have the same value
  threshold=sitk.BinaryThresholdImageFilter()
  threshold.SetUpperThreshold(100)
  threshold.SetLowerThreshold(1)
  threshold.SetInsideValue(1)
  image_reference=threshold.Execute(image_reference)
  image_input=threshold.Execute(image_input)

  measureFilter=sitk.LabelOverlapMeasuresImageFilter()
  if measureFilter.Execute(image_reference,image_input):
   value=measureFilter.GetDiceCoefficient()

  print value


#compare two rater segmentations

for case in range(11,36):

    SegDir = '/Users/peterbehringer/MyStudies/Data/Case'+str(case)+'/IntraopImages/CoverProstate-TG.nrrd'
    SegDir2= '/Users/peterbehringer/MyStudies/Beginner_Segmentations/Case'+str(case)+'/CoverProstate-label.nrrd'

    GetDice(SegDir,SegDir2,case)
