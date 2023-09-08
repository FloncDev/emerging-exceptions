# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:46:31 2023

@author: TheKek
"""

import math

import numpy as np
import PIL.Image
from PIL import Image, ImageFilter


def black_white(img):
    """Turns image into silhouette showing the black C in the Datastamp

    Parameters
    ----------
    img : Image
        Input Image file into this function.

    Returns
    -------
    black_img : Image
        Outputs pure B&W image, useful for finding orientation etc.

    """
    arr = np.array(img)
    arr = np.array(img)
    r = arr[:, :, 0]
    r2 = np.array(r.copy(), "int32")
    g = arr[:, :, 1]
    g2 = np.array(g.copy(), "int32")
    b = arr[:, :, 2]
    b2 = np.array(b.copy(), "int32")

    black = r2 + g2 + b2

    for i in range(black.shape[0]):
        for j in range(black.shape[1]):
            if black[i, j] < 125:
                black[i, j] = 255
            else:
                black[i, j] = 0

    black2 = np.array(black.copy(), "uint8")
    black_img = Image.fromarray(black2)
    black_img = black_img.filter(ImageFilter.MinFilter(5))
    return black_img


def find_right_angle(img):
    """Rotates silhouette so that the C in the datastamp is facing right

    Parameters
    ----------
    img : Image
        Input pure B&W image.

    Returns
    -------
    img : Image
        Returns image that has been rotated to be square .
    angle : Float
        Returns angle that the image had to be rotated by.

    """
    arr = np.array(img)

    cornerx = 0
    corner_y = 0

    cornery = 0
    corner_x = 0

    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if arr[x, y] == 255:
                if cornerx < x or cornerx == 0:
                    cornerx = x
                    corner_y = y
                if cornery > y or cornery == 0:
                    cornery = y
                    corner_x = x

    vert_len = corner_y - cornery
    hor_len = corner_x - cornerx
    if hor_len != 0:
        tan_angle = vert_len / hor_len
    else:
        tan_angle = 0
    anglerad = np.arctan(tan_angle)
    angle = anglerad * 180 / np.pi
    if abs(angle) < 10:
        angle = 0
    img = img.rotate((angle))

    return img, angle


def crop_and_rotate_to_L(img):
    """Crops silhouette and rotates it so that the left and bottom form an L

    Parameters
    ----------
    img : Image
        Input pure B&W image that is square.

    Returns
    -------
    img : Image
        Image no longer rotates to correct upside-down code, Image is cropped and shrunk.
    box : Tuple
        Defines area to be cropped.
    rot_num : Int
        DEPRECATED.
    arr2 : Numpy Array
        DEPRECATED.

    """
    arr = np.array(img)
    firstx = 0
    firsty = 0
    lastx = 0
    lasty = 0

    for x in range(arr.shape[0]):
        for y in range(arr.shape[1]):
            if arr[x, y] == 255:
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

    box = (min(firsty, lasty), min(firstx, lastx),
           max(lasty, firsty) + 5, max(lastx, firstx) + 5)

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

    return img, box  # , rot_num,  arr2


def centre_and_crop_img(img):
    """Centres and crops the input image

    Parameters
    ----------
    img : Image
        Handles image centreing, "squaring" (as in, like how a carpenters square forms a 90 degree angle) and cropping.

    Returns
    -------
    img : Image
        Image that is centred, squared, and cropped, for downsizing and decoding.

    """
    black_img = black_white(img)

    rot_black, angle = find_right_angle(black_img)

    final_img, box = crop_and_rotate_to_L(rot_black)
    im = img
    img = im.rotate(angle)
    img = img.crop(box)
    if angle < -45:
        img = img.rotate(90, 0, 1)

    return img


def resize_and_colour_correct(img):
    """Resizes and colour corrects datastamp

    Parameters
    ----------
    img : Image
        Input squared off and cropped Datastamp.

    Returns
    -------
    new_image : Image
        Datastamp which is downscaled and colour corrected for ease of decoding.

    """
    img = img.resize((33, 34), 0)
    img = img.crop((1, 1, 33, 33))
    arr = np.array(img)
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    for x in range(32):
        for y in range(32):
            if r[x, y] > g[x, y] and r[x, y] > b[x, y]:
                r[x, y] = 255
                g[x, y] = 0
                b[x, y] = 0
                continue
            elif g[x, y] > r[x, y] and g[x, y] > b[x, y]:
                r[x, y] = 0
                g[x, y] = 255
                b[x, y] = 0
                continue
            elif b[x, y] > r[x, y] and b[x, y] > g[x, y]:
                r[x, y] = 0
                g[x, y] = 0
                b[x, y] = 255
                continue
            else:
                return "Please input image taken from different lighting, undistorted"
    r_channel = Image.fromarray(r, "L")
    g_channel = Image.fromarray(g, "L")
    b_channel = Image.fromarray(b, "L")

    bands = (r_channel, g_channel, b_channel)
    new_image = Image.merge("RGB", bands)

    return new_image


def decode2(img):
    """Decodes the datastamp into a string

    Parameters
    ----------
    img : Image
        Decodes Datastamp into a string.

    Returns
    -------
    mystr : str
        String decoded from datastamp.

    """
    pixeldict = pixelise_img(img)
    pixellist = dict_to_list(pixeldict)
    mystr = colour_list_to_str2(pixellist)
    return mystr


def decode_bytes(img):
    """Decodes the datastamp into a string

    Parameters
    ----------
    img : Image
        Decodes Datastamp into a string.

    Returns
    -------
    mystr : str
        String decoded from datastamp.

    """
    pixeldict = pixelise_img(img)
    pixellist = dict_to_list(pixeldict)
    mystr = colour_list_to_byte(pixellist)
    return mystr


def pixelise_img(img) -> dict:
    """Convert the image to dictionary of pixel.

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


def dict_to_list(pixel_dict: dict):
    """Just a simple dict -> list function

    Parameters
    ----------
    pixel_dict : dict
        Input dict.

    Returns
    -------
    pixel_list : list
        Output list.


    """
    pixel_list = []
    for i in pixel_dict:
        pixel_list = pixel_list + pixel_dict[i]
    return pixel_list


def colour_list_to_str2(colour_list: list):
    """Colour list is converted to string

    Parameters
    ----------
    colour_list : list
        Input list of colours.

    Returns
    -------
    output_msg : str
        Message decoded from UTF-8.

    Inspired by Dels UTF-8 experiments

    """
    r_colour = (255, 0, 0)
    g_colour = (0, 255, 0)
    b_colour = (0, 0, 255)
    m_colour = (255, 0, 255)
    c_colour = (0, 255, 255)
    y_colour = (255, 255, 0)
    w_colour = (255, 255, 255)
    chr_decode = []
    j = 0
    for i in colour_list:
        if i == (0, 0, 0) or i == (0, 0, 0, 0) or i == w_colour or i == w_colour + (255,) or j == 2:
            break
        elif i == r_colour or i == r_colour + (255,):
            chr_decode.append("0")
            j = 0
        elif i == g_colour or i == g_colour + (255,):
            chr_decode.append("1")
            j = 0
        elif i == b_colour or i == b_colour + (255,):
            chr_decode.append("2")
            j = 0
        elif i == m_colour or i == m_colour + (255,):
            chr_decode.append("3")
            j = 0
        elif i == c_colour or i == c_colour + (255,):
            chr_decode.append("4")
            j = 0
        elif i == y_colour or i == y_colour + (255,):
            chr_decode.append("5")
            j = 0
        else:
            j = j + 1

    num_list = []
    for i in range(0, len(chr_decode), 5):
        num = map(str, (chr_decode[i:i + 5]))
        num2 = "".join(num)
        if num2 == "00010":
            break
        num_list.append(int(num2, 3))

    output_msg = bytes(num_list)
    return output_msg.decode("utf-8")


def colour_list_to_byte(colour_list: list):
    """Colour list is converted to string

    Parameters
    ----------
    colour_list : list
        Input list of colours.

    Returns
    -------
    output_msg : bytes
        Raw message in byte

    """
    r_colour = (255, 0, 0)
    g_colour = (0, 255, 0)
    b_colour = (0, 0, 255)
    m_colour = (255, 0, 255)
    c_colour = (0, 255, 255)
    y_colour = (255, 255, 0)
    w_colour = (255, 255, 255)
    chr_decode = []
    j = 0
    for i in colour_list:
        if i == (0, 0, 0) or i == (0, 0, 0, 0) or i == w_colour or i == w_colour + (255,) or j == 2:
            break
        elif i == r_colour or i == r_colour + (255,):
            chr_decode.append("0")
            j = 0
        elif i == g_colour or i == g_colour + (255,):
            chr_decode.append("1")
            j = 0
        elif i == b_colour or i == b_colour + (255,):
            chr_decode.append("2")
            j = 0
        elif i == m_colour or i == m_colour + (255,):
            chr_decode.append("3")
            j = 0
        elif i == c_colour or i == c_colour + (255,):
            chr_decode.append("4")
            j = 0
        elif i == y_colour or i == y_colour + (255,):
            chr_decode.append("5")
            j = 0
        else:
            j = j + 1

    num_list = []
    for i in range(0, len(chr_decode), 5):
        num = map(str, (chr_decode[i:i + 5]))
        num2 = "".join(num)
        if num2 == "00010":
            break
        num_list.append(int(num2, 3))

    output_msg = bytes(num_list)
    return output_msg


def photo_to_str(img_path):
    """Converts photo to string

    Parameters
    ----------
    img_path : str
        Input image path of Datastamp you wish to decode (NOTE, code must have a white background).

    Returns
    -------
    mystr : str
        Outputs data decoded from Datastamp.

    """
    if isinstance(img_path, PIL.Image.Image):
        im = img_path
    else:
        im = PIL.Image.open(img_path)
    imgsize = im.size
    img = im.resize(
        (math.floor(0.25 * imgsize[0]), math.floor(0.25 * imgsize[1])), 1)

    img = centre_and_crop_img(img)
    img = resize_and_colour_correct(img)
    if img == "Please input image taken from different lighting, undistorted":
        return "Please input image taken from different lighting, undistorted"
    mystr = decode2(img)
    return mystr


def photo_to_byte(img_path):
    """Converts photo to string

    Parameters
    ----------
    img_path : str
        Input image path of Datastamp you wish to decode (NOTE, code must have a white background).

    Returns
    -------
    mystr : bytes
        Outputs data decoded from Datastamp.

    """
    if isinstance(img_path, PIL.Image.Image):
        im = img_path
    else:
        im = PIL.Image.open(img_path)
    imgsize = im.size
    img = im.resize(
        (math.floor(0.25 * imgsize[0]), math.floor(0.25 * imgsize[1])), 1)

    img = centre_and_crop_img(img)
    img = resize_and_colour_correct(img)
    if img == "Please input image taken from different lighting, undistorted":
        return "Please input image taken from different lighting, undistorted"
    mystr = decode_bytes(img)
    return mystr


if __name__ == "__main__":
    # the functions should handle everything
    img_path = input("Please input img path of image to be decoded \n")
    mystr = photo_to_str(img_path)
    print(mystr)
