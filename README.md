Satellite Image-to-Map Generation Project
===================

Generates maps from satellite photos.

**data_collection/**
Folder to extract data from Google Maps API. We can filter the map image generation by State in the getmapimages.py

**model_generation/**
Scripts used to generate training data and using training model. We used Weka to generate decforests2.model which is a Random Forest implementation. To generate prediction images, load map_data/ with satellite data of 800x800 satellite \
images(containing "satellite" in the filename), and then run python train_test.py. The map generation images from the model will be generated in the map_data/ folder. To change the model being used we have to use weka to generate a mode\
l and change the model location string in predict.java and recompile the class. Then re-run python train_test.py.

**mapgen_results/**
Results of test map generation runs from initial phase of model testing and evaluation. There are 3 runs displayed here.

**

Paper on Research Project
-----------------
[Automated Map Generation Project Paper](https://docs.google.com/a/illinois.edu/file/d/0B0nnyKjxQ-U-ODVpeVVFR252RHc/edit)

Sample Generated Results
-----------------
![enter image description here](https://lh5.googleusercontent.com/-kOV5Hi-2954/VOuC7LtRc-I/AAAAAAAAAC4/q5WYgiWZwvA/s0/Columbus_Georgia_satellite.png "Columbus_Georgia_satellite.png")

![enter image description here](https://lh6.googleusercontent.com/-VThDmT8K0_E/VOuDEfYporI/AAAAAAAAADE/vvjuaZChY9E/s0/Columbus_Georgia_satellite._mask.bmp "Columbus_Georgia_satellite._mask.bmp")

![enter image description here](https://lh5.googleusercontent.com/-5HemnI9lcN4/VOuDP2D6n8I/AAAAAAAAADQ/XkmL8LkoSEs/s0/Colchester_Vermont_satellite.png "Colchester_Vermont_satellite.png")

![enter image description here](https://lh3.googleusercontent.com/-fUnAg7Vv5CQ/VOuDVDe3muI/AAAAAAAAADg/hRRL3zFcWls/s0/Colchester_Vermont_satellite._mask.bmp "Colchester_Vermont_satellite._mask.bmp")

![enter image description here](https://lh5.googleusercontent.com/-LQDLxM5JB4U/VOuDnhzLMJI/AAAAAAAAAD0/4_6XpxETm2A/s0/Saginaw_Michigan_satellite.png "Saginaw_Michigan_satellite.png")

![enter image description here](https://lh4.googleusercontent.com/-je-i3CiQM4I/VOuDshFK8VI/AAAAAAAAAEA/6P4fQ8hKSBo/s0/Saginaw_Michigan_predicted.png "Saginaw_Michigan_predicted.png")

![enter image description here](https://lh3.googleusercontent.com/-5j7lVAQyyLk/VOuB-mRFhYI/AAAAAAAAABY/C0UIOHWa8vo/s0/Lawrenceville_Georgia_satellite.png "Lawrenceville_Georgia_satellite.png")

![enter image description here](https://lh3.googleusercontent.com/-QQDVW1FUIFE/VOuCH5YA4BI/AAAAAAAAABw/ejUZQSkxtec/s0/Lawrenceville_Georgia_satellite._mask.png "Lawrenceville_Georgia_satellite._mask.png")

![enter image description here](https://lh6.googleusercontent.com/-b8DvwfTizUc/VOuBKbjFh_I/AAAAAAAAAAw/p4hvxCfdbD4/s0/McKinney_Texas_satellite.png "McKinney_Texas_satellite.png")

![enter image description here](https://lh4.googleusercontent.com/-Hu9J2VCCCsc/VOuBGcAr3XI/AAAAAAAAAAk/v2JGfLbgaqw/s0/McKinney_Texas_predicated.png "McKinney_Texas_predicated.png")

