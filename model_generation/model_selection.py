# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 14:33:03 2014

@author: pvijaya2
"""

import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn import svm, tree, grid_search
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from sklearn import cross_validation
from sklearn import metrics


#import sklearn

def get_best_model(filename):

    raw_data = open(filename)
    raw_data.readline()
    data = np.loadtxt(raw_data, delimiter = ',')
    
    y = data[:, -1]
    X = data[:, :-1]
    
    print X.shape
    
    scaler = StandardScaler()
    scaler.fit(X)
    
    scaler.transform(X)
    '''
    pca = PCA()
    pca.fit(X)
    r = sorted(pca.explained_variance_ratio_)
    r.reverse()
    var_explained = 0
    n = 0
    while var_explained < .95:
        var_explained+= r[n]
        n+=1
    n+=1
    print n
    print var_explained    
    pca = PCA(X.shape[1]-n)
    pca.fit_transform(X)
    '''
    
    #svm_params = {'kernel':['rbf'], 'C':[0.1, 1, 10, 100]}
    #svc = svm.SVC()
    #svm_grid_search = grid_search.GridSearchCV(svc, svm_params)
#    svm_grid_search.fit(X, y)
    
    pcpt_params = {'alpha': [0.00001, 0.0001, 0.001, 0.01]}
    pcpt = Perceptron()
    pcpt_grid_search = grid_search.GridSearchCV(pcpt, pcpt_params)
    #pcpt_grid_search.fit(X, y)
    
    lr_params = {'C': [0.1, 1, 10, 100]}
    logreg = LogisticRegression()
    lr_grid_search = grid_search.GridSearchCV(logreg, lr_params)
    #lr_grid_search.fit(X, y)
    
    print 'starting cv'
    
    #scores1 = cross_validation.cross_val_score(svm_grid_search, X, y, cv=5)
    #print 'svm done'
    #print scores1
    #print sum(scores1)/5
    scores2 = cross_validation.cross_val_score(pcpt_grid_search, X, y, cv=5)
    print 'perceptron done'
    print scores2
    print sum(scores2)/5
    scores3 = cross_validation.cross_val_score(lr_grid_search, X, y, cv=5)
    print 'logistic regression done'
    print scores3
    print sum(scores3)/5

    best = np.argmax([scores2, scores3])
    
    if best == 1:
        return pcpt_grid_search
    else:
        return lr_grid_search
    
if __name__ == '__main__':     
    filename = "map_data_test.csv"
    model = get_best_model(filename)
    joblib.dump(model, 'model.pkl')
