import cv2
import numpy as np
import math
import imutils


def shape_dissimilarity(resized):

    # Image read and converted to gray-scale blurred shapes
    # resized = imutils.resize(img, width=300)
    # resized = img
    # ratio = img.shape[0] / float(resized.shape[0])
    #print(resized.shape)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    thresholded = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

    # Compute thresholded saliency map
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(resized)
    saliencyMap = (saliencyMap*255).astype("uint8")
    thresh_saliencyMap = cv2.threshold(saliencyMap, 50, 255, cv2.THRESH_BINARY)[1]

    # Shape Detection and Matching on Saliency Map
    # only retrieve the outer shapes(largest salient region)
    contours = cv2.findContours(thresh_saliencyMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # peri = cv2.arcLength()
    contours = imutils.grab_contours(contours)
    # print(contours)
    # Only consider longest contour as the shape for largest salient region
    max_ctr = None
    max_len = 0
    for ctr in contours:
        if max_len < len(ctr):
            max_len = len(ctr)
            max_ctr = ctr

    # draw the longest contour for eye test
    cv2.drawContours(resized, max_ctr, -1, (0, 255, 0), 2)
    #
    # cv2.imshow("img", resized)

    # Find Contours of reference shapes

    # square
    square = cv2.imread("./shapes/square.jpg")
    square_contour, square_resized = find_max_contour(square)

    cv2.drawContours(square_resized, square_contour, -1, (0, 255, 0), 2)

    # cv2.imshow("shape1", square_resized)
    # cv2.waitKey(0)
    #

    # rectangle 1
    rect1 = cv2.imread("./shapes/rect1.png")
    rect1_contour, rect1_resized = find_max_contour(rect1)

    # cv2.drawContours(rect1_resized, rect1_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape2", rect1_resized)
    # cv2.waitKey(0)

    # rectangle 2
    rect2 = cv2.imread("./shapes/rect2.png")
    rect2_contour, rect2_resized = find_max_contour(rect2)

    # cv2.drawContours(rect2_resized, rect2_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape3", rect2_resized)
    # cv2.waitKey(0)
    #

    # triangle 1

    tri1 = cv2.imread("./shapes/scalene.png")
    tri1_contour, tri1_resized = find_max_contour(tri1)

    # cv2.drawContours(tri1_resized, tri1_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape4", tri1_resized)
    # cv2.waitKey(0)

    # triangle 2
    tri2 = cv2.imread("./shapes/isosceles.jpg")
    tri2_contour, tri2_resized = find_max_contour(tri2)

    # cv2.drawContours(tri2_resized, tri2_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape5", tri2_resized)
    # cv2.waitKey(0)

    # triangle 3
    tri3 = cv2.imread("./shapes/right.png")
    tri3_contour, tri3_resized = find_max_contour(tri3)

    # cv2.drawContours(tri3_resized, tri3_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape6", tri3_resized)
    # cv2.waitKey(0)

    # triangle 4
    tri4 = cv2.imread("./shapes/obtuse.png")
    tri4_contour, tri4_resized = find_max_contour(tri4)

    # cv2.drawContours(tri4_resized, tri4_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape7", tri4_resized)
    # cv2.waitKey(0)

    # five-pointed star

    star = cv2.imread("./shapes/star.jpg")
    star_contour, star_resized = find_max_contour(star)

    # cv2.drawContours(star_resized, star_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape8", star_resized)
    # cv2.waitKey(0)

    # rhombus

    rhombus = cv2.imread("./shapes/rhombus.jpg")
    rhombus_contour, rhombus_resized = find_max_contour(rhombus)

    # cv2.drawContours(rhombus_resized, rhombus_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape9", rhombus_resized)
    # cv2.waitKey(0)

    # trapezoid

    trapezoid = cv2.imread("./shapes/trapezoid.png")
    trapezoid_contour, trapezoid_resized = find_max_contour(trapezoid)

    # cv2.drawContours(trapezoid_resized, trapezoid_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape10", trapezoid_resized)
    # cv2.waitKey(0)

    # circle

    circle = cv2.imread("./shapes/circle.jpg")
    circle_contour, circle_resized = find_max_contour(circle)

    # cv2.drawContours(circle_resized, circle_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape11", circle_resized)
    # cv2.waitKey(0)

    # line

    line = cv2.imread("./shapes/line.png")
    line_contour, line_resized = find_max_contour(line)

    # cv2.drawContours(line_resized, line_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape12", line_resized)
    # cv2.waitKey(0)

    # free-form curve

    curve = cv2.imread("./shapes/curve.png")
    curve_contour, curve_resized = find_max_contour(curve)

    # cv2.drawContours(curve_resized, curve_contour, -1, (0, 255, 0), 2)
    # cv2.imshow("shape13", curve_resized)
    # cv2.waitKey(0)

    # Shape Matching with Hu invariants
    scores = []
    score1 = cv2.matchShapes(max_ctr, square_contour, 3, 0)
    score2 = cv2.matchShapes(max_ctr, rect1_contour, 3, 0)
    score3 = cv2.matchShapes(max_ctr, rect2_contour, 3, 0)
    score4 = cv2.matchShapes(max_ctr, tri1_contour, 3, 0)
    score5 = cv2.matchShapes(max_ctr, tri2_contour, 3, 0)
    score6 = cv2.matchShapes(max_ctr, tri3_contour, 3, 0)
    score7 = cv2.matchShapes(max_ctr, tri4_contour, 3, 0)
    score8 = cv2.matchShapes(max_ctr, star_contour, 3, 0)
    score9 = cv2.matchShapes(max_ctr, rhombus_contour, 3, 0)
    score10 = cv2.matchShapes(max_ctr, trapezoid_contour, 3, 0)
    score11 = cv2.matchShapes(max_ctr, circle_contour, 3, 0)
    score12 = cv2.matchShapes(max_ctr, line_contour, 3, 0)
    score13 = cv2.matchShapes(max_ctr, curve_contour, 3, 0)

    # print("square", score1)
    # print("rect1 ", score2)
    # print("rect2 ", score3)
    # print("tri1 ", score4)
    # print("tri2 ", score5)
    # print("tri3 ", score6)
    # print("tri4 ", score7)
    # print("star ", score8)
    # print("rhombus ", score9)
    # print("trapezoid ", score10)
    # print("circle", score11)
    # print("line", score12)
    # print("curve ", score13)

    # convexity
    hull = cv2.convexHull(max_ctr, returnPoints=False)
    defects = cv2.convexityDefects(max_ctr, hull)
    # print(defects)
    # print(hull)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(max_ctr[s][0])
        end = tuple(max_ctr[e][0])
        far = tuple(max_ctr[f][0])
        cv2.line(resized, start, end, [0, 255, 0], 2)
        cv2.circle(resized, far, 5, [0, 0, 255], -1)
    convexity = defects.shape[0] / hull.shape[0]
    # print(convexity)
    # print(defects.shape[0], hull.shape[0])
    # cv2.imshow("img", resized)
    # cv2.waitKey(0)

    scores.append(score1)
    scores.append(score2)
    scores.append(score3)
    scores.append(score4)
    scores.append(score5)
    scores.append(score6)
    scores.append(score7)
    scores.append(score8)
    scores.append(score9)
    scores.append(score10)
    scores.append(score11)
    scores.append(score12)
    scores.append(score13)

    return scores


def find_max_contour(img):
    # preprocess image
    resized = imutils.resize(img, width=300)
    #resized = img
    # ratio = img.shape[0] / float(resized.shape[0])
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (5, 5), 0)
    thresholded = cv2.threshold(denoised, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours
    contours = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    max_ctr = None
    max_len = 0
    for ctr in contours:
        if max_len < len(ctr):
            max_len = len(ctr)
            max_ctr = ctr
    # print(max_ctr)
    return max_ctr, resized


#
# import cv2
# import numpy as np
# import math
# import imutils
# import os
# import pickle
#
#
# def shape_dissimilarity(denoised):
#
#     # Image read and converted to gray-scale blurred shapes
#     # img = cv2.imread(path)
#     # resized = imutils.resize(img, width=300)
#     # ratio = img.shape[0] / float(resized.shape[0])
#     # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#     # denoised = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresholded = cv2.threshold(denoised, 60, 255, cv2.THRESH_BINARY)[1]
#
#     # Compute thresholded saliency map
#     saliency = cv2.saliency.StaticSaliencyFineGrained_create()
#     (success, saliencyMap) = saliency.computeSaliency(resized)
#     saliencyMap = (saliencyMap*255).astype("uint8")
#     thresh_saliencyMap = cv2.threshold(saliencyMap, 50, 255, cv2.THRESH_BINARY)[1]
#
#     # Shape Detection and Matching on Saliency Map
#     # only retrieve the outer shapes(largest salient region)
#     contours = cv2.findContours(thresh_saliencyMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # peri = cv2.arcLength()
#     contours = imutils.grab_contours(contours)
#     # print(contours)
#     # Only consider longest contour as the shape for largest salient region
#     max_ctr = []
#     max_len = 0
#     for ctr in contours:
#         if max_len < len(ctr):
#             max_len = len(ctr)
#             max_ctr = ctr
#     # print(max_ctr)
#     # print(contours[0])
#     # draw the longest contour for eye test
#     cv2.drawContours(resized, max_ctr, -1, (0, 255, 0), 2)
#
#     # cv2.imshow("img", thresh_saliencyMap)
#     # cv2.waitKey(0)
#     # Find Contours of reference shapes
#
#     # square
#     square = cv2.imread("shapes/square.jpg")
#     square_contour, square_resized = find_max_contour(square)
#
#     cv2.drawContours(square_resized, square_contour, -1, (0, 255, 0), 2)
#
#     # cv2.imshow("shape1", square_resized)
#     # cv2.waitKey(0)
#     #
#
#     # rectangle 1
#     rect1 = cv2.imread("shapes/rect1.png")
#     rect1_contour, rect1_resized = find_max_contour(rect1)
#
#     # cv2.drawContours(rect1_resized, rect1_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape2", rect1_resized)
#     # cv2.waitKey(0)
#
#     # rectangle 2
#     rect2 = cv2.imread("shapes/rect2.png")
#     rect2_contour, rect2_resized = find_max_contour(rect2)
#
#     # cv2.drawContours(rect2_resized, rect2_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape3", rect2_resized)
#     # cv2.waitKey(0)
#     #
#
#     # triangle 1
#
#     tri1 = cv2.imread("shapes/scalene.png")
#     tri1_contour, tri1_resized = find_max_contour(tri1)
#
#     # cv2.drawContours(tri1_resized, tri1_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape4", tri1_resized)
#     # cv2.waitKey(0)
#
#     # triangle 2
#     tri2 = cv2.imread("shapes/isosceles.jpg")
#     tri2_contour, tri2_resized = find_max_contour(tri2)
#
#     # cv2.drawContours(tri2_resized, tri2_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape5", tri2_resized)
#     # cv2.waitKey(0)
#
#     # triangle 3
#     tri3 = cv2.imread("shapes/right.png")
#     tri3_contour, tri3_resized = find_max_contour(tri3)
#
#     # cv2.drawContours(tri3_resized, tri3_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape6", tri3_resized)
#     # cv2.waitKey(0)
#
#     # triangle 4
#     tri4 = cv2.imread("shapes/obtuse.png")
#     tri4_contour, tri4_resized = find_max_contour(tri4)
#
#     # cv2.drawContours(tri4_resized, tri4_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape7", tri4_resized)
#     # cv2.waitKey(0)
#
#     # five-pointed star
#
#     star = cv2.imread("shapes/star.jpg")
#     star_contour, star_resized = find_max_contour(star)
#
#     # cv2.drawContours(star_resized, star_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape8", star_resized)
#     # cv2.waitKey(0)
#
#     # rhombus
#
#     rhombus = cv2.imread("shapes/rhombus.jpg")
#     rhombus_contour, rhombus_resized = find_max_contour(rhombus)
#
#     # cv2.drawContours(rhombus_resized, rhombus_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape9", rhombus_resized)
#     # cv2.waitKey(0)
#
#     # trapezoid
#
#     trapezoid = cv2.imread("shapes/trapezoid.png")
#     trapezoid_contour, trapezoid_resized = find_max_contour(trapezoid)
#
#     # cv2.drawContours(trapezoid_resized, trapezoid_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape10", trapezoid_resized)
#     # cv2.waitKey(0)
#
#     # circle
#
#     circle = cv2.imread("shapes/circle.jpg")
#     circle_contour, circle_resized = find_max_contour(circle)
#
#     # cv2.drawContours(circle_resized, circle_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape11", circle_resized)
#     # cv2.waitKey(0)
#
#     # line
#
#     line = cv2.imread("shapes/line.png")
#     line_contour, line_resized = find_max_contour(line)
#
#     # cv2.drawContours(line_resized, line_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape12", line_resized)
#     # cv2.waitKey(0)
#
#     # free-form curve
#
#     curve = cv2.imread("shapes/curve.png")
#     curve_contour, curve_resized = find_max_contour(curve)
#
#     # cv2.drawContours(curve_resized, curve_contour, -1, (0, 255, 0), 2)
#     # cv2.imshow("shape13", curve_resized)
#     # cv2.waitKey(0)
#
#     # Shape Matching with Hu invariants
#     scores = []
#     score1 = cv2.matchShapes(max_ctr, square_contour, 3, 0)
#     score2 = cv2.matchShapes(max_ctr, rect1_contour, 3, 0)
#     score3 = cv2.matchShapes(max_ctr, rect2_contour, 3, 0)
#     score4 = cv2.matchShapes(max_ctr, tri1_contour, 3, 0)
#     score5 = cv2.matchShapes(max_ctr, tri2_contour, 3, 0)
#     score6 = cv2.matchShapes(max_ctr, tri3_contour, 3, 0)
#     score7 = cv2.matchShapes(max_ctr, tri4_contour, 3, 0)
#     score8 = cv2.matchShapes(max_ctr, star_contour, 3, 0)
#     score9 = cv2.matchShapes(max_ctr, rhombus_contour, 3, 0)
#     score10 = cv2.matchShapes(max_ctr, trapezoid_contour, 3, 0)
#     score11 = cv2.matchShapes(max_ctr, circle_contour, 3, 0)
#     score12 = cv2.matchShapes(max_ctr, line_contour, 3, 0)
#     score13 = cv2.matchShapes(max_ctr, curve_contour, 3, 0)
#     #
#     # print("square", score1)
#     # print("rect1 ", score2)
#     # print("rect2 ", score3)
#     # print("tri1 ", score4)
#     # print("tri2 ", score5)
#     # print("tri3 ", score6)
#     # print("tri4 ", score7)
#     # print("star ", score8)
#     # print("rhombus ", score9)
#     # print("trapezoid ", score10)
#     # print("circle", score11)
#     # print("line", score12)
#     # print("curve ", score13)
#
#     # convexity
#     # print(max_ctr)
#     hull = cv2.convexHull(max_ctr, returnPoints=False)
#     defects = cv2.convexityDefects(max_ctr, hull)
#     # print(defects)
#     # print(hull)
#     for i in range(defects.shape[0]):
#         s, e, f, d = defects[i, 0]
#         start = tuple(max_ctr[s][0])
#         end = tuple(max_ctr[e][0])
#         far = tuple(max_ctr[f][0])
#         cv2.line(resized, start, end, [0, 255, 0], 2)
#         cv2.circle(resized, far, 5, [0, 0, 255], -1)
#     convexity = defects.shape[0] / hull.shape[0]
#     # print(convexity)
#     # print(defects.shape[0], hull.shape[0])
#     # cv2.imshow("img", resized)
#     # cv2.waitKey(0)
#
#     scores.append(score1)
#     scores.append(score2)
#     scores.append(score3)
#     scores.append(score4)
#     scores.append(score5)
#     scores.append(score6)
#     scores.append(score7)
#     scores.append(score8)
#     scores.append(score9)
#     scores.append(score10)
#     scores.append(score11)
#     scores.append(score12)
#     scores.append(score13)
#     scores.append(convexity)
#
#     return scores
#
#
# def find_max_contour(img):
#     # preprocess image
#     resized = imutils.resize(img, width=300)
#     # resized = img
#     # ratio = img.shape[0] / float(resized.shape[0])
#     gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#     denoised = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresholded = cv2.threshold(denoised, 60, 255, cv2.THRESH_BINARY)[1]
#
#     # find contours
#     contours = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(contours)
#
#     max_ctr = None
#     max_len = 0
#     for ctr in contours:
#         if max_len < len(ctr):
#             max_len = len(ctr)
#             max_ctr = ctr
#     # print(max_ctr)
#     return max_ctr, resized
#
#
# # directory = "./test_paintings"
# # x = dict()
# # # count = 0
# # # for filename in os.listdir(directory):
# # #     if filename == ".DS_Store":
# # #         continue
# # #     # print(filename)
# # for sub_filename in os.listdir(directory):
# #         if sub_filename == ".DS_Store":
# #             continue
# #         cur_path = directory+"/"+sub_filename
# #         print(directory+"/"+sub_filename)
# #         # count += 1
# #         temp_feature = shape_dissimilarity(cur_path)
# #         x[sub_filename] = temp_feature
# #         #
# #         # x.append(temp_feature)
# #
# # #
# # with open('test_shapes.pickle', 'wb') as handle:
# #     pickle.dump(x, handle, protocol=pickle.HIGHEST_PROTOCOL)
# #
# # with open('test_shapes.pickle', 'rb') as handle:
# #     b = pickle.load(handle)
#
# # print(x == b)
#
# # print(count)
# shape_dissimilarity("./abstract_selected/abstract/abstract_0005.jpg")