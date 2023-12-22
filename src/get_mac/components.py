#!/usr/bin/env python
# encoding: utf-8
"""
    @File       : components.py
    @Time       : 2022/8/18 11:10
    @Author     : Haoran Jia
    @license    : Copyright(c) 2022 Haoran Jia. All rights reserved.
    @contact    : 21211140001@m.fudan.edu.cn
    @Description：Gate仿真脚本文件的组成成分
"""

import os
import SimpleITK as sitk



# ======================================================================================================================
# 脚本文件初始化
# ======================================================================================================================
class Components():

    def initialization(self, fpath):
        """
        初始化脚本文件
        :param fpath: 脚本路径
        :return:
        """
        # 创建路径
        folder = os.path.dirname(fpath)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(fpath, "w") as f:
            f.write(f"""

    # GATE Macro Script Generated by Python
    #==============================================================================

    """)
        return 0
        
            
    # ======================================================================================================================
    # Geometry：受照空间 phantom
    # ======================================================================================================================

    def material(self, fpath):
        """
        设置基本的Material Database，运行Gate前需有文件 data/utils/GateMaterials.db
        :param fpath: 脚本路径
        :return:
        """
        with open(fpath, "a") as f:
            f.write("""
    #==============================================================================
    # GEOMETRY
    #==============================================================================

    # Material

    /gate/geometry/setMaterialDatabase              data/utils/GateMaterials.db

            """)


    def geometry_ct(self, fpath, patient_name, ct, ct_name):
        """
        将CT图像文件作为phantom输入
        :param ct_name: ct文件名(不需要格式)
        :param fpath: 脚本路径
        :param patient_name: 患者名称，在“data”下保存“CT.hdr”文件的子文件夹
        :param ct: 待输入的CT，用于计算大小
        :return:
        """
        # 根基CT大小计算world大小
        world = [round(x*y)+10 for (x, y) in zip(ct.GetSize(), ct.GetSpacing())]
        with open(fpath, "a") as f:
            f.write(f"""
    # WORLD

    /gate/world/geometry/setXLength       {world[0]} mm
    /gate/world/geometry/setYLength       {world[1]} mm
    /gate/world/geometry/setZLength       {world[2]} mm

    # CT phantom

    /gate/world/daughters/name                      ct
    /gate/world/daughters/insert                    ImageNestedParametrisedVolume
    /gate/geometry/setMaterialDatabase              data/utils/CT_Materials.db
    /gate/ct/geometry/setHUToMaterialFile           data/utils/CT_HU2mat.txt
    /gate/ct/geometry/setImage                      data/{patient_name}/{ct_name}.hdr

    /gate/ct/placement/setTranslation               0. 0. 0. mm
    /gate/ct/placement/setRotationAxis              1 0 0
    /gate/ct/placement/setRotationAngle             0 deg

    /gate/ct/attachPhantomSD

            """)
        pass


    def geometry_atlas(self, fpath, patient_name, atlas, atlas_name):
        """
            将Atlas图像文件作为phantom输入
            :param atlas_name: ct文件名(不需要格式)
            :param fpath: 脚本路径
            :param patient_name: 患者名称，在“data”下保存“Atlas.hdr”文件的子文件夹
            :param atlas: 待输入的atlas，用于计算大小
            :return:
            """
        world = [round(x * y) + 10 for (x, y) in zip(atlas.GetSize(), atlas.GetSpacing())]
        with open(fpath, "a") as f:
            f.write(f"""
    # WORLD

    /gate/world/geometry/setXLength       {world[0]} mm
    /gate/world/geometry/setYLength       {world[1]} mm
    /gate/world/geometry/setZLength       {world[2]} mm

    # Atlas phantom

    /gate/world/daughters/name                      atlas
    /gate/world/daughters/insert                    ImageNestedParametrisedVolume
    /gate/geometry/setMaterialDatabase              data/utils/OrganMaterials.db
    /gate/atlas/geometry/setRangeToMaterialFile     data/utils/LabelRange.dat
    /gate/atlas/geometry/setImage                   data/{patient_name}/{atlas_name}.hdr

    /gate/atlas/placement/setTranslation               0. 0. 0. mm
    /gate/atlas/placement/setRotationAxis              1 0 0
    /gate/atlas/placement/setRotationAngle             0 deg

    /gate/atlas/attachPhantomSD

    """)
        pass


    # ======================================================================================================================
    # Actor 计数
    # ======================================================================================================================

    def actor_statistic(self, fpath, patient_name, saveEveryNSeconds=20, folder_output="output"):
        with open(fpath, "a") as f:
            f.write(f"""
    #==============================================================================
    # ACTOR
    #==============================================================================

    # Simulation Statistic Actor

    /gate/actor/addActor                SimulationStatisticActor stat
    /gate/actor/stat/save               {folder_output}/{patient_name}/Statistic.txt
    /gate/actor/stat/saveEveryNSeconds  {saveEveryNSeconds}

    """)
        return 0


    def actor_DoseActor_image(self, fpath, patient_name, image, image_type, folder_output="output"):
        with open(fpath, "a") as f:
            f.write(f"""
    # Dose Actor

    /gate/actor/addActor                     DoseActor  dose3d
    /gate/actor/dose3d/save                  {folder_output}/{patient_name}/output.mhd
    /gate/actor/dose3d/attachTo    	         {image_type}
    /gate/actor/dose3d/stepHitType           random
    /gate/actor/dose3d/setPosition           0 0 0 cm
    /gate/actor/dose3d/setResolution         {image.GetSize()[0]} {image.GetSize()[1]} {image.GetSize()[2]}
    /gate/actor/dose3d/saveEveryNSeconds     600

    /gate/actor/dose3d/enableEdep            true
    /gate/actor/dose3d/enableUncertaintyEdep true
    /gate/actor/dose3d/enableDose            true
    /gate/actor/dose3d/enableUncertaintyDose true
    /gate/actor/dose3d/enableNumberOfHits    true

    """)
        return 0


    # ======================================================================================================================
    # Physics 物理过程 & Initialize 初始化
    # ======================================================================================================================

    def physics_petct(self, fpath):
        with open(fpath, "a") as f:
            f.write("""
    #==============================================================================
    # PHYSICS
    #==============================================================================

    /gate/physics/addPhysicsList emstandard_opt3

    """)
        return 0


    def initialize(self, fpath):
        with open(fpath, "a") as f:
            f.write("""
    #==============================================================================
    # INITIALIZE
    #==============================================================================

    /gate/run/initialize

    """)
        return 0


    # ======================================================================================================================
    # Source 放射源
    # ======================================================================================================================

    def source_pet_F18(self, fpath, patient_name, pet: sitk.Image, pet_name):
        """
        用一个PET图像作为源
        :param pet_name: 源文件的名称(不需要格式, 默认为.hdr)
        :param fpath: 脚本路径
        :param patient_name: 患者名称，在“data”下保存“PET.hdr”文件的子文件夹
        :param pet: 待输入的PET，用于计算平移距离
        :return:
        """
        # 将PET平移半个图像大小，使(0, 0, 0)在PET中心
        position = [round(size * spacing / 2 * (-1), 2) for size, spacing in zip(pet.GetSize(), pet.GetSpacing())]
        with open(fpath, "a") as f:
            f.write(f"""
    #==============================================================================
    # SOURCE
    #==============================================================================

    /gate/source/addSource              pet     voxel
    /gate/source/pet/reader/insert      image

    /gate/source/pet/imageReader/translator/insert              linear
    /gate/source/pet/imageReader/linearTranslator/setScale      1.0 Bq 
    /gate/source/pet/imageReader/readFile                       data/{patient_name}/{pet_name}.hdr
    /gate/source/pet/imageReader/verbose                        1
    /gate/source/pet/setPosition                                {position[0]} {position[1]} {position[2]} mm

    /gate/source/pet/gps/particle               e+
    /gate/source/pet/setForcedUnstableFlag      true
    /gate/source/pet/setForcedHalfLife          6586.2 s
    /gate/source/pet/gps/ene/type               Mono
    /gate/source/pet/gps/ene/mono               0.2498 MeV
    /gate/source/pet/gps/confine                NULL
    /gate/source/pet/gps/angtype                iso
    /gate/source/pet/dump                       1

    /gate/source/list

    """)
        return 0


    # ======================================================================================================================
    # Application 收尾：仿真时间、粒子数、随机
    # ======================================================================================================================

    def application(self, fpath, N=100000000):
        with open(fpath, "a") as f:
            f.write(f"""
    #==============================================================================
    # TIME, NUMBER, RANDOM
    #==============================================================================

    /gate/application/setTimeSlice   1 s
    /gate/application/setTimeStart   0 s
    /gate/application/setTimeStop    1 s

    /gate/random/setEngineName MersenneTwister
    /gate/random/setEngineSeed auto

    /gate/application/noGlobalOutput
    /gate/application/setNumberOfPrimariesPerRun {N}
    /gate/application/startDAQ

    /exit

    """)
        return 0


    # ======================================================================================================================
    # 其他
    # ======================================================================================================================

    def Hounsfield_material(self, fpath):
        """
        生成CT与material的对应文件
        :param fpath:脚本路径
        :return:
        """
        with open(fpath, "w") as f:
            f.write("""
    #=====================================================================================================
    # An easy way to generate Material.db and HU2mat.txt files for real CT input as phantom
    #   Three files are needed in the right place:
    #       1. data/utils/GateMaterials.db
    #       2. data/utils/Schneider2000MaterialsTable.txt              
    #       3. data/utils/Schneider2000DensitiesTable.txt
    #   Two files will be generated:
    #       1. data/utils/CT_Materials.db          
    #       2. data/utils/CT_HU2mat.txt    
    #=====================================================================================================

    /gate/geometry/setMaterialDatabase                                      data/utils/GateMaterials.db

    /gate/HounsfieldMaterialGenerator/SetMaterialTable                      data/utils/Schneider2000MaterialsTable.txt
    /gate/HounsfieldMaterialGenerator/SetDensityTable                       data/utils/Schneider2000DensitiesTable.txt
    /gate/HounsfieldMaterialGenerator/SetDensityTolerance                   0.1 g/cm3
    /gate/HounsfieldMaterialGenerator/SetOutputMaterialDatabaseFilename     data/utils/CT_Materials.db
    /gate/HounsfieldMaterialGenerator/SetOutputHUMaterialFilename           data/utils/CT_HU2mat.txt
    /gate/HounsfieldMaterialGenerator/Generate
    """)
        return 0


    def verbose(self, fpath):
        with open(fpath, "a") as f:
            f.write("""
    #==============================================================================
    # VERBOSE
    #==============================================================================
    /gate/verbose Physic    1
    /gate/verbose Cuts      1
    /gate/verbose SD        0
    /gate/verbose Actions   0
    /gate/verbose Actor     0
    /gate/verbose Step      0
    /gate/verbose Error     1
    /gate/verbose Warning   1
    /gate/verbose Output    0
    /gate/verbose Beam      0
    /gate/verbose Volume    0
    /gate/verbose Image     0
    /gate/verbose Geometry  2

    """)


    def visualization(self, fpath):
        with open(fpath, "a") as f:
            f.write("""
    #==============================================================================
    # VISUALIZATION
    #==============================================================================
    /vis/open                           OGLIQt
    /vis/viewer/set/viewpointThetaPhi   60 60
    /vis/viewer/zoom                    1.0
    /vis/drawVolume
    /vis/viewer/flush
    /tracking/storeTrajectory           1
    /vis/scene/add/trajectories 
    /vis/scene/endOfEventAction         accumulate  -1

    """)


def PET_Atlas(fpath, patient_name, pet_name, atlas: sitk.Image, pet: sitk.Image, N=5E8, output="output"):
    components = Components()

    components.initialization(fpath)

    components.geometry_atlas(fpath, patient_name, atlas, "Atlas")

    components.actor_statistic(fpath, patient_name, folder_output=output)
    components.actor_DoseActor_image(fpath, patient_name, atlas, image_type="atlas", folder_output=output)

    components.physics_petct(fpath)

    components.initialize(fpath)

    components.source_pet_F18(fpath, patient_name, pet, pet_name)

    components.application(fpath, N)

    return 0