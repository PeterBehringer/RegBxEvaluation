import SimpleITK as sitk

inputPATH = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/TempDir/25_8-Resampled-CoverProstate-TG.nrrd'
outputPATH = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/masks/25_8-Resampled-CoverProstate-TG_bigger_automated_z0.nrrd'

image_input=sitk.ReadImage(inputPATH)

grayscale_dilate_filter = sitk.GrayscaleDilateImageFilter()
grayscale_dilate_filter.SetKernelRadius([7,7,0])
grayscale_dilate_filter.SetKernelType(sitk.sitkBall)

image_output = grayscale_dilate_filter.Execute(image_input)
sitk.WriteImage(image_output,outputPATH)



