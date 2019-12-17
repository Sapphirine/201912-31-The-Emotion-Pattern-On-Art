from pyemd import emd
import numpy as np
import cv2
import math
#didn't implement the contrast sub-feature yet

def d(a,b):
    b_a = int( a / 16 )
    g_a = int( (a - b_a*16) / 4 )
    r_a = int( a - b_a*16 - g_a*4 )
    b_a = b_a*64 + 32
    g_a = g_a*64 + 32
    r_a = r_a*64 + 32
    
    b_b = int( b / 16 )
    g_b = int( (b - b_b*16) / 4 )
    r_b = int( b - b_b*16 - g_b*4 )
    b_b = b_b*64 + 32
    g_b = g_b*64 + 32
    r_b = r_b*64 + 32
    
    array_a = np.zeros(shape=(1,1,3),dtype=np.uint8)
    array_a[0][0][0] = b_a
    array_a[0][0][1] = g_a
    array_a[0][0][2] = r_a
    array_a = cv2.cvtColor(array_a, cv2.COLOR_BGR2LUV)
    array_a = array_a.astype(int)
    
    array_b = np.zeros(shape=(1,1,3),dtype=np.uint8)
    array_b[0][0][0] = b_b
    array_b[0][0][1] = g_b
    array_b[0][0][2] = r_b
    array_b = cv2.cvtColor(array_b, cv2.COLOR_BGR2LUV)
    array_b = array_b.astype(int)
    return np.linalg.norm(array_a-array_b)

def color(img):
    #calculate the S,V related feature of the img
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = np.mean(img_hsv[:,:,1])
    saturation_std = np.std(img_hsv[:,:,1])
    brightness = np.mean(img_hsv[:,:,2])
    brightness_std = np.std(img_hsv[:,:,2])
    pleasure = 0.69*brightness + 0.22 * saturation
    arousal = -0.31 * brightness + 0.6 * saturation
    dominance = 0.76 * brightness + 0.32 * saturation


    #calculate Hue related feature
    n = img_hsv.shape[0] * img_hsv.shape[1]
    A = 0
    B = 0
    A_Satur = 0
    B_Satur = 0
    for i in range(img_hsv.shape[0]):
        for j in range(img_hsv.shape[1]):
            A += math.cos(img_hsv[i][j][0]*np.pi/90)
            A_Satur += img_hsv[i][j][1] * math.cos(img_hsv[i][j][0]*np.pi/90)
            
            B += math.sin(img_hsv[i][j][0]*np.pi/90)
            B_Satur += img_hsv[i][j][1] * math.sin(img_hsv[i][j][0]*np.pi/90)
    if A == 0:
        mean_hue = 0
    else:
        mean_hue = np.arctan(B/A)*180/np.pi
    
    if A_Satur == 0:
        mean_hue_saturation_weighted = 0
    else:
        mean_hue_saturation_weighted =  np.arctan(B_Satur/A_Satur)*180/np.pi
    
    dispersion = math.sqrt(A*A+B*B)/n
    dispersion_saturation_weighted = math.sqrt(A_Satur*A_Satur+B_Satur*B_Satur)/n

    #calculate the histogram of the image, D1 servers as the uniform distributed image
    D1 = np.ones(64)
    D1 /= 64
    D2 = np.zeros(64)

    for i in range(0,img.shape[0]): 
        for j in range(0,img.shape[1]):
            temp_color = img[i][j]
            b = int(temp_color[0]/64)
            g = int(temp_color[1]/64)
            r = int(temp_color[2]/64)
            D2[b*16 + g*4 + r] += 1
    D2 /= img.shape[0]*img.shape[1]


    #calculate the distance matrix used to do emd calculation
    distance_matrix = np.zeros((64,64))    
    for i in range(0,64):
        for j in range(0,64):
            distance_matrix[i][j] = d(i,j)
    
    colorfulness = emd(D1,D2,distance_matrix) #contains more color, value is smaller

    color_feature = [saturation,saturation_std,brightness,brightness_std,pleasure,\
        arousal,dominance,mean_hue,dispersion,mean_hue_saturation_weighted, dispersion_saturation_weighted,\
            colorfulness]

    return color_feature#12d