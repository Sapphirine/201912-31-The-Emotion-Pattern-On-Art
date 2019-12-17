import cv2
from skimage.feature import greycomatrix, greycoprops

def texture(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    glcm = greycomatrix(img_gray, [5], [0], 256, symmetric=True, normed=True)
    contrast = greycoprops(glcm, 'contrast')[0][0]
    correlation = greycoprops(glcm,'correlation')[0][0]
    energy = greycoprops(glcm,'energy')[0][0]
    homo = greycoprops(glcm,'homogeneity')[0][0]
    dissimilarity = greycoprops(glcm,'dissimilarity')[0][0]
    texture_feature = [contrast,correlation,energy,homo,dissimilarity]
    return texture_feature
    #5d