import SimpleITK as sitk
import numpy as np
import os


def dat2nii(foldername, filename, x, y, z):
    '''
    path: relative path
    '''
    fullpath = os.path.join('/workspace/data', foldername, filename)
    data = np.fromfile(fullpath, dtype=np.uint8)
    shape = (z, y, x) # z, y, x
    newdata = np.reshape(data, shape)
    img = sitk.GetImageFromArray(newdata)
    img.SetOrigin((0, 0, 0))
    img.SetSpacing((2, 2, 2))
    img.SetDirection([1, 0, 0, 0, 1, 0, 0, 0, 1])
    save_nii = os.path.join('/workspace/data', foldername, 'Atlas.nii')
    sitk.WriteImage(img, save_nii)
    save_mhd = os.path.join('/workspace/data', foldername, 'Atlas.mhd')
    sitk.WriteImage(img, save_mhd)