
from interface.IQA.quality_estimator.estimator import estimate_quality
import os.path
import time

image_names = ['St112L_4_V_46_S_629671.2562.bmp',
               'St112L_4_V_52_S_621672.4916.bmp',
               'St112L_4_V_58_S_616534.0086.bmp',
               'St112L_4_V_62_S_618506.5305.bmp',
               'St112L_4_V_64_S_622187.4392.bmp']
img_dir = 'D:/Word/imgs'
qualities = []
start_time = time.time()
for name in image_names:
    path_to_img = os.path.join(img_dir, name)
    quality = estimate_quality(path_to_img)
    qualities.append(quality)
print("--- %s seconds ---" % (time.time() - start_time))
print(qualities)
