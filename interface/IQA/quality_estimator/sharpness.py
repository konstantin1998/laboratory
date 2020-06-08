import cv2
import numpy as np
from math import atan

def get_grad_dir(grad_x, grad_y):
  if grad_x == 0:
    if grad_y > 0:
      return 'up'
    else:
      return 'down'
  angle = atan(grad_y / grad_x)
  pi = 3.141592
  angles = np.array([pi / 2, pi / 4, 0, -pi / 4, -pi / 2])
  directions = ['up', 'up-right', 'right', 'down-right', 'down']
  angles = np.abs(angles - angle)
  min_angle_index = list(angles).index(min(angles))
  direction = directions[min_angle_index]
  return direction


def pick_pixels(arr, curr_pixel, direction, interval, reverse=False):
    x, y = curr_pixel
    if direction == 'up':
        pixels = []
        if not reverse:
            for k in range(1, interval + 1):
                pixels.append(arr[x + k][y])
        else:
            for k in range(1, interval + 1):
                pixels.append(arr[x - k][y])
        return pixels

    if direction == 'up-right':
        pixels = []
        if not reverse:
            for k in range(1, interval + 1):
                pixels.append(arr[x + k][y + k])
        else:
            for k in range(1, interval + 1):
                pixels.append(arr[x - k][y - k])
        return pixels

    if direction == 'right':
        if not reverse:
            return arr[x][y + 1: y + interval + 1]
        else:
            return arr[x][y - interval: y]

    if direction == 'down-right':
        pixels = []
        if not reverse:
            for k in range(1, interval + 1):
                pixels.append(arr[x + k][y - k])
        else:
            for k in range(1, interval + 1):
                pixels.append(arr[x - k][y + k])
        return pixels

    if direction == 'down':
        pixels = []
        if not reverse:
            for k in range(1, interval + 1):
                pixels.append(arr[x - k][y])
        else:
            for k in range(1, interval + 1):
                pixels.append(arr[x + k][y])
        return pixels


def measure_sharpness(src_img, rate = 0.75):
  edges_img = cv2.Canny(src_img, 3, 1)
  interval = 5
  sharpness = []
  edge_intensity = edges_img.max()
  height, width = edges_img.shape
  sobel_x = cv2.Sobel(src_img, -1, 1, 0)
  sobel_y = cv2.Sobel(src_img, -1, 0, 1)
  for i in range(interval, height - interval):
    for j in range(interval, width - interval):
      if edges_img[i][j] == edge_intensity:
        direction = get_grad_dir(sobel_x[i][j], sobel_y[i][j])
        pixels = list(pick_pixels(src_img, (i,j), direction, interval, True) + pick_pixels(src_img, (i,j), direction, interval))
        min_pixel = min(pixels)
        min_pixel_index = pixels.index(min_pixel)
        max_pixel = max(pixels)
        max_pixel_index = pixels.index(max_pixel)
        curr_sharpness = (max_pixel - min_pixel) / (abs(max_pixel_index - min_pixel_index) + 1)
        sharpness.append(curr_sharpness)
  sharpness.sort()
  sharpness = sharpness[int(len(sharpness) * rate):len(sharpness)]
  sharpness = np.array(sharpness)
  return sharpness.mean()