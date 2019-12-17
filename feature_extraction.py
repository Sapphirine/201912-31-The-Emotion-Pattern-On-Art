import cv2
import pickle
from color import color
from texture import texture
from composition import composition
from shape import shape_dissimilarity
import os
import csv
import math
import numpy as np
import threading
from collections import defaultdict

def feature_extract(img_path):
    img = cv2.imread(img_path)
    aspect_ratio = img.shape[0]/img.shape[1]
    # print(aspect_ratio)
    total_pixels = 2e5
    height = int(math.sqrt(total_pixels/aspect_ratio))
    width = int(height*aspect_ratio)
    resized = cv2.resize(img, (height, width), interpolation=cv2.INTER_AREA)
    denoised = cv2.GaussianBlur(resized, (5, 5), 0)
    # cv2.imshow('t', denoised)
    # cv2.waitKey(0)
    f1 = color(denoised)
    f2 = texture(denoised)
    f3 = composition(denoised)
    try:
        f4 = shape_dissimilarity(denoised)
    except:
        print('ERROR in shape: ', img_path)

    return f1 + f2 + f3 + f4


def predictByArtist(directory):
    x = dict()
    for sub_filename in os.listdir(directory):
        if sub_filename == ".DS_Store":
            continue
        cur_path = directory + "/" + sub_filename
        print(directory + "/" + sub_filename)
        temp_feature = feature_extract(cur_path)
        emotion_score = model.predict(scaler.transform([temp_feature]))
        x[sub_filename] = emotion_score

    pickle.dump(x, open('./model_results/'+directory.split('/')[2], "wb"))




if __name__ == "__main__":
    with open('model.pickle', 'rb') as handle:
        model_dict = pickle.load(handle)

    model = model_dict["model"]
    scaler = model_dict["scaler"]
    emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"]

    directory = "./paintings"
    for sub_foldername in os.listdir(directory):
        if sub_foldername not in os.listdir('./model_results'):
            print(sub_foldername)
            predictByArtist(directory + '/' + sub_foldername)

