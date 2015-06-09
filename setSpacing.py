import SimpleITK as sitk

mistakes=[]
mistakes.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/7-TG.nrrd')
mistakes.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/12-TG.nrrd')
mistakes.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/13-TG.nrrd')
mistakes.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/19-TG.nrrd')
mistakes.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/23-TG.nrrd')

image_reference=sitk.ReadImage('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/12.nrrd')
image_mistake=sitk.ReadImage('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/12-TG.nrrd')

spacing_reference=image_reference.GetSpacing()
spacing_mistake=image_mistake.GetSpacing()
print 'spacing_reference = '+str(spacing_reference)
print 'spacing_mistake = '+str(spacing_mistake)

origin_reference=image_reference.GetOrigin()
origin_mistake=image_mistake.GetOrigin()
print 'origin_reference = '+str(origin_reference)
print 'origin_mistake = '+str(origin_mistake)

outputPaths=[]
outputPaths.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/7-TG_1.nrrd')
outputPaths.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/12-TG_1.nrrd')
outputPaths.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/13-TG_1.nrrd')
outputPaths.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/19-TG_1.nrrd')
outputPaths.append('/Users/peterbehringer/MyStudies/Data/Case14/IntraopImages/23-TG_1.nrrd')

for i in range(0,len(mistakes)):
    image=sitk.ReadImage(mistakes[i])
    image.SetSpacing(spacing_reference)
    image.SetOrigin(origin_reference)
    sitk.WriteImage(image,outputPaths[i])





