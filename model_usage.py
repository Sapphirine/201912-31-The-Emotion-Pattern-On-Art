import pickle
import cv2
import os
import numpy as np
from sklearn.neighbors import KDTree
from feature_extraction import feature_extract

with open('model.pickle','rb') as handle:
    model_dict = pickle.load(handle)

model = model_dict["model"]
scaler = model_dict["scaler"]

def error_measure(x,y,k):
    top_indices_x = np.argsort(np.array(x))[-k:]
    top_indices_y = np.argsort(np.array(y))[-k:]
    error_count = 0
    for i in range(k):
        if top_indices_x[i] != top_indices_y[i]:
            error_count +=1
    
    for i in range(k):
        index = top_indices_x[i]
        if index != top_indices_y[i] and y[index] == y[top_indices_y[i]]:
            error_count-=1
    
    return error_count

def training(X,Y,gamma,C,epsilon):
    avg_error = 0
    best_svr = MultiOutputRegressor(SVR(kernel='rbf',gamma = gamma,C=C,epsilon=epsilon))
    cv = KFold(n_splits=10, random_state=42, shuffle=True)
    for train_index, test_index in cv.split(X):
        X_train, X_test, Y_train, Y_test = X[train_index], X[test_index], Y[train_index], Y[test_index]
        best_svr.fit(X_train, Y_train)
        predicted_y = best_svr.predict(X_test)
        
        cur_error= 0 
        for i in range(X_test.shape[0]):
            cur_error += error_measure(predicted_y[i],Y_test[i],3)
            
        avg_error = cur_error/X_test.shape[0]
    return best_svr,avg_error/10

#parameter tunning
def tunning(X,Y)
    C_range = np.linspace(0.01, 1,20)
    gamma_range = np.linspace(0.01,100,300)
    small_error = 1
    value=[0,0] #C,gamma
    count = 0
    total_runs = len(C_range)*len(gamma_range)
    for c in C_range:
        for g in gamma_range:
            count += 1
            print("finish(%):",round(count*100/total_runs,2))
            model,avg_error = training(X,Y,g,c,0.05)
            y_predict = model.predict(X)
            #update the parameter
            if avg_error < small_error:
                small_error = avg_error
                value[0] = c
                value[1] = g