import SimpleITK as sitk
import nibabel as nib
import numpy as np
import csv
import os

def read_mhd_and_raw(file_path):
    """读取.mhd文件和对应的.raw文件，并返回作为numpy数组的图像数据及其元数据."""
    itk_image = sitk.ReadImage(file_path)
    np_image = sitk.GetArrayFromImage(itk_image)
    spacing = itk_image.GetSpacing()
    return np_image, spacing

def read_nii_file(file_path):
    """读取.nii文件并返回作为numpy数组的图像数据."""
    nii_image = nib.load(file_path)
    np_image = np.array(nii_image.dataobj)
    return np_image

def cal_age(filename):
    age = 0

    if not filename:
        return 'no filename'

    if filename[0].isdigit():
        age = 18
    elif filename[0] == '1':
        age = int(filename[0:2])
    elif filename[0] == '0':
        if filename[1].isdigit():
            age = int(filename[0:2])
        else:
            age = 0
    return age



def get_sum_of_A(age) -> float:
    # 自己手算更快 F18
    # read the csv file with pharms subtable
    A_tmp = 2.229
    links = [0.26, 0.23, 0.16]
    if age > 5:
        A_tmp += links[2]
    elif age > 1:
        A_tmp += links[1]
    else:
        A_tmp += links[0]
    return A_tmp
    


def calculate_organ_doses(dose_distribution, organ_labels, sum_A):
    """根据器官标签计算并返回每个器官的总剂量.
    Dose = (sum(dosemap)/sum(mask)) * (sum(A)*3600/N) * 1E9 * Freq_e
    F18: Freq_e = 0.9673
    """
    organ_doses = {}
    unique_labels = np.unique(organ_labels)

    # 对于标签图中的每个唯一标签，计算对应器官的总剂量
    for label in unique_labels:
        if label != 0:  # 假设标签0是背景或不感兴趣的区域
            organ_mask = (organ_labels == label)
            organ_dose_all = np.sum(dose_distribution[organ_mask]) 
            organ_mass = np.count_nonzero(organ_mask)
            organ_doses[label] = (organ_dose_all / organ_mass) * (sum_A * 3600 / 1E8) * 1E9 * 0.9673
        # elif label == 15:
        #     organ_mask = (organ_labels == label)
        #     organ_dose_all = np.sum(dose_distribution[organ_mask]) 
        #     organ_mass = np.count_nonzero(organ_mask)
        #     organ_doses[label] = organ_dose_all * 1000 * 3600 / (100 * np.log(2) / 1.83) / organ_mass

    return organ_doses




def run_one_step(dose_file_path, labels_file_path, sum_A):
    # 读取剂量分布和器官标签文件
    dose_distribution, _ = read_mhd_and_raw(dose_file_path)
    dose_distribution = np.transpose(dose_distribution, (2, 1, 0))
    organ_labels = read_nii_file(labels_file_path)

    # 验证剂量和标签数组的形状是否匹配
    if dose_distribution.shape != organ_labels.shape:
        raise ValueError("Dose and label arrays must have the same shape.")

    # 计算每个器官的剂量
    organ_doses = calculate_organ_doses(dose_distribution, organ_labels, sum_A)

    return organ_doses



if __name__ == "__main__":
    # 获得名称
    output_path = '/home/siyi424/gate_Runing_Chinese/output_PETAtlas'
    data_path = '/home/siyi424/gate_Runing_Chinese/data'
    # table_path = '/home/siyi424/gate_Runing_Chinese/get_Dose/Tables_of_pharmas_A.xlsx'

    folder_names = [folder for folder in os.listdir(output_path) if os.path.isdir(os.path.join(output_path, folder))]
    print(folder_names)

    all_res = {}
    # 使用csv模块将数据写入CSV文件
    with open('/home/siyi424/gate_Runing_Chinese/get_Dose/organ_dose.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        for folder in folder_names:
            age = cal_age(folder)
            sum_A = get_sum_of_A(age)
            dose_file_path = os.path.join(output_path, folder,'output-Dose.mhd')
            labels_file_path = os.path.join(data_path, folder, 'Atlas.nii')
            organ_doses = run_one_step(dose_file_path, labels_file_path, sum_A)



            for label, dose in organ_doses.items():
                print(f"{folder}: {label} = {dose}")
                if label not in all_res:
                    all_res[label] = {}
                all_res[label][folder] = dose

        # 写入标题行
        headers = ['Organ'] + folder_names
        writer.writerow(headers)

        for label, doses in all_res.items():
            row = [label] + [doses.get(folder, 0) for folder in folder_names] 
            writer.writerow(row)

                


    
