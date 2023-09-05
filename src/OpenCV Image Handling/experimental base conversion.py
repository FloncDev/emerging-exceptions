# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:47:18 2023

@author: olive
"""

import math
import PIL
from PIL import Image
import random
import lorem
import cv2
import time
import numpy

def str_to_colour_list2(SecretMsg: str):
    r_colour = (255,0,0)
    g_colour = (0,255,0)
    b_colour = (0,0,255)
    m_colour = (255,0,255)
    c_colour = (0,255,255)
    y_colour = (255,255,0)
    w_colour = (255,255,255)
    colour_list = []
    base_3_list = []
    
    str_integer_list = list(SecretMsg.encode('utf-8'))
    print(f"{str_integer_list =}")
    for a in str_integer_list:
        base_3_num = baseconvert2(a,3)
        base_3_num = base_3_num.zfill(5)
        base_3_list.append(base_3_num)
        
    base_3_list.append("00010")
    
    print(base_3_list)
        
    for j in str(base_3_list):
        if j == "0":
            colour_list.append(r_colour)
        elif j == "1":
            colour_list.append(g_colour)
        elif j == "2":
            colour_list.append(b_colour)
        elif j == "3":
            colour_list.append(m_colour)
        elif j == "4":
            colour_list.append(c_colour)
        elif j == "5":
            colour_list.append(y_colour)
    
    return colour_list
        

   

def baseconvert2(num: int, base: int) -> str:
    if base == 10:
        return str(num)
    if base == 1:
        return ('1'*num).zfill(1)
    max_length = math.floor(math.log(num) / math.log(base))
    current_num = num
    return_str = ''
    for notation in range(max_length,-1,-1):
        notation_value = base**notation
        if current_num >= notation_value:
            return_str += str(current_num//notation_value)
            current_num -= (current_num//notation_value)*notation_value
        else:
            return_str += '0'
    return return_str


def colour_list_to_str2(colour_list: list):
    r_colour = (255,0,0)
    g_colour = (0,255,0)
    b_colour = (0,0,255)
    m_colour = (255,0,255)
    c_colour = (0,255,255)
    y_colour = (255,255,0)
    w_colour = (255,255,255)
    chr_list = []
    chr_decode = []
    j=0
    for i in colour_list:
        if i == (0,0,0) or i == (0,0,0,0) or i == w_colour or i == w_colour + (255,) or j==2:
            break
        elif i == r_colour or i == r_colour+(255,):
            chr_decode.append("0")
            j=0
        elif i == g_colour or i == g_colour+(255,):
            chr_decode.append("1")
            j=0
        elif i == b_colour or i == b_colour+(255,):
            chr_decode.append("2")
            j=0
        elif i == m_colour or i == m_colour+(255,):
            chr_decode.append("3")
            j=0
        elif i == c_colour or i == c_colour+(255,):
            chr_decode.append("4")
            j=0
        elif i == y_colour or i == y_colour+(255,):
            chr_decode.append("5")
            j=0
        else:
            j=j+1
    
    num_list = []
    for i in range(0,len(chr_decode),5):
        num = map(str,(chr_decode[i:i+5]))
        num2 = "".join(num)
        if num2 == "00010":
            break
        num_list.append(int(num2,3))
    print(num_list)
        
        
    output_msg = bytes(num_list)
    return output_msg.decode("utf-8")

def colour_list_to_image(colour_list: list,image_size: tuple, out_path: str):
    col_list = [(255,0,0),(0,255,0),(0,0,255)]
    if len(colour_list) > (image_size[0] * image_size[1]):
        return "Colour list is too big for given size of image"
    new_image = PIL.Image.new("RGBA", image_size)
    for pixel_num , col in enumerate(colour_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = new_image.load()
        px[pixel_num, row_num] = col
    
    background = PIL.Image.new("RGBA", image_size)
    
    background_datachunk = image_size[0]*image_size[1] // 5
    lorem_text = ""
    
    while len(lorem_text) < background_datachunk:
        lorem_text = lorem_text + lorem.text()
    lorem_text = "".join(list(lorem_text)[:(background_datachunk-1)])
    print(lorem_text)
    lorem_col_list = str_to_colour_list2(lorem_text)
    print(lorem_col_list)
    for pixel_num , col in enumerate(lorem_col_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = background.load()
        print(f"{pixel_num =}")
        print(f"{row_num =}")
        px[pixel_num, row_num] = col
    
    background2 = PIL.Image.new("RGBA", image_size)
    
    for pixel_num in range(image_size[0] * image_size[1]):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = background2.load()
        px[pixel_num, row_num] = random.choice(col_list)
        pixel_num = pixel_num + 1
    
    background2.alpha_composite(background,(0,0))
    background2.alpha_composite(new_image, (0,0))
    background2.save(out_path)
    
def dict_to_list(pixel_dict:dict):
    pixel_list = []
    for i in pixel_dict:
        pixel_list = pixel_list + pixel_dict[i]
    return pixel_list

def pixelise(img_path: str) -> dict:
    """
    Convert the image to dictionary of pixel.

    Parameters
    ----------
    img_path : str
        Input Image Path.
    Returns
    -------
    pixel_dict : Dict
        Returns Dictionary where each Line represents a row of pixels,
        the colour codes of these pixels are recorded in the dict.
    """
    pixel_dict = {}
    with Image.open(img_path) as im:
        px = im.load()
        img_size = im.size
        for line_num in range(img_size[1]):
            line_list = [0] * img_size[0]
            for col_num in range(img_size[0]):
                new_pixel = px[col_num, line_num]
                line_list[col_num] = new_pixel
            pixel_dict[f"{line_num}"] = line_list
    return pixel_dict

def pixelise_img(img) -> dict:
    """
    Convert the image to dictionary of pixel.

    Parameters
    ----------
    img_path
        Input Image .
    Returns
    -------
    pixel_dict : Dict
        Returns Dictionary where each Line represents a row of pixels,
        the colour codes of these pixels are recorded in the dict.
    """
    pixel_dict = {}

    px = img.load()
    img_size = img.size
    for line_num in range(img_size[1]):
        line_list = [0] * img_size[0]
        for col_num in range(img_size[0]):
            new_pixel = px[col_num, line_num]
            line_list[col_num] = new_pixel
        pixel_dict[f"{line_num}"] = line_list
    return pixel_dict

def tob10(i):
    outVal = 0
    for ii in map(int, i):
        outVal = 3 * outVal + ii
    return outVal

def imgtostr2(img):
    ta = list(img.getdata())
    decoded = ""
    counter = 0
    pixels = 0
    for i in ta:
        if i[0] == 255 or i[0] == 254:
            decoded = decoded + "0"
        elif i[1] == 255 or i[1] == 254:
            decoded = decoded + "1"
        elif i[2] == 255 or i[2] == 254:
            decoded = decoded + "2"
        else:
            counter += 1
            continue
        if pixels == 4:
            pixels = 0
            decoded += ","
            continue
        pixels += 1
    decString = ""
    for i in decoded.split(sep=","):
        thisChar = chr(tob10(i))
        if thisChar == "\x03":
            break
        decString += thisChar
    with open("t.txt", "w", encoding="utf-8") as file:
        file.write(decString)
        file.close()
    return decString
        
def rebuild(pixel_dict: dict):
    new_image=PIL.Image.new("RGBA", (32,32))
    px=new_image.load()
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            pixel=pixel_dict[i][j]
            px[j,int(i)]=pixel
    new_image.show()
    
def str_to_img(secret_msg:str, out_path:str, image_size:tuple = (32,32)):
    col_list = str_to_colour_list2(secret_msg)
    colour_list_to_image(col_list, image_size, out_path)
    return

def take_photo():
    vid = cv2.VideoCapture(0)
    while(True):
          
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        with Image.fromarray(frame) as im:
            NewImg = PIL.Image.new("RGBA", im.size, None)
            OldImg = im.crop((0,0)+(im.size))
            NewImg.paste(OldImg, (0,0))
            
            centre_x = im.size[0]//2
            centre_y = im.size[1]//2
            
            
            with Image.open("Overlay.png") as overlay:
                NewImg.alpha_composite(overlay,(centre_x-130,centre_y-130))
            newframe = numpy.array(NewImg)
        # Display the resulting frame
        cv2.imshow('frame', newframe)
          
        # the 'c' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('c'):
            final = cv2.cvtColor(newframe, cv2.COLOR_BGR2RGB)
            final = Image.fromarray(final)
            new_image = final.crop((194,114,446,366))
            img = new_image
            px = img.load()
            img_new = img.convert('RGBA')
            px2 = img_new.load()
            for x in range(img.size[0]):
                for y in range(img.size[1]):
                    if sum(px[x, y]) <= (255*0.3*3):
                        px2[x, y] = (0,0,0,0)
            img_new.save('test_result2.png')
            
            new_image.save("SavedCode.png")
            time.sleep(2)
            break
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            time.sleep(2)
            break
      
    vid.release()
    cv2.destroyAllWindows()
    return new_image

def colour_correct(image):
    smol = image.resize((32,32), PIL.Image.NEAREST)
    px = smol.load()
    for y in range(32):
        for x in range(32):
            if px[x,y][0] > px[x,y][1] and px[x,y][0] > px[x,y][2]:
                px[x,y] = (255,0,0)
            elif px[x,y][1] > px[x,y][0] and px[x,y][1] > px[x,y][2]:
                px[x,y] = (0,255,0)    
            elif px[x,y][2] > px[x,y][0] and px[x,y][2] > px[x,y][1]:
                px[x,y] = (0,0,255)
    return smol

def img_to_str_the_second():
    print("please wait for the camera to boot")
    img_photo = take_photo()
    print("1")
    img_photo.show()
    print("2")
    corrected = colour_correct(img_photo)
    print("3")
    corrected.show()
    output_string = imgtostr2(corrected)
    return "output_string"