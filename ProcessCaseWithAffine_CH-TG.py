import os, argparse, string, re, sys, glob
from time import time

registrationCmd = "/Applications/Slicer_5.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSFit"
resamplingCmd = "/Applications/Slicer_5.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

def BFRegister(fixed=None,moving=None,fixedMask=None,movingMask=None,rigidTfm=None,affineTfm=None,bsplineTfm=None,initializer=None,log=None,initTfm=None,initialTfm=None):
  CMD=registrationCmd+" --fixedVolume "+fixed+" --movingVolume "+moving+" --numberOfThreads -1 --maskProcessingMode ROI"

  if fixedMask:
    CMD = CMD+" --fixedBinaryVolume "+fixedMask
  if movingMask:
    CMD = CMD+" --movingBinaryVolume "+movingMask
  if initializer:
    CMD = CMD+" "+initializer
  if initTfm:
    CMD = CMD+' --initialTransform '+initTfm
  if bsplineTfm:
    print ('now went into second if case')
    CMD = CMD+" --useROIBSpline --useBSpline --splineGridSize 3,3,3 --outputTransform "+bsplineTfm+" --useScaleVersor3D --useScaleSkewVersor3D --numberOfIterations 1500 --outputVolumePixelType float --backgroundFillValue 0 --interpolationMode Linear --minimumStepLength 0.005 --translationScale 1000 --reproportionScale 1 --skewScale 1 --fixedVolumeTimeIndex 0 --movingVolumeTimeIndex 0 --medianFilterSize 0,0,0 --ROIAutoDilateSize 0 --relaxationFactor 0.5 --maximumStepLength 0.2 --failureExitCode -1 --costFunctionConvergenceFactor 1.00E+09 --projectedGradientTolerance 1.00E-05 --maxBSplineDisplacement 0 --maximumNumberOfEvaluations 900 --maximumNumberOfCorrections 25  --removeIntensityOutliers 0 --ROIAutoClosingSize 9"
  if rigidTfm:
    CMD = CMD+" --useRigid"
  if rigidTfm and not bsplineTfm:
    CMD = CMD+" --outputTransform "+rigidTfm
  if affineTfm:
    CMD = CMD+" --useAffine --outputTransform "+affineTfm
  if fixedMask and movingMask and bsplineTfm:
    # B SPLINE TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for bspline')
    CMD = CMD +' --samplingPercentage 0.002 --maskInferiorCutOffFromCenter 1000 --numberOfHistogramBins 50 --numberOfMatchPoints 10 --metricSamplingStrategy Random --costMetric MMI'
  if fixedMask and movingMask and rigidTfm and not bsplineTfm:
    # RIGID TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for rigid')
  if fixedMask and movingMask and affineTfm and not bsplineTfm:
    # AFFINE TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for affine')
  if initialTfm and not initializer:
    CMD = CMD+' --initialTransform '+initialTfm

  print "About to run ",CMD

  if log:
    CMD = CMD+" | tee "+log

  ret = os.system(CMD)
  if ret:
    exit()

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
parser.add_argument('--needle',help='needle confirmation image to register')

args = parser.parse_args()

case = args.case
needleReq = args.needle

IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'
RegDir='/Users/peterbehringer/MyStudies/Data/Case'+case+'/Slicer4registration/CH-TG'
TempDir='/Users/peterbehringer/MyStudies/TempDir/CH-TG'
BeginnerSegDir='/Users/peterbehringer/MyStudies/Beginner_Segmentations/Case'+case+'/'
try:
  os.mkdir(RegDir)
except:
  pass

try:
  os.mkdir(TempDir)
except:
  pass

# 1. run preop/intraop registration

# 2. for each needle image, run intraop/intraop registration using different
# registration modes

#   list all needle image ids first
needleImageIds = []
if not needleReq:
  needleImages = glob.glob(IntraDir+'/[0-9]*nrrd')
  for ni in needleImages:
    fname = string.split(ni,'/')[-1]
    #if string.find(fname,'TG') == -1:
    # keep only those images that look like 10.nrrd
    if re.match('\d+\.nrrd',fname):
      needleImageIds.append(int(string.split(fname,'.')[0]))
  needleImageIds.sort()
else:
  needleImageIds = [int(needleReq)]

print needleImageIds

# moving image/mask will always be the same
movingImage = IntraDir+'/CoverProstate.nrrd'
movingMask = BeginnerSegDir+'/CoverProstate-label.nrrd'

latestRigidTfm = '/Users/peterbehringer/MyStudies/InitialTransforms/Identity.h5'
latestMovingMask = movingMask

# try to read the registration log
regTimesLog = open(RegDir+'/'+case+'_registration_times.log','a+')

for nid in needleImageIds:
  success = False
  rigidTfm = None
  affineTfm = None
  bsplineTfm = None
  attempt = ''

  nidStr=str(nid)

  fixedImage = IntraDir+'/'+nidStr+'.nrrd'

  log = RegDir+'/'+nidStr+'_registration.log'

  # check if there is a matching TG
  fixedMask = IntraDir+'/'+nidStr+'-TG.nrrd'

  if not os.path.isfile(fixedMask):
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt1.h5'
    rigidTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt1.h5'
    affineTfm = RegDir+'/'+nidStr+'-IntraIntra-Affine-Attempt1.h5'
    fixedMask = TempDir+'/'+str(case)+'_'+nidStr+'-Resampled-'+string.split(latestMovingMask,'/')[-1]
    print ('DEBUG: FIXED IMAGE')
    print fixedImage
    print ('DEBUG: LATEST MOVING MASK')
    print latestMovingMask
    print ('DEBUG: LATEST RIGID TFM')
    print latestRigidTfm
    print ('DEBUG: FIXED MASK')
    print fixedMask
    BFResample(reference=fixedImage,moving=latestMovingMask,tfm=latestRigidTfm,output=fixedMask,interp='NearestNeighbor')
    # since we have only one mask, we cannot use a smarter initialization procedure
    startTime = time()
    # rigid
    BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log,initialTfm=latestRigidTfm)
    # affine
    BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,affineTfm=affineTfm,initTfm=rigidTfm,log=log)
    # bspline
    BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,bsplineTfm=bsplineTfm,log=log,initialTfm=affineTfm)
    print 'latest BSpline transform path in not else case: '+str(bsplineTfm)

    endTime = time()
    attempt='Attempt1'
  else:
    print 'ENTERED MASK EXIST CASE'
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'
    rigidTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt2.h5'
    affineTfm = RegDir+'/'+nidStr+'-IntraIntra-Affine-Attempt2.h5'
    initTfm = RegDir+'/'+nidStr+'-IntraIntra-Init-Attempt2.h5'
    startTime = time()
    # rigid
    BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log)
    # affine
    BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,affineTfm=affineTfm,log=log)
    # bspline
    print 'latest BSpline transform path in else case BEFORE RUNNING the BSPLINE: '+str(bsplineTfm)
    BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,bsplineTfm=bsplineTfm,log=log)
    # BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,rigidTfm=rigidTfm,bsplineTfm=bsplineTfm,log=log,initTfm=initTfm)
    print 'latest BSpline transform path in else case: '+str(bsplineTfm)


    endTime = time()
    attempt='Attempt1'

  print ('DEBUG: latestRigidTfm')
  print rigidTfm

  latestRigidTfm = rigidTfm

  success = success or IsBSplineTfmValid(bsplineTfm)
  if not success:
    print 'Processing failed for needle image ',nid
    exit()

  regTimesLog.write(str(case)+';'+str(nid)+';'+attempt+';'+str(endTime-startTime)+';')

