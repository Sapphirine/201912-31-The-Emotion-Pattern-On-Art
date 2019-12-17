import cv2
import math

def find_angle(degree):
    diff = degree
    index = 0
    standard_angles = [0,15,30,45,60,75,90,105,120,135,150,165]
    for i in range(len(standard_angles)):
        if abs(degree - standard_angles[i]) < diff:
            diff = abs(degree-standard_angles[i])
            index = i
            
    return index

# def calc_directions(lines):
#     angles = [0,0,0,0,0,0,0,0,0,0,0,0] #(0,15,30,45,60,75,90,105,120,135,150,165)
#     for i in lines:
#         for x1,y1,x2,y2 in i:
#             degree = math.degrees(math.atan2(y2-y1,x2-x1))
#             if degree < 0:
#                 degree += 180
#             angles[find_angle(degree)] +=1

#     total_lines = len(lines)
#     min_val = total_lines
#     max_val = 0
#     sum_angles = 0
#     for j in range(len(angles)):
#         sum_angles += j*15*angles[j]
        
#     mean = sum_angles/total_lines
#     variance = 0
#     for j in range(len(angles)):
#         variance += (j*15-mean)*(j*15-mean)*angles[j]
    
#     variance /= total_lines
#     return variance #smaller the variance, less messy

def calc_directions(lines):
    count_static_lines = 0
    length_static = 0
    length_dynamic = 0
    for i in lines:
        for x1,y1,x2,y2 in i:
            degree = math.degrees(math.atan2(y2-y1,x2-x1))
            if degree < 0:
                degree += 180
                
            if degree <= 15 or degree >= 165:
                count_static_lines += 1
                length_static += math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
            elif degree <= 105 and degree >= 75:
                count_static_lines += 1
                length_static += math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
            else:
                length_dynamic += math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    
    total_lines = len(lines)
    line_feature = [count_static_lines/total_lines,(total_lines - count_static_lines)/total_lines]
    if count_static_lines != 0:
        line_feature.append(length_static/count_static_lines)
    else:
        line_feature.append(0)

    if total_lines - count_static_lines != 0:
        line_feature.append(length_dynamic/(total_lines - count_static_lines))
    else:
        line_feature.append(0)
        
    return line_feature

def composition(img):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img_gray,30,200)
    edge_count = 0
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i][j] == 255:
                edge_count +=1
    edge_count /= edges.shape[0] * edges.shape[1]
    minLineLength = 80
    maxLineGap = 15
    lines = cv2.HoughLinesP(edges,0.3,math.pi/180,50,minLineLength,maxLineGap)
    if lines is None or len(lines) == 0:
        messy_order = [0,0,0,0] 
    else:
        messy_order = calc_directions(lines) 
    
    composition_feature = messy_order + [edge_count]
    return composition_feature#5d