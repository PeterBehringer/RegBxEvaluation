import os, argparse, string, re, sys, glob
from time import time

def BFResample(reference,moving,tfm,output,interp='Linear'):
  CMD = 'Slicer3 --launch BRAINSResample --referenceVolume '+reference+' --inputVolume '+moving+' --outputVolume '+output+' --warpTransform '+tfm
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

def TransformFiducials(ref, mov, fidIn, tfmIn, fidOut):

 CMD="~/bitbucket/SlicerCLITools-build/TransformFiducialList --referenceimage "+ref+" --movingimage "+mov+" --fiducialsfile "+fidIn+" --inputtransform "+tfmIn+" --outputfile "+fidOut
 print CMD
  
 ret = os.system(CMD)
 if ret:
   exit()

 '''
 Case11/IntraopImages/10.nrrd --movingimage
 Case11/IntraopImages/CoverProstate.nrrd --fiducialsfile
 Case11/IntraopImages/CoverProstate-Centroid.fcsv --inputtransform
 Case11/Registration2attempts/10-IntraIntra-BSpline-Attempt1.tfm --outputfile
 Case11/Registration2attempts/10_CoverProstate-Centroid.fcsv
 '''


def transformFiducialsBRAINS(fidIn,tfmIn,fidOut):
  CMD='/Users/peterbehringer/MyProjects/BRAINSTools/BRAINSTools-build/bin/BRAINSConstellationLandmarksTransform -i '+fidIn+' -t '+tfmIn+' -o '+fidOut
  print 'about to run : '+CMD

  ret = os.system(CMD)
  if ret:
   exit()

def transformFiducialsSlicer(fiducialsIn, transform, fiducialsOut):
  ### done in Slicer!
  fidLogic = slicer.modules.markups.logic()
  tfmLogic = slicer.modules.transforms.logic()
  fidId = fidLogic.LoadMarkupsFiducials(fiducialsIn, 'na')
  print 'Fiducials loaded:',fidId
  fid = slicer.mrmlScene.GetNodeByID(fidId)
  tfm = tfmLogic.AddTransform(transform, slicer.mrmlScene)
  fid.SetAndObserveTransformNodeID(tfm.GetID())
  tfmLogic.hardenTransform(fid)

  fidStorage = fid.GetStorageNode()
  fidStorage.SetFileName(fiducialsOut)
  fidStorage.WriteData(fid)
  #slicer.mrmlScene.Clear()

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('case',help='case to be processed')

args = parser.parse_args()

case = args.case

IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'
RegDir='/Users/peterbehringer/MyStudies/Data/Case'+case+'/Slicer4registration'
ResDir='/Users/peterbehringer/MyStudies/Verification/Case'+case
TempDir='/Users/peterbehringer/MyStudies/TempDir'

print 'started!'
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

# moving image/mask will always be the same
movingImage = IntraDir+'/CoverProstate.nrrd'

for nid in needleImageIds:
  bsplineTfm=None

  nidStr=str(nid)

  fixedImage = IntraDir+'/'+nidStr+'.nrrd'

  # check if there is a matching TG
  bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'
  print ('bsplineTfm'+str(bsplineTfm))
  if not os.path.isfile(bsplineTfm):
    print ('went here')
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt1.h5'
    print ('bsplineTfm '+str(bsplineTfm))
  if not os.path.isfile(bsplineTfm):
    print 'Failed to find ANY transform!'
    exit()

  # TODO: choose if targets or centroids should be registered and saved
  #resampled = ResDir+'/'+nidStr+'-Pelvis-RigidRegistered-centroid.fcsv'
  resampled = ResDir+'/'+nidStr+'-BSplineRegistered-centroid.fcsv'
  fidList = IntraDir+'/CoverProstate-Centroid.fcsv'
  # resampled = ResDir+'/'+nidStr+'-BSplineRegistered-targets.fcsv'
  # fidList = IntraDir+'/Case'+case+'_CoverProstate-registered_targets.fcsv'
 
  #if not IsBSplineTfmValid(bsplineTfm):
  #  print 'BSpline transform is not valid! Will skip needle image ',nid
  #  continue
  transformFiducialsBRAINS(fidIn=fidList,tfmIn=bsplineTfm,fidOut=resampled)
  print ('transformed fiducials!')
  # TransformFiducials(ref=fixedImage,mov=movingImage,fidIn=fidList,tfmIn=bsplineTfm,fidOut=resampled)



  # BFResample(reference=fixedImage,moving=movingImage,:tfm=bsplineTfm,output=resampled)  
