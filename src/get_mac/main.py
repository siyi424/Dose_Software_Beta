import os
import SimpleITK as sitk
import nibabel as nib
import numpy as np
import mysql.connector
import shutil

from components import PET_Atlas
from OrganDict import OrganID, MultipleOrgans
from dat2nii import dat2nii



# ======================================================================================================================
# 文件生成函数
# ======================================================================================================================

def ICRP_F18PET_source_preg(fpath_atlas, fpath_save):
    """
    根据ICRP128号报告的器官累计活度，生成对应的活度源
    :param age: 患者的年龄
    :param fpath_save: 保存nii文件的路径
    :param fpath_atlas: 分割文件的路径
    :return:
    """
    # 读取分割
    seg: np.ndarray = sitk.GetArrayFromImage(sitk.ReadImage(fpath_atlas))

    # 指定剂量器官ID，填补其中空缺
    ID_specific = [18, 26, 33, 32, 15]
    fetus_ID = [113, 119, 118, 121, 127]
    for ID in ID_specific:
        if ID in MultipleOrgans:
            for ID_sub in MultipleOrgans[ID]:
                seg[seg == ID_sub] = ID

    # 将其他器官均设为body 10
    ID_ignore = [x for x in OrganID if (x not in ID_specific and x != 10 and x < 110)]
    for ID in ID_ignore:
        seg[seg == ID] = 10
    # 将其他婴儿器官均设为body 110
    fetus_ID_ignore = [x for x in OrganID if (x not in fetus_ID and x > 110)]
    for ID in fetus_ID_ignore:
        seg[seg == ID] = 110

    # 根据年龄获取膀胱的ICRP值
    # bladder_activity = F18_bladder_cumulate_activity(age)
    # 0.26_mother; 0.16_fetus

    # source为生成的源
    source = np.zeros_like(seg, dtype=float)
    # 赋值
    for ID, ICRP_value in zip([18, 26, 33, 32, 15, 10, 113, 119, 118, 121, 127, 110],
                              [0.21, 0.11, 0.079, 0.13, 0.26, 1.7, 0.21, 0.11, 0.079, 0.13, 0.16, 1.7]):
        mask = seg.copy()
        mask[mask != ID] = 0
        mask[mask == ID] = 1
        if mask.sum() == 0:
            print(f"{fpath_atlas} misses organ {ID}")
            source[seg == ID] = 0
        else:
            source[seg == ID] = ICRP_value * 10E6 / mask.sum()

    # 保存图像文件
    source = sitk.GetImageFromArray(source)
    source.CopyInformation(sitk.ReadImage(fpath_atlas))
    source = sitk.Cast(source, sitk.sitkFloat32)
    sitk.WriteImage(source, os.path.join(fpath_save, "PET.nii"))

    # 转换为hdr
    source_nib = nib.load(os.path.join(fpath_save, "PET.nii"))
    # nib.save(source_nib, fpath_save[:-4] + ".hdr")
    nib.save(source_nib, os.path.join(fpath_save, "PET.hdr"))

    return 0

def F18_bladder_cumulate_activity(age):
    if 0 <= age <= 3:
        activity = 0.16
    elif 3 < age <= 7:
        activity = 0.23
    else:
        activity = 0.26

    return activity

def ICRP_F18PET_source(fpath_atlas, fpath_save, age):
    """
    根据ICRP128号报告的器官累计活度，生成对应的活度源
    :param age: 患者的年龄
    :param fpath_save: 保存nii文件的路径
    :param fpath_atlas: 分割文件的路径
    :return:
    """
    # 读取分割
    seg: np.ndarray = sitk.GetArrayFromImage(sitk.ReadImage(fpath_atlas))

    # 指定剂量器官ID，填补其中空缺
    ID_specific = [18, 26, 33, 32, 16]
    for ID in ID_specific:
        if ID in MultipleOrgans:
            for ID_sub in MultipleOrgans[ID]:
                seg[seg == ID_sub] = ID

    # 将其他器官均设为body 10

    OrganID = np.unique(seg)[1:]
    print(OrganID)

    ID_ignore = [x for x in OrganID if (x not in ID_specific and x != 10)]
    for ID in ID_ignore:
        seg[seg == ID] = 10

    # 根据年龄获取膀胱的ICRP值
    bladder_activity = F18_bladder_cumulate_activity(age)
    # 0.26_mother; 0.16_fetus

    # source为生成的源
    source = np.zeros_like(seg, dtype=float)
    # 赋值
    for ID, ICRP_value in zip([18, 26, 33, 32, 16, 10],
                              [0.21, 0.11, 0.079, 0.13, bladder_activity, 1.7]):
        mask = seg.copy()
        mask[mask != ID] = 0
        mask[mask == ID] = 1
        if mask.sum() == 0:
            print(f"{fpath_atlas} misses organ {ID}")
            source[seg == ID] = 0
        else:
            source[seg == ID] = ICRP_value * 10E5 / mask.sum()

    # 保存图像文件
    source = sitk.GetImageFromArray(source)
    source.CopyInformation(sitk.ReadImage(fpath_atlas))
    source = sitk.Cast(source, sitk.sitkFloat32)
    sitk.WriteImage(source, os.path.join(fpath_save, "PET.nii"))

    # 转换为hdr
    source_nib = nib.load(os.path.join(fpath_save, "PET.nii"))
    # nib.save(source_nib, fpath_save[:-4] + ".hdr")
    nib.save(source_nib, os.path.join(fpath_save, "PET.hdr"))

    return 0



def prepare_simulation_ICRPAtlas(pname, output="output", N=5E8, age=8):
    # 数据文件夹
    folder_data = os.path.join("/workspace/data", pname)
    folder_output = os.path.join(output, pname)
    # 输出文件夹
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)

    # 利用ICRP参数生成伪PET
    if not os.path.exists(os.path.join(folder_data, "PET.hdr")):
        # 生成
        ICRP_F18PET_source(fpath_atlas=os.path.join(folder_data, "Atlas.nii"),
                           fpath_save=os.path.join(folder_data), age=age)

    atlas = sitk.ReadImage(os.path.join(folder_data, "Atlas.nii"))
    PET = sitk.ReadImage(os.path.join(folder_data, "PET.nii"))
    # 转换格式
    if not os.path.exists(os.path.join(folder_data, "Atlas.hdr")):
        Atlas_nib = nib.load(os.path.join(folder_data, "Atlas.nii"))
        nib.save(Atlas_nib, os.path.join(folder_data, "Atlas.hdr"))

    PET_Atlas(fpath=os.path.join("mac", pname + ".mac"), patient_name=pname,
                    pet_name="PET", atlas=atlas, pet=PET, N=N, output=output)

def connect_mysql(filename):
    mydb = mysql.connector.connect(
        host="mysql-env",  # Use the service name as hostname
        user="root",
        password="123456",
        database="Chinses_Reference_Population"
    )

    filename_to_search = filename  # Replace with the actual filename
    cursor = mydb.cursor()
    query = f"SELECT file_path FROM your_table WHERE filename = '{filename_to_search}'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        file_path_in_mysql = result[0]
    else:
        # Handle the case where the file is not found
        print("File not found in MySQL.")
        exit()
    
    local_destination_folder = "/workspace/data/03yf"  # Replace with your desired local folder
    shutil.copy(file_path_in_mysql, local_destination_folder)



if __name__ == "__main__":
    # step1: connect to mysql
    filename = "222_(166_96_528)_03yf_ChangeOrganWeight_FinalSize(331_192_1055)_Fetus_344_199_1055_Merged.dat"
    x, y, z = 166, 96, 528
    connect_mysql(filename)

    # step2: data2nii -> Altas.nii
    dat2nii(foldername='03yf', filename=filename, x=x, y=y, z=z)

    # step3: -> PET.nii & pname.mac file
    # pname: data/(phantoms's folder_name)
    prepare_simulation_ICRPAtlas(pname="03yf", output="/workspace/output", N=1E8, age=3)
