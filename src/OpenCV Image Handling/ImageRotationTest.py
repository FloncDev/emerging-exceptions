# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:46:31 2023

@author: olive
"""

import PIL
from PIL import Image
from PIL import ImageFilter
import numpy as np

def black_white(img_path):
    with Image.open(img_path) as im:
        arr = np.array(im)

        r = arr[:,:,0]
        r2 = np.array(r.copy(), "int32")
        g = arr[:,:,1]
        g2 = np.array(g.copy(), "int32")
        b = arr[:,:,2]
        b2 = np.array(b.copy(), "int32")
        
        black = r2+g2+b2

        for i in range(black.shape[0]):
            for j in range(black.shape[1]):
                if black[i,j] < 125:
                    black[i,j] = 255
                else:
                    black[i,j] = 0
                    
        black2 = np.array(black.copy(), "uint8")
        black_img = Image.fromarray(black2)
        black_img = black_img.filter(ImageFilter.MinFilter(5))
        return black_img
    
def find_right_angle(img):
    arr = np.array(img)
    
    cornerx = 0
    corner_y = 0
    
    cornery = 0
    corner_x = 0
        
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if arr[x,y] == 255:
                if cornerx < x or cornerx == 0:
                    cornerx = x
                    corner_y = y
                if cornery > y or cornery == 0:
                    cornery = y
                    corner_x = x

    print(f"{cornerx =} {cornery =} {corner_x =} {corner_y =}")
    vert_len = corner_y-cornery    
    hor_len = corner_x-cornerx
    tan_angle = vert_len / hor_len
    anglerad = np.arctan(tan_angle)
    angle = anglerad * 180 / np.pi
    img = img.rotate((angle))
    print(angle)


    return img, angle

def crop_and_rotate_to_L(img):
    img = img.filter(ImageFilter.MinFilter(3))
    arr = np.array(img)
    firstx = 0
    firsty = 0
    lastx = 0
    lasty = 0
    
    
    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if arr[x,y] == 255:
                if x < firstx or firstx == 0:
                    firstx = x
                if y < firsty or firsty == 0:
                    firsty = y
                if x > lastx:
                    lastx = x
                if y > lasty:
                    lasty = y
            else:
                continue
                    

    box = (min(firsty,lasty),min(firstx,lastx),max(lasty,firsty),max(lastx,firstx))
    
    

    img = img.crop(box)
    arr2 = np.array(img)
    img = Image.fromarray(arr2)
    
    # maxx = arr2.shape[0]
    # maxy = arr2.shape[1]
    
    # rot_num = 0
    # while arr2[(maxx-1),1] != 0:

    #     img = img.rotate(90)
    #     arr2 = np.array(img)
    #     rot_num = rot_num + 1
        
    # img = img.rotate(90)
    # img = img.rotate(90)
    # rot_num = rot_num + 2
    
    return img, box #, rot_num,  arr2

def centre_and_crop_img(img_path):
    black_img = black_white(img_path)
    rot_black, angle = find_right_angle(black_img)
    final_img , box = crop_and_rotate_to_L(rot_black)
    with Image.open(img_path) as im:
        img = im.rotate(angle)
        img = img.crop(box)
        if angle < -45:
            img = img.rotate(90,0,1)
        
    return img

def resize_and_colour_correct(img):
    img = img.resize((33,34),0)
    img = img.crop((1,1,33,33))
    arr = np.array(img)
    r = arr[:,:,0]
    g = arr[:,:,1]
    b = arr[:,:,2]
    for x in range(32):
        for y in range(32):
            if r[x,y] > g[x,y] and r[x,y] > b[x,y]:
                r[x,y] = 255
                g[x,y] = 0
                b[x,y] = 0
            elif g[x,y] > r[x,y] and g[x,y] > b[x,y]:
                r[x,y] = 0
                g[x,y] = 255
                b[x,y] = 0
            elif b[x,y] > r[x,y] and b[x,y] > g[x,y]:
                r[x,y] = 0
                g[x,y] = 0
                b[x,y] = 255
    
    r_channel = Image.fromarray(r, "L")
    g_channel = Image.fromarray(g, "L")
    b_channel = Image.fromarray(b, "L")
    
    bands = (r_channel,g_channel,b_channel)
    new_image = Image.merge("RGB", bands)
    
    return new_image