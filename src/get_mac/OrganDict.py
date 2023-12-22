OrganID = {
    10: 'Body', 11: 'Skin', 13: 'Muscle', 15: 'Bladder', 18: 'Brain',
    19: 'Breast', 20: 'Bronchi', 21: 'Esophagus', 22: 'Eye', 23: 'Len',
    24: 'GallBladder', 26: 'Heart', 28: 'Kidney', 29: 'Larynx', 32: 'Liver',
    33: 'Lung', 37: 'OralCavity', 38: 'Pancreas', 39: 'Penis', 42: 'Pituitary',
    43: 'Parotid', 44: 'Intestine', 46: 'Bone', 47: 'Marrow', 63: 'TMJ',
    65: 'SpinalCord', 66: 'Spleen', 67: 'Stomach', 69: 'Thymus', 70: 'Thyroid',
    71:'Tongue', 72: 'Tonsil', 73: 'Trachea', 75: 'Cochlea', 76: 'BrainStem',
    77: 'TemporalLobe', 78: 'OpticChiasm', 79: 'OpticalNerve', 80: 'Rectum',
    81: 'Sigmoid', 82: 'Duodenum', 85: "Testis", 86: 'Ovary', 88: 'Uterine',
    90: 'Placenta', 92: 'Amniotic fluid', 110: 'Fetal soft tissue', 111: 'Fetal skeleton',
    112: 'Fetus Bone Marrow', 113: 'Fetus Brain', 114: 'Fetus Esophagus',
    115: 'Fetus Eyes', 116: 'Fetus Thyroid', 117: 'Fetus Spinal cord',
    118: 'Fetus Lungs', 119: 'Fetus Heart', 120: 'Fetus Kidneys',
    121: 'Fetus Liver', 122: 'Fetus Stomach', 123: 'Fetus Gall bladder',
    124: 'Fetus SG', 125: 'Fetus LI', 126: 'Fetus SI', 127: 'Fetus UB',
    128: 'Fetus Skin', 129: 'Fetus Ovaries', 130: 'Fetus Testis',
    131: 'Fetus Adrenal', 132: 'Fetus Pancreas', 133: 'Fetus Spleen',
    134: 'Fetus Thymus',
    210: 'Twins soft tissue', 211: 'Twins skeleton',
    212: 'Twins Bone Marrow', 213: 'Twins Brain', 214: 'Twins Esophagus',
    215: 'Twins Eyes', 216: 'Twins Thyroid', 217: 'Twins Spinal cord',
    218: 'Twins Lungs', 219: 'Twins Heart', 220: 'Twins Kidneys',
    221: 'Twins Liver', 222: 'Twins Stomach', 223: 'Twins Gall bladder',
    224: 'Twins SG', 225: 'Twins LI', 226: 'Twins SI', 227: 'Twins UB',
    228: 'Twins Skin', 229: 'Twins Ovaries', 230: 'Twins Testis',
    231: 'Twins Adrenal', 232: 'Twins Pancreas', 233: 'Twins Spleen',
    234: 'Twins Thymus'
    # 其他
}

OrganDensity_ICRP = {
    10: 1.00, 11: 1.09, 15: 1.04, 18: 1.05,
    19: 0.99, 20: 1.03, 21: 1.03, 22: 1.05,
    23: 1.05, 24: 1.03, 26: 1.05, 27: 1.00, 28: 1.05,
    32: 1.05, 33: 0.26, 38: 1.05, 42: 1.03,
    43: 1.03, 44: 1.04, 46: 1.92, 47: 0.98,
    65: 1.03, 66: 1.04, 67: 1.04, 69: 1.03,
    70: 1.04, 71: 1.05, 72: 1.03, 73: 1.03,
    88: 1.03, 90: 1.03, 91: 1.03, 92: 1.00,
    93: 1.03, 94: 1.03, 110: 1.00, 111: 1.92,
    112: 0.98, 113: 1.05, 114: 1.03, 115: 1.05,
    116: 1.04, 117: 1.03, 118: 0.26, 119: 1.05,
    120: 1.05, 121: 1.05, 122: 1.04, 123: 1.03,
    124: 1.03, 125: 1.04, 126: 1.04, 127: 1.02,
    128: 1.09, 129: 1.04, 130: 1.04, 131: 1.03,
    132: 1.05, 133: 1.04, 134: 1.03
}

OrganDensity_excel = {
    10: 1.00, 11: 0.92, 15: 1.06, 18: 1.05,
    19: 0.98, 20: 1.07, 21: 1.05, 22: 1.05,
    23: 1.02, 24: 1.02, 26: 1.04, 28: 1.03,
    32: 1.05, 33: 0.41, 38: 1.05, 42: 0.95,
    43: 1.05, 44: 1.03, 46: 1.91, 47: 1.40,
    65: 1.05, 66: 1.04, 67: 1.05, 69: 1.03,
    70: 1.01, 71: 1.08, 72: 0.95, 73: 1.05,
    88: 1.04, 90: 1.03, 91: 1.03, 92: 1.00,
    110: 1.02, 111: 1.42,
    112: 0.76, 113: 1.02, 114: 1.02, 115: 1.02,
    116: 1.00, 117: 1.02, 118: 1.05, 119: 0.98,
    120: 1.00, 121: 1.02, 122: 1.02, 123: 1.02,
    124: 1.02, 125: 1.02, 126: 1.02, 127: 1.02,
    128: 0.60, 129: 1.02, 130: 1.02, 131: 1.05,
    132: 1.05, 133: 1.05, 134: 1.00
}

MultipleOrgans = {
    10: (10, 11, 13, 15, 18, 19, 21, 22, 23, 24,
         26, 28, 29, 32, 33, 37, 38, 39, 42, 43,
         44, 46, 47, 63, 65, 66, 67, 70, 73, 75,
         76, 77, 78, 79, 80, 81, 82, 85, 86),
    22: (22, 23), 18: (18, 76, 77), 46: (46, 47),
    88: (88, 90, 92, 110, 111, 112, 113, 114, 115, 116,
         117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
         128, 129, 130, 131, 132, 133, 134),
}


EssentialOrganID = [10, 11, 15, 18, 23, 24, 26, 28, 32, 33, 38, 44, 46, 66, 67, 70]
