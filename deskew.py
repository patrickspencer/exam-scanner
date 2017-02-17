import cv2
from PIL import Image
import numpy as np

def compute_skew(image):
    image = cv2.bitwise_not(image)
    height, width = image.shape

    edges = cv2.Canny(image, 150, 200, 3, 5)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=width / 2.0, maxLineGap=20)
    angle = 0.0
    cv2.imwrite('lines.png',edges)
    number_of_line = lines.size
    for x1, y1, x2, y2 in lines[0]:
        if x1 != x2:
            angle += np.arctan(y2 - y1 / x2 - x1)
    return angle / number_of_line

def deskew(image, angle):
    angle = np.math.degrees(angle)
    # image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)
    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows, cols = image.shape
    rotated = cv2.warpAffine(image, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)
    return cv2.getRectSubPix(rotated, (cols, rows), center)

img = cv2.imread("exam_small_spacing_blank_right_rotated.png", cv2.IMREAD_GRAYSCALE)

deskewed_image = deskew(img.copy(), compute_skew(img))
cv2.imwrite('deskewed_image.png',deskewed_image)
