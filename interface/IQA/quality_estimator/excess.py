import numpy as np
import scipy.stats

def get_excess(gray_img):
  gray_img_fft = np.fft.fftn(gray_img)
  gray_img_fft_shifted = np.abs(np.fft.fftshift(gray_img_fft))
  excess = scipy.stats.kurtosis(gray_img_fft_shifted, axis=None)
  return excess

