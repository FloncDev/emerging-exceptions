# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 20:55:37 2023

@author: TheKekening
"""
# import cv2
import PIL
from PIL import Image
from PIL import ImageEnhance
import numpy
import time
import random
import math
import typing
  
# define a video capture object
# vid = cv2.VideoCapture(0)
 
# def take_photo():
#     while(True):
          
#         # Capture the video frame
#         # by frame
#         ret, frame = vid.read()
#         with Image.fromarray(frame) as im:
#             NewImg = PIL.Image.new("RGBA", im.size, None)
#             OldImg = im.crop((0,0)+(im.size))
#             NewImg.paste(OldImg, (0,0))
            
#             centre_x = im.size[0]//2
#             centre_y = im.size[1]//2
            
            
#             with Image.open("Overlay.png") as overlay:
#                 NewImg.alpha_composite(overlay,(centre_x-130,centre_y-130))
#             newframe = numpy.array(NewImg)
#         # Display the resulting frame
#         cv2.imshow('frame', newframe)
          
#         # the 'c' button is set as the
#         # quitting button you may use any
#         # desired button of your choice
#         if cv2.waitKey(1) & 0xFF == ord('c'):
#             final = cv2.cvtColor(newframe, cv2.COLOR_BGR2RGB)
#             final = Image.fromarray(final)
#             new_image = final.crop((194,114,446,366))
#             img = new_image
#             px = img.load()
#             img_new = img.convert('RGBA')
#             px2 = img_new.load()
#             for x in range(img.size[0]):
#                 for y in range(img.size[1]):
#                     if sum(px[x, y]) <= (255*0.3*3):
#                         px2[x, y] = (0,0,0,0)
#             img_new.save('test_result2.png')
            
#             new_image.save("SavedCode.png")
#             time.sleep(2)
#             break
    
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             time.sleep(2)
#             break
      
#     vid.release()
#     cv2.destroyAllWindows()
#     return new_image

def downscale(img_path:str,out_path:str):
    with Image.open(img_path) as im:
        new_image=im
        smol = new_image.resize((32,32), PIL.Image.NEAREST)
        over_saturate = PIL.ImageEnhance.Color(smol)
        smol = over_saturate.enhance(3)
        smol.save(out_path)
    return

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

def pixelise2(img):

    im = img
    px = im.load()
    img_size = im.size
    pixel_dict = {}
    for line_num in range(img_size[1]):
        line_list = [0] * img_size[0]
        for col_num in range(img_size[0]):
            new_pixel = px[col_num, line_num]
            line_list[col_num] = new_pixel
        pixel_dict[f"{line_num}"] = line_list
    return pixel_dict
        
def colourcorrect(img_path:str):
    pixel_dict = pixelise(img_path)
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            value = [0,0,0]
            for k in range(3):
                #this is done because cameras are more sensitive to green light, therefore a higher boundary must be crossed for green to be registered
                if k==1:
                    if pixel_dict[i][j][k] > 120:
                        value[k] = 255
                    else:
                        value[k] = 0
                else:
                    if pixel_dict[i][j][k] > 120:
                        value[k] = 255
                    else:
                        value[k] = 0
                
            pixel_dict[i][j] = (value[0], value[1], value[2])
            
    return pixel_dict

def colourcorrect2(img_path:str):
    r_colour = (255,0,0)
    g_colour = (0,255,0)
    b_colour = (0,0,255)
    m_colour = (255,0,255)
    c_colour = (0,255,255)
    y_colour = (255,255,0)
    w_colour = (255,255,255)
    pixel_dict = pixelise(img_path)
    sens = 50
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            value = [0,0,0]
            #this is done because cameras are more sensitive to green light, therefore a higher boundary must be crossed for green to be registered
            if abs(pixel_dict[i][j][0]-pixel_dict[i][j][1]) < sens and abs(pixel_dict[i][j][0]-pixel_dict[i][j][2]) < sens and pixel_dict[i][j][0] > 100:
                pixel_dict[i][j] = w_colour
            elif abs(pixel_dict[i][j][0]-pixel_dict[i][j][1]) > sens and abs(pixel_dict[i][j][0]-pixel_dict[i][j][2]) > sens and pixel_dict[i][j][0] > 100:
                pixel_dict[i][j] = r_colour
            elif abs(pixel_dict[i][j][1]-pixel_dict[i][j][0]) > sens and abs(pixel_dict[i][j][1]-pixel_dict[i][j][2]) > sens and pixel_dict[i][j][1] > 100:
                pixel_dict[i][j] = g_colour
            elif abs(pixel_dict[i][j][2]-pixel_dict[i][j][0]) > sens and abs(pixel_dict[i][j][2]-pixel_dict[i][j][1]) > sens and pixel_dict[i][j][1] > 100:
                pixel_dict[i][j] = b_colour
            elif abs(pixel_dict[i][j][0]-pixel_dict[i][j][2]) < sens and abs(pixel_dict[i][j][0]-pixel_dict[i][j][1]) > sens:
                pixel_dict[i][j] = m_colour
            elif abs(pixel_dict[i][j][0]-pixel_dict[i][j][1]) < sens and abs(pixel_dict[i][j][0]-pixel_dict[i][j][2]) > sens:
                pixel_dict[i][j] = y_colour
            elif abs(pixel_dict[i][j][1]-pixel_dict[i][j][2]) < sens and abs(pixel_dict[i][j][1]-pixel_dict[i][j][0]) > sens:
                pixel_dict[i][j] = c_colour
            else:
                pixel_dict[i][j] = (0,0,0)
            
    rebuild(pixel_dict)
    return pixel_dict




def colourcorrect_modified(img_path:str):
    with Image.open(img_path) as im:
        px = im.load()
        r_channel, g_channel, b_channel, a_channel = im.split()
        r_channel.show()
        g_channel.show()
        b_channel.show()
        r_dict = pixelise2(r_channel)
        g_dict = pixelise2(g_channel)
        b_dict = pixelise2(b_channel)
                
        for i in r_dict:
            for j,val in enumerate(r_dict[i]):
                if val > 120:
                    r_dict[i][j] = 255
                else:
                    r_dict[i][j] = 0
                    
        for i in g_dict:
            for j,val in enumerate(g_dict[i]):
                if val > 120:
                    g_dict[i][j] = 255
                else:
                    g_dict[i][j] = 0
                    
        for i in b_dict:
            for j,val in enumerate(b_dict[i]):
                if val > 120:
                    b_dict[i][j] = 255
                else:
                    b_dict[i][j] = 0

                    

        r_channel = rebuildL(r_dict)
        g_channel = rebuildL(g_dict)
        b_channel = rebuildL(b_dict)
        
        col_channel_join(r_channel, g_channel, b_channel, (32,32))
        
        
def col_channel_join(r_channel, g_channel, b_channel, size:tuple):
    bands = (r_channel,g_channel,b_channel)
    new_image = Image.merge("RGB", bands)
    new_image.show()


def rebuild(pixel_dict: dict):
    new_image=PIL.Image.new("RGBA", (32,32))
    px=new_image.load()
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            pixel=pixel_dict[i][j]
            px[j,int(i)]=pixel
            print(j)
            print(i)
            print(pixel)
    new_image.show()

def rebuildL(pixel_dict: dict):
    new_image=PIL.Image.new("L", (32,32))
    px=new_image.load()
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            pixel=pixel_dict[i][j]
            px[j,int(i)]=pixel
            print(j)
            print(i)
            print(pixel)
    new_image.show()
    return new_image

#Depreciated, baseconvert2 is more efficient
def baseconvert(num : int, base : int):
    final_list = []
    place_num = 0
    for i in range(num):
        try: final_list[place_num]
        except:  final_list.append(0)
        place_num = 0
        final_list[place_num] = final_list[place_num] + 1
        while final_list[place_num] == base:
            final_list[place_num] = 0
            place_num = place_num + 1
            try: final_list[place_num]
            except:  final_list.append(0)
            final_list[place_num] = final_list[place_num] + 1
    final_list.reverse()
    final_int = int("".join(map(str,final_list)))
    return final_int
                
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


def str_to_colour_list(SecretMsg: str):
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

    for a in str_integer_list:
        base_3_num = baseconvert2(a,3)
        base_3_num = base_3_num.zfill(3)
        base_3_list.append(base_3_num)
        
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
    for i in range(4): 
        colour_list.append(w_colour)
    return colour_list
        
def colour_list_to_str(colour_list: list):
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
        if i == (0,0,0) or i == (0,0,0,0) or j==2:
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
    for i in range(0,chr_decode,3):
        num_list.append(chr_decode[i:i+3])
        
    output_msg = "".join(chr_list)
    
    return output_msg



def colour_list_to_image(colour_list: list,image_size: tuple, out_path: str):
    col_list = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,255,255)]
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
    
    for pixel_num in range(image_size[0] * image_size[1]):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = background.load()
        px[pixel_num, row_num] = random.choice(col_list)
        pixel_num = pixel_num + 1
    
    background.alpha_composite(new_image, (0,0))
    background.save(out_path)
    
def dict_to_list(pixel_dict:dict):
    pixel_list = []
    for i in pixel_dict:
        pixel_list = pixel_list + pixel_dict[i]
    return pixel_list

def str_to_image(secret_str:str, img_size:tuple, out_path:str):
    collist = str_to_colour_list(secret_str)
    colour_list_to_image(collist, img_size, out_path)
    with Image.open(out_path) as im:
        new_image = Image.new("RGB",(33,34))
        im.show()
        new_image.paste(im,(1,1))
        new_image.show()
        new_image.save(out_path)
    return "done"

def img_to_str(in_path:str):
#    img = take_photo()
    downscale(in_path, "Downscaled.png")
    pixeldictnorm = pixelise("Downscaled.png")
    rebuild(pixeldictnorm)
    pixeldict = colourcorrect("Downscaled.png")
    print(pixeldict)
    pixellist = dict_to_list(pixeldict)
    
    rebuild(pixeldict)
    decoded_str = colour_list_to_str(pixellist)
    return decoded_str
    