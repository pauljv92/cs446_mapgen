# -*- coding: utf-8 -*-
"""
Created on Tues Nov 17 20:06:26 2014

@author: pvijaya2
"""
import os

#import cv2
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io
import scipy.spatial as sp
from PIL import Image

def segment(dataset_folder):

    image_dict = dict()    
    for file in os.listdir(dataset_folder):
        filename = dataset_folder + "/" + file;
        if "satellite" in filename:
            image = img_as_float(io.imread(filename))
            num_segments = 1000
            segments = slic(image, n_segments = num_segments, sigma = 3)
            spxls = dict()
            for row in range(segments.shape[0]):
                for column in range(segments.shape[1]):
                    spid = segments[row][column]
                    if not spxls.has_key(spid):
                        spxls[spid] = set()
                    pos = (row, column)
                    spxls[spid].add(pos)
                
            image_dict[filename] = spxls

    return image_dict


def rgb2hex(rgb):
    return '%02x%02x%02x' % rgb

def getsptopcolor(filename,listofcoords,tree,mapped_colors):
    #classes = {A: Roads, B: Buildings, C:Water_Bodies, D:Other(Forests etc.)}
    #mapped_colors = [(255, 255, 255),(240,240,240),(204,204,204),(153,204,255),     #(102,255,102),(255,204,102),(255,255,204),(204,255,204),(255,153,51),
    #(225,225,225),(255,204,204),(204,225,176),(225,225,176),(240,240,225)] # list of web-save colors

    #(255,255,255) = Roads (White) (FFFFFF) - Class A
    #(240,240,240) = Tall Buildings (F0F0F0) - Class B
    #(204,204,204) = Buildings (Grey) (CCCCCC) - Class B
    #(153,204,255) = Sea/Lakes (Light Blue) - (99CCFF) - Class C
    #(102,255,102) = Green land (Green) - (66FF66) - Class D
    #(255,204,102) = Highways (Orange/Yellow) (FFCC66) - Class A   
    #(255,255,204) = Sand/Roads (Light Yellow) -(FFCC66) - Class A
    #(204,255,204) = Greenland/Parks (Light Green) - (CCFFCC) -Class D
    #(255,153,51) = Large Highways (Dark Orange) - (FF9933) - Class A
    #(225,225,225) = Darker Area Around Buildings (Dark Grey) - Class D
    #(255,204,204) = Area around Hospitals (Pink) - (FFCCCC) - Class D
    #(204,225,176) = Park Area (Govt) (Dirty Green) - (CCE1B0) - Class D
    #(225,225,176) = Dirt Ground (Light Brown) - Class D
    #(240,240,225) = Tall Buildings2 - Class B

    classa = [(255,255,255),(255,204,102),(255,255,204),(255,153,51)] #roads
    classb = [(204,204,204),(240,240,240),(240,240,225)] #buildings
    classc = [(153,204,255)] # water
    classd = [(102,255,102),(204,255,204),(225,225,225),(255,204,204),(204,225,176),(225,225,176)] #other 
    classes = {"1":classa, "2":classb, "3":classc,"4":classd}

    im = Image.open(filename);
    pix = im.convert('RGB')

    colors = {}
    for x,y in listofcoords:
        input_color = pix.getpixel((x,y))
        distance, result = tree.query(input_color) # get Euclidean distance and index of web-save color in tree/list
        nearest_color = mapped_colors[result]
        hexcolor = rgb2hex(nearest_color)
        for Class in classes.keys():
            if nearest_color in classes[Class]:
                hexcolor = Class
                break

        #Hex color is the class of the pixel (A,B,C,D)
        #print("Pixel hexcolor ->"+hexcolor)
        if hexcolor in colors.keys():
            if hexcolor == "1":
                colors[hexcolor] += 1.7
            else:
                colors[hexcolor] += 1.0
        else:
            if hexcolor == "1":
                colors[hexcolor] = 1.7
            else:
                colors[hexcolor] = 1.0
            
    return max(colors.iterkeys(), key=lambda k: colors[k])

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
    
def towebsafecolors(rgbhex):
    r,g,b = hex_to_rgb(rgbhex)
    rw = 51 * ((int(r)+25)//51)
    gw = 51 * ((int(g)+25)//51)
    bw = 51 * ((int(b)+25)//51)
    return (rw,gw,bw)

def getroadmapimgs(dataset_folder,image_dict,tree,mapped_colors):
    image_labels = dict()
    #for img in image_dict:
    #    print(img)
    for file in os.listdir(dataset_folder):
        filename = dataset_folder + "/" + file
        if "roadmap" in filename:
            sfilename = filename.replace("roadmap","satellite")
            #image = img_as_float(io.imread(filename))
            print("Filename: "+filename)
            print("SFilemame: "+sfilename)
            image_labels[sfilename] = dict()
            #print("THIS IS image_dict: "+str(image_dict[sfilename]))
            for spxl in image_dict[sfilename]:
                image_labels[sfilename][spxl] = getsptopcolor(filename, image_dict[sfilename][spxl],tree,mapped_colors)
            
    return image_labels
    
def get_training_labels(folder):
    print("Currently getting Labels");
    image_dict = segment(folder)
    print("Extracted superpixels")
    print(image_dict.keys())
    #print(image_dict.values())
    
    #list of web-save colors
    mapped_colors = [(255,255,255),(240,240,240),(204,204,204),(153,204,255),(102,255,102),(255,204,102),(255,255,204),(204,255,204),(255,153,51),(225,225,225),(255,204,204),(204,225,176),(225,225,176),(240,240,225)] 
    tree = sp.KDTree(mapped_colors) # creating k-d tree from web-save colors
    roadimage_labels = getroadmapimgs(folder,image_dict,tree,mapped_colors)
    image_tc_dist = {}
    labels = dict()
    
    #print(roadimage_labels);
    for rd in roadimage_labels:
        rdmap = set(roadimage_labels[rd].values())
        print(rd) #roadmap filename
        print(rdmap) #labels of superpixels
        print(len(rdmap)) #number of superpixels

    return roadimage_labels

    '''
    for image_name in image_dict.keys():
        labels[image_name] = dict()
        img_labels = labels[image_name]
        for spx_id in image_dict[image_name].keys():
            topcolor = getsptopcolor(image_name, image_dict[image_name][spx_id])
            if topcolor in image_tc_dist:
                img_labels[spx_id] = image_tc_dist[topcolor]
            else:
                img_labels[spx_id] = 'other'
                
            
            if topcolor in image_tc_dist:
                image_tc_dist[topcolor] += 1
            else:
                image_tc_dist[topcolor] = 1
            
    print len(labels)
    return labels
'''
     
if __name__ == '__main__':

    #dictionary of images indexed by filename. Each filename
    #maps to a dictionary of superpixel_ids as the key and a list of
    #pixel coordinates as the values
    image_dict = segment("map_data")
    image_tc_dist = {}

    '''
    #Do not run this for now.
    for image in image_dict:
        for superpix in image:
            topcolor = getsptopcolor(image[superpix],image)
            if topcolor in image_tc_dist:
                image_tc_dist[topcolor] += 1
            else:
                image_tc_dist[topcolor] = 1
    '''
    #test input for function
    #print getsuperpixeltopcolor("mapdata/Joliet_Illinois_roadmap.jpg",[(0,0),(20,20),(40,40),(80,80)])

    #features = extract_features(image_dict)
    #training_set = get_training(image_dict)
    
    #classifier = trainClassifier()
    
    #joblib.dump(classifier, 'mapper.pkl') 
    
