import os, argparse, string, re, sys, glob
from time import time

resamplingCmd = "/Applications/Slicer_5.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

def BFResample(reference,moving,tfm,output,interp='Linear'):
  CMD = resamplingCmd+' --referenceVolume '+reference+' --inputVolume '+moving+' --outputVolume '+output+' --warpTransform '+tfm
  CMD = CMD + ' --interpolationMode '+interp
  ret = os.system(CMD)
  if ret:
    exit()

def IsBSplineTfmValid(tfm):
  import h5py
  f=h5py.File(tfm,'r')
  transformType=f["TransformGroup/2/TransformType"]
  type=transformType[:]
  typeStr=str(type)
  if 'BSplineTransform' in typeStr:
    return True

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('case',help='case to be processed')

args = parser.parse_args()

case = args.case

IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'
ResDir='/Users/peterbehringer/MyTesting/ProjectWeek15/Verification/Case'+case
TempDir='/Users/peterbehringer/MyTesting/ProjectWeek15/Data/Case'+case+'TempDir'
RegDir='/Users/peterbehringer/MyTesting/ProjectWeek15/Data/Case'+case+'/Slicer4registration'

try:
  os.mkdir(ResDir)
except:
  pass


#   list all needle image ids first

needleImageIds = []
needleImages = glob.glob(IntraDir+'/[0-9]*nrrd')
for ni in needleImages:
  fname = string.split(ni,'/')[-1]
  #if string.find(fname,'TG') == -1:
  # keep only those images that look like 10.nrrd
  if re.match('\d+\.nrrd',fname):
    needleImageIds.append(int(string.split(fname,'.')[0]))
needleImageIds.sort()

#needleImageIds=[18]

print str(needleImageIds)

# moving image/mask will always be the same
movingImage = IntraDir+'/CoverProstate.nrrd'

for nid in needleImageIds:
  bsplineTfm=None

  nidStr=str(nid)

  fixedImage = IntraDir+'/'+nidStr+'.nrrd'

  # check if there is a matching TG
  bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt1.h5'

  #bsplineTfm='/Users/peterbehringer/MyTesting/ProjectWeek15/Data/Case15/Slicer4Registration/15-IntraIntra-Rigid-Attempt1.h5'

  print str(bsplineTfm)
  if not os.path.isfile(bsplineTfm):
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'
  if not os.path.isfile(bsplineTfm):
    print 'Failed to find ANY transform!'
    exit()

  resampled = ResDir+'/'+nidStr+'-regular_stepSize_bigger_mask_automated_RETRY_2.nrrd'
  """
  if not IsBSplineTfmValid(bsplineTfm):
    print 'BSpline transform is not valid! Will skip needle image ',nid
    continue
  """
  BFResample(reference=fixedImage,moving=movingImage,tfm=bsplineTfm,output=resampled)
