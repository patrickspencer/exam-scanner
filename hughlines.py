import cv2
import numpy as np

img = cv2.imread('exam_small_spacing_blank_right_rotated.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

def HughLinesNorm(image):
    lines = cv2.HoughLines(image,1,np.pi/180,200)

    points = []
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        points.append([x1,x2,y1,y2])
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)

    angles = []
    for p in points:
        x1 = p[0]
        x2 = p[1]
        y1 = p[2]
        y2 = p[3]
        if x1 != x2:
            angles.append(np.arctan(y2 - y1 / x2 - x1))
            # angle += np.arctan(y2 - y1 / x2 - x1)
    print("Number of lines: " + str(len(angles)))

    return image

# cv2.imwrite('houghlines_normal.jpg',HughLinesNorm(edges))

def HughLinesP(image):
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    minLineLength = 100
    maxLineGap = 10
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    print(type(lines[0]))
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    return image

cv2.imwrite('houghlines5.jpg',HughLinesP(edges))
