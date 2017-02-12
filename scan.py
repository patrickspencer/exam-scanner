import cv2
import imutils
import argparse
import numpy as np
from PIL import Image
from imutils import contours

# define the answer key which maps the question number
# to the correct answer
ANSWER_KEY = {
        0: 0,
        1: 1,
        2: 1,
        3: 4,
        4: 4,
        5: 2,
        6: 3,
        7: 2,
        8: 1,
        9: 3,
        10: 1,
        11: 0,
        12: 2,
        13: 2,
        14: 0,
        15: 3,
        16: 1,
        17: 4,
        }

image = cv2.imread("cropped_to_be_graded.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)
# cv2.imwrite('output.png',edged)

# find contours in the edge map, then initialize
# the contour that corresponds to the document
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# apply Otsu's thresholding method to binarize the warped
# piece of paper
thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
# cv2.imwrite('output.png',thresh)

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
questionCnts = []

# loop over the contours
for c in cnts:
        # compute the bounding box of the contour, then use the
        # bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)

        # in order to label the contour as a question, region
        # should be sufficiently wide, sufficiently tall, and
        # have an aspect ratio approximately equal to 1
        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                questionCnts.append(c)

# sort the question contours top-to-bottom, then initialize
# the total number of correct answers
questionCnts = contours.sort_contours(questionCnts,
        method="top-to-bottom")[0]
correct = 0
print(len(questionCnts))

submitted_ans = []

# each question has 5 possible answers, to loop over the
# question in batches of 5
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
        # sort the contours for the current question from
        # left to right, then initialize the index of the
        # bubbled answer
        cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
        bubbled = None
        	# loop over the sorted contours

        # loop through the 5 bubbles in an answer row
        for (j, c) in enumerate(cnts):
                # construct a mask that reveals only the current
                # "bubble" for the question
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)

                # apply the mask to the thresholded image, then
                # count the number of non-zero pixels in the
                # bubble area
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                # if the current total has a larger number of total
                # non-zero pixels, then we are examining the currently
                # bubbled-in answer
                if bubbled is None or total > bubbled[0]:
                        bubbled = (total, j)

                # initialize the contour color and the index of the
                # *correct* answer
                color = (0, 0, 255)
                # q is the problem we are on
                k = ANSWER_KEY[q]

                # check to see if the bubbled answer is correct
                if k == bubbled[1]:
                        color = (0, 255, 0)
                        correct += 1


                # draw the outline of the correct answer on the test
                cv2.drawContours(image, [cnts[k]], -1, color, 3)

        # add the bubble that we stopped on last in the last loop to
        # the submitted answer array
        submitted_ans.append(bubbled[1])

print(submitted_ans)

# print(len(cnts))
contoured = cv2.drawContours(thresh, questionCnts[0:5], -1, (128,155,0), 3)
# cv2.imwrite('output.png',thresh)
cv2.imwrite('output.png',image)
# print(questionCnts[0])

