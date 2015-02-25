# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 22:27:07 2014

@author: jordan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 21:04:03 2014

@author: luber2/pvijaya2
"""

import os
import sys
import csv
from PIL import Image
import numpy as np

from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io

import feature_extractor

def segment(dataset_folder):    
    seg_dict = dict()
    if os.path.isdir("bob"):
        for file in os.listdir(dataset_folder):
            filename = dataset_folder + "/" + file
            print filename
            image = img_as_float(io.imread(filename))
            num_segments = 1000
            segments = slic(image, n_segments = num_segments, sigma = 3)
            
            seg_dict[filename] = segments
    else:
        image = img_as_float(io.imread(dataset_folder))
        num_segments = 1000
        segments = slic(image, n_segments = num_segments, sigma = 3)
        seg_dict[dataset_folder] = segments    
        
    return seg_dict 
    
def extract_features(image_dict, seg_dict):
    features = dict()
    for image_name in image_dict.keys():
        print image_name
        features[image_name] = feature_extractor.get_features(image_dict[image_name], image_name, seg_dict[image_name])
    
    return features
    
def PIL2array(img):
    return np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    
def generate_data(ds_folder):
    seg_dict = segment(ds_folder)
    image_dict = dict()
    for filename in seg_dict.keys():
        im = Image.open(filename)
        im = im.convert(mode="RGB")
        image_dict[filename] = PIL2array(im)
    features = extract_features(image_dict, seg_dict)
    
    print 'Saving to File...'
    filename = ''
    with open('map_data.csv', 'w') as csvfile:
        filename = csvfile
        fieldnames = features[features.keys()[0]][0].keys()
        fieldnames.append('label')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for pic_id in features.keys():
            for spx_id in features[pic_id].keys():
                row = features[pic_id][spx_id]
                row['label'] = '?'
                writer.writerow(row)
    return filename  
     
if __name__ == '__main__': 
    
    ds_folder = None
    if len(sys.argv) > 1:
        ds_folder = sys.argv[1]    
    else: 
        ds_folder = "/home/jordan/School/CS446/Project/map_data"
    
    filename = generate_data(ds_folder) 
    print filename

