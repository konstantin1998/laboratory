import cv2
# import random
from .excess import get_excess
from .TFM import tfm as get_tfm
from .brisque import get_brisque_score as get_brisque


def estimate_quality(path_to_img):
    gray_image = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)

    modified_tfm = get_tfm(gray_image)
    modified_brisque = (get_brisque(gray_image) + 10) * 30
    modified_excess = get_excess(gray_image) / 1000

    return int((modified_tfm + modified_brisque + modified_excess) / 3)