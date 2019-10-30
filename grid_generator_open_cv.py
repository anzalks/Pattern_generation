#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:23:35 2019

@author: anzal
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

#print("please enter the grid height Eg: for a 29x25 sized grid write 29 as height")
#array_height = int(input())
#
#print("please enter the grid width Eg: for a 29x25 sized grid write 25 as width")
#array_width = int(input())
#
#print('how many grid points should light up in the pattern at once? eg: if you need 5 points of a 29x25 grid to be lit input 5')
#number_of_grids_lit =  int(input())
#
#print('what is the spacing you prefer between grid points which are lit?')
#grid_spacing = int(input())

array_height = 7
array_width = 5
number_of_grids_lit = 3
grid_spacing = 2

len_array = array_height*array_width
image_array = np.zeros(len_array,dtype = np.uint8)
I = np.arange(len(image_array))
print(I)

rand_ind = np.random.choice(I, number_of_grids_lit, replace=False)
assert len(rand_ind) == number_of_grids_lit
image_array[rand_ind] = 1
image_array = image_array.reshape(array_height,array_width)

total = image_array.copy()
index_of_1 = []
for i in range(20):
    np.random.shuffle(image_array)
    random = index_of_1
    index_of_1 = np.array(np.where(image_array==1))
    try:
        print(index_of_1)
        print(',,,')
        print(random)
        if index_of_1[0] == random:
            print('....')
    except:
        pass
    total += image_array
    plt.imshow(image_array)
    plt.show()
    plt.close()
    

























#indices_list = []
#while np.sum(image_array)< 255*number_of_grids_lit:
#    print(np.sum(image_array))
#    random_row, random_column = int(np.random.randint(0,array_height,1)), int(np.random.randint(0,array_width,1))
#    print([random_row, random_column])
#    print(np.ravel(image_array[random_row-grid_spacing:random_row+grid_spacing+1, random_column-grid_spacing:random_column+grid_spacing+1]))
#    if 255 in np.ravel(image_array[random_row-grid_spacing:random_row+grid_spacing+1, random_column-grid_spacing:random_column+grid_spacing+1]):
#        print('yes its there')
#        pass
#    else:
#        image_array[random_row, random_column] = 255
#        indices_list.append([random_row, random_column])
#    print(indices_list)
#    print(image_array)
#    imshow_plt(image_array) 
#
#
##imshow_plt
##
##cv2.imshow("Color Image",image_array)
##
##
##cv2.waitKey(0)
##cv2.destroyAllWindows()
#
#
