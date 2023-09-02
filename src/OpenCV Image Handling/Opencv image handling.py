# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 20:55:37 2023

@author: TheKekening
"""
import cv2
import PIL
from PIL import Image
from PIL import ImageEnhance
import numpy
import time
  
# define a video capture object
vid = cv2.VideoCapture(0)
 
def take_photo():
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
            final.save("SavedCode.png")
            time.sleep(2)
            break
      
    vid.release()
    cv2.destroyAllWindows()
    return

def downscale(img_path:str):
    with Image.open(img_path) as im:
        # new_image = im.crop((194,114,446,366))
        new_image=im
        smol = new_image.resize((64,64), PIL.Image.NEAREST)
        over_saturate = PIL.ImageEnhance.Color(smol)
        smol = over_saturate.enhance(5)
        smol.save("downscaled5.png")

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
        
def colourcorrect(img_path:str):
    pixel_dict = pixelise(img_path)
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            value = [0,0,0]
            for k in range(3):
                #this is done because cameras are more sensitive to green light, therefore a higher boundary must be crossed for green to be registered
                if k==1:
                    if pixel_dict[i][j][k] > 160:
                        value[k] = 255
                    else:
                        value[k] = 0
                else:
                    if pixel_dict[i][j][k] > 128:
                        value[k] = 255
                    else:
                        value[k] = 0
                
            pixel_dict[i][j] = (value[0], value[1], value[2])
            
    return pixel_dict

def rebuild(pixel_dict: dict):
    new_image=PIL.Image.new("RGBA", (64,64))
    px=new_image.load()
    for i in pixel_dict:
        for j in range(len(pixel_dict[i])):
            pixel=pixel_dict[i][j]
            px[j,int(i)]=pixel
    new_image.save("FINAL3.png")
    
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
                
def str_to_colour_list(SecretMsg: str):
    r_colour = (255,0,0)
    g_colour = (0,255,0)
    b_colour = (0,0,255)
    m_colour = (255,0,255)
    c_colour = (0,255,255)
    y_colour = (255,255,0)
    w_colour = (255,255,255)
    colour_list = []
    for i in SecretMsg:
        char_val = ord(i)
        #NOTE: in this case hex refers to base 6 rather than base 16
        msg_hex = baseconvert(char_val, 6)
        for j in str(msg_hex):
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
        colour_list.append(w_colour)
    colour_list.append((0,0,0))
    return colour_list
        
def colour_list_to_str(colour_list: str):
    r_colour = (255,0,0)
    g_colour = (0,255,0)
    b_colour = (0,0,255)
    m_colour = (255,0,255)
    c_colour = (0,255,255)
    y_colour = (255,255,0)
    w_colour = (255,255,255)
    chr_list = []
    chr_decode = []
    for i in colour_list:
        if i == w_colour:
            #NOTE: in this case hex refers to base 6 rather than base 16
            chr_hex_num = "".join(chr_decode)
            chr_dec_num = int(chr_hex_num,6)
            chr_list.append(chr(chr_dec_num))
            chr_decode = []
            continue
        elif i == (0,0,0):
            break
        elif i == r_colour:
            chr_decode.append("0")
        elif i == g_colour:
            chr_decode.append("1")
        elif i == b_colour:
            chr_decode.append("2")
        elif i == m_colour:
            chr_decode.append("3")
        elif i == c_colour:
            chr_decode.append("4")
        elif i == y_colour:
            chr_decode.append("5")
    output_msg = "".join(chr_list)
    return output_msg

def colour_list_to_image(colour_list: list,image_size: tuple, out_path: str):
    if len(colour_list) > (image_size[0] * image_size[1]):
        return "Colour list is too big for given size of image"
    new_image = PIL.Image.new("RGB", image_size)
    for pixel_num , col in enumerate(colour_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = new_image.load()
        print(pixel_num)
        print(row_num)
        px[pixel_num, row_num] = col
    new_image.save(out_path)
    
def dict_to_list(pixel_dict:dict):
    pixel_list = []
    for i in pixel_dict:
        pixel_list = pixel_list + pixel_dict[i]
    return pixel_list


        
        
        
    
    