# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 21:36:04 2014

@author: luber2/pvijaya2
"""
import os
import sys
import numpy as np
from PIL import Image
from skimage.util import img_as_float
from skimage import io
from skimage.segmentation import slic

from generate_csv_weka import generate_data
import matplotlib.pyplot as plt

def segment(ds_folder):

    seg_dict = dict()
    for file in os.listdir(ds_folder):
        filename = ds_folder + "/" + file
        print filename
        image = img_as_float(io.imread(filename))
        
        num_segments = 1000
        segments = slic(image, n_segments = num_segments, sigma = 3)
        seg_dict[filename] = segments
    return seg_dict


def generate_prediction_image(filename,seg_dict):
    fn = "preds.csv"
    raw_data = open(fn)
    labels = np.loadtxt(raw_data, delimiter = ',')

    seg = seg_dict[filename]    
    mask = np.zeros(seg.shape)
    for y in range(seg.shape[0]):
        for x in range(seg.shape[1]):
            mask[y,x] = labels[seg[x,y]]*50
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 2))
    ax1.imshow(Image.open(filename))
    ax1.axis('off')
    ax1.set_title('Initial Image', fontsize=20)
    
    ax2.imshow(mask, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Mask', fontsize=20)
    fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                        bottom=0.02, left=0.02, right=0.98)
    
    #plt.show()
    saved = Image.fromarray((mask * 255).astype(np.uint8))
    saved.save(filename[:-3] + '_mask.bmp')


if __name__ == '__main__': 
    
    '''
    ds_folder = None 
    if len(sys.argv) > 1:
        ds_folder = sys.argv[1]
    else: 
        ds_folder = "/home/jordan/School/CS446/Project/map_data"
        
    fn = "preds.csv"
    raw_data = open(fn)
    labels = np.loadtxt(raw_data, delimiter = ',')
    seg_dict = segment(ds_folder)

    seg = seg_dict[ds_folder]
    
    mask = np.zeros(seg.shape)
    for y in range(seg.shape[0]):
        for x in range(seg.shape[1]):
            mask[y,x] = labels[seg[y,x]]*50
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(8, 2))
    ax1.imshow(Image.open(ds_folder))
    ax1.axis('off')
    ax1.set_title('Initial Image', fontsize=20)
    
    ax2.imshow(mask, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Mask', fontsize=20)
    fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                        bottom=0.02, left=0.02, right=0.98)
    
    plt.show()
    saved = Image.fromarray((mask * 255).astype(np.uint8))
    saved.save(ds_folder[:-3] + '_mask.bmp')
    '''
    
