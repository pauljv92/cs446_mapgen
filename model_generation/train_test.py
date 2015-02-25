# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 19:06:26 2014

@author: pvijaya2
"""
import os
import csv
from PIL import Image
import numpy as np

from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io

import train_withmaxcolor2
import feature_extractor
import model_selection
import weka.core.serialization as serialization
from weka.classifiers import Classifier
from weka.core.dataset import Instances
import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver
from subprocess import call
import predict_weka as predweka

#from sklearn.externals import joblib

def segment(dataset_file):
    seg_dict = dict()
    if os.path.isdir("bob"):
        for file in os.listdir(dataset_file):
            filename = dataset_file + "/" + file
            print filename
            image = img_as_float(io.imread(filename))
    
            num_segments = 1000
            segments = slic(image, n_segments = num_segments, sigma = 3)
            seg_dict[filename] = segments
    else:
        print("correct")
        filename = dataset_file
        image = img_as_float(io.imread(dataset_file))
        num_segments = 1000
        segments = slic(image, n_segments = num_segments, sigma = 3)
        seg_dict[dataset_file] = segments    
        
    return seg_dict 

def extract_features(image_dict, seg_dict):
    features = dict()
    for image_name in image_dict.keys():
        print image_name
        features[image_name] = feature_extractor.get_features(image_dict[image_name], image_name, seg_dict[image_name])
    
    return features
    
def PIL2array(img):
    return np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    
def generate_data(ds_file):
    seg_dict = segment(ds_file)
    image_dict = dict()
    #Loop through each satellite image superpixel set
    for filename in seg_dict.keys():
        im = Image.open(filename)
        im = im.convert(mode="RGB")
        image_dict[filename] = PIL2array(im)
    features = extract_features(image_dict, seg_dict)
    print 'Generating Labels...'
    #labels = train_withmaxcolor2.get_training_labels(ds_folder)
    
    print("Obtained Labels")
    '''    
    for image in labels.keys():
        for spx in labels[image].keys():
            features[image][spx]['label'] = labels[image][spx]
    '''
    print('Saving to File...')
    filename = ''
    i = 1
    with open('map_testdata.csv', 'w') as csvfile:
        #filename = csvfile
        fieldnames = features[features.keys()[0]][0].keys()
        fieldnames.append('label')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pic_id in features.keys():
            for spx_id in features[pic_id].keys():
                row = features[pic_id][spx_id]
                row['label'] = i
                i = (i%4)+1
                writer.writerow(row)
    return seg_dict
    
def trainClassifier(filename):    
    return model_selection.get_best_model(filename)
     
if __name__ == '__main__': 

    ds_folder = str(os.getcwd())+"/map_data"
    print(ds_folder)
    
    for ds_file in os.listdir(ds_folder):
        if "satellite" in ds_file:
            ds_file = str(ds_folder)+"/"+str(ds_file)
            print(ds_file)
            seg_dict = generate_data(ds_file)
            call("java -classpath weka.jar: predict",shell=True) #call predict.class to generate preds.csv using the model
            predweka.generate_prediction_image(ds_file,seg_dict)
    #classifier = trainClassifier(filename)
    #joblib.dump(classifier, 'mapper.pkl') 
    
