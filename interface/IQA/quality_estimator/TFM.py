import numpy as np


def sobel_grad(arr):
    d_r = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    d_c = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    arr = np.array(arr)
    s_r = (arr * d_r).sum()
    s_c = (arr * d_c).sum()
    return (s_r ** 2 + s_c ** 2) ** 0.5


def tfm(arr, p=0.6):
    arr = np.array(arr)
    max_elem = np.absolute(arr).max()
    k = np.zeros(arr.shape)
    for i in range(k.shape[0]):
        for j in range(k.shape[1]):
            if (abs(arr[i, j]) >= p * max_elem):
                k[i, j] = 1
            else:
                k[i, j] = 0

    result = 0
    height, width = arr.shape
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            window = np.array([arr[i - 1][j - 1: j + 2], arr[i][j - 1: j + 2], arr[i + 1][j - 1: j + 2]])
            result += k[i, j] * sobel_grad(window) ** 2

    return result
