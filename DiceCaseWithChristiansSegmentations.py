import os, argparse, string, re, sys, glob
from time import time

resamplingCmd = "/Applications/Slicer_5.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

def BFResample(reference,moving,tfm,output,interp='Linear'):
  CMD = resamplingCmd+' --referenceVolume '+reference+' --inputVolume '+moving+' --outputVolume '+output+' --warpTransform '+tfm
  CMD = CMD + ' --interpolationMode '+interp
  ret = os.system(CMD)
  if ret:
    exit()

def GetDice(reference,moving,result,case):

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
    print 'filter executed'
  value=measureFilter.GetDiceCoefficient()

  # write in log file
  f = open(result, 'w')
  f.write("\n"+'case: '+str(case)+','+str(value))

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('case',help='case to be processed')

args = parser.parse_args()

case = args.case

SegDir = '/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/Case'+case+'-ManualSegmentations'
TempDir='/Users/peterbehringer/MyStudies/TempDir'
IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'

# 1. run preop/intraop registration

# 2. for each needle image, run intraop/intraop registration using different
# registration modes

#   list all needle image ids first
needleImageIds = []
if 1:
  needleImages = glob.glob(IntraDir+'/[0-9]*nrrd')
  for ni in needleImages:
    fname = string.split(ni,'/')[-1]
    #if string.find(fname,'TG') == -1:
    # keep only those images that look like 10.nrrd
    if re.match('\d+\.nrrd',fname):
      needleImageIds.append(int(string.split(fname,'.')[0]))
  needleImageIds.sort()


lastId = str(needleImageIds[-1])
# moving image/mask will always be the same
IdentityTfm='/Users/peterbehringer/MyStudies/InitialTransforms/Identity.h5'
movingMask = SegDir+'/CoverProstate-label.nrrd'
fixedMask = SegDir+'/'+lastId+'-label.nrrd'
Tfm1='/Users/peterbehringer/MyStudies/Data/Case'+case+'/Slicer4registration/'+lastId+'-IntraIntra-BSpline-Attempt2.h5'

if not os.path.isfile(Tfm1):
  Tfm1='/Users/peterbehringer/MyStudies/Data/Case'+case+'/Slicer4registration/'+lastId+'-IntraIntra-BSpline-Attempt1.h5'

before = TempDir+'/Case'+case+'-'+lastId+'-before.nrrd'
after = TempDir+'/Case'+case+'-'+lastId+'-after.nrrd'

BFResample(fixedMask, movingMask, IdentityTfm, before, interp='NearestNeighbor')

BFResample(fixedMask, movingMask, Tfm1, after, interp='NearestNeighbor')

diceBefore = TempDir+'/Case'+case+'_dice_before.log'
diceAfter = TempDir+'/Case'+case+'_dice_after.log'

if not os.path.isfile(diceBefore):
  cmd=('touch '+diceBefore)
  os.system(cmd)

if not os.path.isfile(diceAfter):
  cmd=('touch '+diceAfter)
  os.system(cmd)

GetDice(fixedMask, before, diceBefore,case)

GetDice(fixedMask, after, diceAfter,case)
