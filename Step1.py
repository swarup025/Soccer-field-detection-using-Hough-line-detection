#Step1 includes Preprocessing

import cv2 as cv
import numpy as np
import matplotlib

#from glob import glob

frame = cv.imread(r'Original Snaps\\img2.jpg')

frame = cv.resize(frame, (640, 480))

hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_green = np.array([36,0,0])
upper_green = np.array([86,255,255])
# Threshold the HSV image to get only blue colors
mask = cv.inRange(hsv, lower_green, upper_green)
# Bitwise-AND mask and original image
res = cv.bitwise_and(frame,frame, mask= mask)
#cv.imshow('frame',frame)
#cv.imshow('mask',mask)
cv.imshow('res',res)
cv.imwrite(r'Preprosessed Snaps\\Segmented1.jpg',res)
rows,cols,_ = res.shape

#Canny
gray = cv.cvtColor(res,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)


#Hough-Line Transformation
lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100, None, 50, 20)

for points in lines:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
     # On the original image
    cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

cv.imwrite(r'Preprosessed Line Snaps\\LinedPre1.jpg',frame)

cv.waitKey(0)
cv.destroyAllWindows()