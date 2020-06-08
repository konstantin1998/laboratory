import cv2
import os
import numpy as np
import scipy.stats
from .TFM import tfm
def estimate_quality(path_to_img):
    gray_image = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)
    tfm_score = tfm(gray_image)
    return tfm_score