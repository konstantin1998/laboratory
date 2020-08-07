import time
from interface.IQA.quality_estimator.estimator import estimate_quality

img_paths = [
    "D:\Word\DataSets\DS_1205\Migr\cropped_old\DS20180906120502_2Conv_Migr_1_V60_R200_T5e-07_Tc1_dwns6_V40_S5.9744_lb.bmp",
    "D:\Word\DataSets\DS_1205\Migr\cropped_old\DS20180906120502_2Conv_Migr_1_V60_R200_T5e-07_Tc1_dwns6_V40_S5.9744_lt.bmp",
    "D:\Word\DataSets\DS_1205\Migr\cropped_old\DS20180906120502_2Conv_Migr_1_V60_R200_T5e-07_Tc1_dwns6_V40_S5.9744_rb.bmp",
    "D:\Word\DataSets\DS_1205\Migr\cropped_old\DS20180906120502_2Conv_Migr_1_V60_R200_T5e-07_Tc1_dwns6_V40_S5.9744_rt.bmp",
    "D:\Word\DataSets\DS_1205\Migr\cropped_old\DS20180906120502_2Conv_Migr_1_V60_R200_T5e-07_Tc1_dwns6_V42_S5.9642_lb.bmp"
]
qualities = []
start_time = time.time()

for img_path in img_paths:
    quality = estimate_quality(img_path)
    qualities.append(quality)
print('duration:', time.time() - start_time)
print('qualities:', qualities)




