import numpy as np
import cupy as cp
from cupyx.scipy.ndimage import convolve as conv


def tfm(arr, p=0.6):
    arr = np.array(arr)
    p_cpu = np.array([p])

    with cp.cuda.Device(0):
        img = cp.asarray(arr)
        p_gpu = cp.asarray(p_cpu)
        p = p_gpu[0]
        max_elem = img.max()

        k = (img >= p * max_elem).astype(int)
        d_r = cp.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        d_c = cp.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        s_r = conv(img, d_r) / 1000
        s_c = conv(img, d_c) / 1000
        squared_s_r = cp.square(s_r)
        squared_s_c = cp.square(s_c)
        sobel_grad_arr = cp.add(squared_s_r, squared_s_c)

        tfm = cp.multiply(k, sobel_grad_arr).sum()
        tfm_arr_gpu = cp.array([tfm])

    tfm_arr_cpu = cp.asnumpy(tfm_arr_gpu)
    return tfm_arr_cpu[0]
