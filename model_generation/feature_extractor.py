# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 11:37:02 2014

@author: luber2
"""

import numpy as np
from math import pow
from skimage import color
from skimage.filter import sobel
from skimage.feature import greycomatrix, greycoprops
from skimage.filter.rank import entropy as get_entropy
from skimage.morphology import disk
from skimage.util import img_as_float
from skimage import io

def get_empty_feature_dict(layer, sp_mask):
    features = dict()
    if (len(layer)!= len(sp_mask)):
        print("mask and picture don't match")
        print layer
        return None
        
    curr_spx = 0
    size = 0
    features[curr_spx] = dict()
    for y in range(len(sp_mask)):
        for x in range(len(sp_mask[0])):
            if sp_mask[y][x] != curr_spx:
                features[curr_spx]['size'] = size
                curr_spx = sp_mask[y][x]
                if curr_spx not in features:
                    features[curr_spx] = dict()
                    size = 1
                else:
                    size = features[curr_spx]['size']
            else: 
                size+=1   
    features[curr_spx]['size'] = size
                
    return features
    
    
def add_statistics(layer, sp_mask, features, feature_name):

    curr_spx_key = 0
    curr_spx_features = features[curr_spx_key]
    mu_count= 0
    spx_min = float('inf')
    spx_max = float('-inf')
        
    for y in range(len(layer)):
        for x in range(len(layer[0])):
            if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features[feature_name + '_mean'] = mu_count
                curr_spx_features[feature_name + '_min'] = spx_min
                curr_spx_features[feature_name + '_max'] = spx_max
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                if (feature_name + '_mean') not in curr_spx_features:
                    mu_count = 0
                    spx_min = float('inf')
                    spx_max = float('-inf')
                else:
                    mu_count = curr_spx_features[feature_name + '_mean']
                    spx_min = curr_spx_features[feature_name + '_min']
                    spx_max = curr_spx_features[feature_name + '_max']
            mu_count += layer[y][x]
            spx_min = min([spx_min, layer[y][x]])
            spx_max = max([spx_min, layer[y][x]])
            
    curr_spx_features[feature_name + '_mean'] = mu_count
    curr_spx_features[feature_name + '_min'] = spx_min
    curr_spx_features[feature_name + '_max'] = spx_max
               
    for spx in features.keys():
        features[spx][feature_name + '_mean']/= features[spx]['size']        
    
    
    #compute var
    var_count = 0
    mu = -1
    for y in range(len(layer)):
        for x in range(len(layer[0])):
            if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features[feature_name + '_var'] = var_count
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                mu = curr_spx_features[feature_name + '_mean']
                if (feature_name + '_var') not in curr_spx_features:
                    var_count = 0
                else:
                    var_count = curr_spx_features[feature_name + '_var']
            var_count += pow(layer[y][x]-mu, 2)
    
    curr_spx_features[feature_name + '_var'] = var_count
        
    for spx in features.keys():
        features[spx][feature_name + '_var']/= features[spx]['size']
    

def to_intensity(pic):
    return np.dot(pic[...,:3], [1, 1, 1])
            
def add_intensity_stats(pic, sp_mask, features):
    i_layer = to_intensity(pic)
    add_statistics(i_layer, sp_mask, features, 'intensity')
            
    
def to_layered(pic):
    r_layer = np.ndarray(shape = (pic.shape[0], pic.shape[1]))
    g_layer = np.ndarray(shape = (pic.shape[0], pic.shape[1]))
    b_layer = np.ndarray(shape = (pic.shape[0], pic.shape[1]))
    for y in range(pic.shape[0]):
        for x in range(pic.shape[1]):
            r_layer[y][x] = pic[y][x][0]
            g_layer[y][x] = pic[y][x][1]
            b_layer[y][x] = pic[y][x][2]
    return [r_layer, g_layer, b_layer]
    
def add_rgb_stats(pic, sp_mask, features):
    layered = to_layered(pic)
    add_statistics(layered[0], sp_mask, features, 'rgb_r')
    add_statistics(layered[1], sp_mask, features, 'rgb_g')
    add_statistics(layered[2], sp_mask, features, 'rgb_b')
    
def add_lab_stats(pic, sp_mask, features):
    lab = color.rgb2lab(pic)
    layered = to_layered(lab)
    add_statistics(layered[0], sp_mask, features, 'lab_l')
    add_statistics(layered[1], sp_mask, features, 'lab_a')
    add_statistics(layered[2], sp_mask, features, 'lab_b')
    return
    
def add_edgeness(name, sp_mask, features):
    edges = sobel(to_intensity(img_as_float(io.imread(name))) )
    
    curr_spx_key = 0
    curr_spx_features = features[curr_spx_key]
    
    edgeness = 0    
    
    for y in range(edges.shape[0]):
        for x in range(edges.shape[1]):
            if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features['edgeness'] = edgeness
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                if 'edgeness' not in curr_spx_features:
                    edgeness = 0
                else:
                    edgeness = curr_spx_features['edgeness']
            edgeness += edges[y][x]
            
    curr_spx_features['edgeness'] = edgeness
            
    for spx in features.keys():
        features[spx]['edgeness']/= features[spx]['size']
        
        
def normaize_by_spx(layer, sp_mask, features):
    
    
    curr_spx_key = 0
    curr_spx_features = features[curr_spx_key]
    coocc_sum = 0
    
    for y in range(sp_mask.shape[0]):
        for x in range(sp_mask.shape[1]):
             if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features['coocc_sum'] = coocc_sum
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                if 'coocc_sum' not in curr_spx_features:
                    coocc_sum = 0
                else:
                    coocc_sum = curr_spx_features['coocc_sum']
             coocc_sum += layer[y][x]
    
    for y in range(sp_mask.shape[0]):
        for x in range(sp_mask.shape[1]):
             if (sp_mask[y][x] != curr_spx_key):
                curr_spx_key = sp_mask[y][x]
                coocc_sum = curr_spx_features[curr_spx_key]['coocc_sum']
                
             layer[y][x]/=coocc_sum
    
    
def add_cooccurrence_features(name, sp_mask, features):
    img = to_intensity(img_as_float(io.imread(name)))
    
    for spx in features.keys():
        range_x = features[spx]['range_x']
        range_y = features[spx]['range_y']
        avg_x = features[spx]['avg_x']
        avg_y = features[spx]['avg_y']
        rad_x = range_x/3
        rad_y = range_y/3
        patch = img[max(avg_y - max(3, rad_y), 0): min(avg_y + max(3, rad_y), img.shape[0]-1), max(avg_x - max(3, rad_x), 0): min(img.shape[1]-1, avg_x + max(3, rad_x))]
        #print patch
        
        coocc = greycomatrix(patch, [5], [0], 256, symmetric=True, normed=True)
        features[spx]['dissimilarity'] = greycoprops(coocc, 'dissimilarity')[0, 0]
        features[spx]['correlation'] = greycoprops(coocc, 'correlation')[0, 0]
        features[spx]['contrast'] = greycoprops(coocc, 'contrast')[0, 0]
        features[spx]['homogeneity'] = greycoprops(coocc, 'homogeneity')[0, 0]
        features[spx]['ASM'] = greycoprops(coocc, 'ASM')[0, 0]
        features[spx]['energy'] = greycoprops(coocc, 'energy')[0, 0]
             
def add_entropy(name, sp_mask, features):

    pic = io.imread(name)
    ent_pic = get_entropy(to_intensity(pic).astype(np.uint8), disk(5)) 
    
    curr_spx_key = 0
    curr_spx_features = features[curr_spx_key]  
    entropy = 0
    
    for y in range(sp_mask.shape[0]):
        for x in range(sp_mask.shape[1]):
             if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features['entropy'] = entropy
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                if 'entropy' not in curr_spx_features:
                    entropy = 0
                else:
                    entropy = curr_spx_features['entropy']
             entropy += ent_pic[y][x]
             
    curr_spx_features['entropy'] = entropy
      
    for spx in features.keys():
        features[spx]['entropy']/=features[spx]['size']

def add_texture_features(name, sp_mask, features):
    add_edgeness(name, sp_mask, features)
    add_entropy(name, sp_mask, features)
    add_cooccurrence_features(name, sp_mask, features)
    return    
    
    
#adds number of area/edge nodes, height, width, average distance from center
def add_geom_features(sp_mask, features):
    
    curr_spx = 0    
    boarder_length = 0
    
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    sum_x = 0
    sum_y = 0
    for y in range(sp_mask.shape[0]):
        for x in range(sp_mask.shape[1]):
            if sp_mask[y][x] != curr_spx:
                features[curr_spx]['boarder_length'] = boarder_length
                features[curr_spx]['min_x'] = min_x
                features[curr_spx]['max_x'] = max_x
                features[curr_spx]['min_y'] = min_y
                features[curr_spx]['max_y'] = max_y
                features[curr_spx]['avg_x'] = sum_x
                features[curr_spx]['avg_y'] = sum_y
                curr_spx = sp_mask[y][x] 
                if 'boarder_length' not in features[curr_spx]:
                    boarder_length = 0
                    min_x = float('Inf')
                    max_x = float('-Inf')
                    min_y = float('Inf')
                    max_y = float('-Inf')
                    sum_x = 0
                    sum_y = 0
                else:
                    boarder_length = features[curr_spx]['boarder_length']
                    min_x = features[curr_spx]['min_x']
                    max_x = features[curr_spx]['max_x']
                    min_y = features[curr_spx]['min_y']
                    max_y = features[curr_spx]['max_y']
                    sum_x = features[curr_spx]['avg_x']
                    sum_y = features[curr_spx]['avg_y']
                    
            # boarders
            if y == 0 or y == sp_mask.shape[0]-1:
                boarder_length +=1
                if x < 1 or (sp_mask[y][x] == sp_mask[y][x-1]):
                    continue
                else:
                    features[sp_mask[y][x-1]]['boarder_length']+=1
                    
            else:
                if (sp_mask[y][x] != sp_mask[y-1][x]):
                    boarder_length+=1
                    features[sp_mask[y-1][x]]['boarder_length']+=1
                    if x < 1 or (sp_mask[y][x] == sp_mask[y][x-1]): 
                        continue
                    else:
                        features[sp_mask[y][x-1]]['boarder_length']+=1
                            
                else:
                    if x < 1 or x == sp_mask.shape[1]-1: 
                        boarder_length+=1
                    else:
                        if (sp_mask[y][x] == sp_mask[y][x-1]):
                            continue
                        else:
                            boarder_length+=1
                            features[sp_mask[y][x-1]]['boarder_length']+=1
                        
            # min, max, sums
            min_x = min([min_x, x])
            max_x = max([max_x, x])
            min_y = min([min_y, y])
            max_y = max([max_y, y])
            sum_x += x
            sum_y += y
           
    features[curr_spx]['boarder_length'] = boarder_length
    features[curr_spx]['min_x'] = min_x
    features[curr_spx]['max_x'] = max_x
    features[curr_spx]['min_y'] = min_y
    features[curr_spx]['max_y'] = max_y
    features[curr_spx]['avg_x'] = sum_x
    features[curr_spx]['avg_y'] = sum_y
           
    for spx in features.keys():
        features[spx]['avg_x']= float(features[spx]['avg_x'])/features[spx]['size']
        features[spx]['avg_y']= float(features[spx]['avg_y'])/features[spx]['size']
        features[spx]['area/boarder'] = features[spx]['size']/features[spx]['boarder_length']
        features[spx]['range_x'] = features[spx]['max_x'] - features[spx]['min_x']
        features[spx]['range_y'] = features[spx]['max_y'] - features[spx]['min_y']
        
    #variance
    var_x = 0
    var_y = 0
    curr_spx_key = 0
    curr_spx_features = features[0]
    mu_x = curr_spx_features['avg_x']
    mu_y = curr_spx_features['avg_y']
    for y in range(len(sp_mask)):
        for x in range(len(sp_mask[0])):
            if (sp_mask[y][x] != curr_spx_key):
                curr_spx_features['var_x'] = var_x
                curr_spx_features['var_y'] = var_y
                curr_spx_key = sp_mask[y][x]
                curr_spx_features = features[sp_mask[y][x]]
                mu_x = curr_spx_features['avg_x']
                mu_y = curr_spx_features['avg_y']
                if 'var_x' not in curr_spx_features:
                    var_x = 0
                    var_y = 0
                else:
                    var_x = curr_spx_features['var_x']
                    var_y = curr_spx_features['var_y']
            var_x += pow(x-mu_x, 2)
            var_y += pow(y-mu_y, 2)
  
    curr_spx_features['var_x'] = var_x
    curr_spx_features['var_y'] = var_y
          
    for spx in features.keys():
        features[spx]['var_x']/= features[spx]['size']
        features[spx]['var_y']/= features[spx]['size']
        
            
# pic must be a 3-dim array 
def get_features(pic, name, sp_mask):
    features = get_empty_feature_dict(pic, sp_mask)
    add_intensity_stats(pic, sp_mask, features)
    add_rgb_stats(pic, sp_mask, features)
    add_lab_stats(pic, sp_mask, features)
    add_geom_features(sp_mask, features)
    add_texture_features(name, sp_mask, features)
    return features