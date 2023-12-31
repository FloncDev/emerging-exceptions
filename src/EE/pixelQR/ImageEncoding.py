# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 21:00:09 2023

@author: TheKek
"""
import math
import random

import PIL
from PIL import Image, ImageOps


def str_to_image(secret_str: str, img_size: tuple = (32, 32)):
    """Converts input string to Datastamp

    Parameters
    ----------
    secret_str : str
        Input the string you wish to encode into the image.
    out_path : str
        Input the output path of the image.
    img_size : tuple, optional
        Size of the data encoding image in pixels. The default is (32,32).

    Returns
    -------
    out_path: str
        Return the output path of the image.

    """
    collist = str_to_colour_list2(secret_str)
    im = colour_list_to_image(collist, img_size)
    new_image = Image.new("RGB", (33, 34))
    new_image.paste(im, (1, 1))
    # The "new_image" variable is used to form the black C shape
    # The black C shape is used for orientation purposes
    w_background = Image.new("L", (35, 36))
    w_background = ImageOps.colorize(
        w_background, (255, 255, 255), (255, 255, 255))
    w_background.paste(new_image, (1, 1))
    # The white background is necessary for the datastamp to successfully
    # be scanned
    new_image = w_background.resize((1000, 1000), 0)
    return new_image


def baseconvert2(num: int, base: int) -> str:
    """Converts from base 10 to a given base

    Function made by deleted.user0 on discord

    Parameters
    ----------
    num : int
        Input number in base 10.
    base : int
        Input the base the output should be given in.

    Returns
    -------
    return_str : str
        Returns the input number converted to the desired base,
        e.g. 2 in base 2 = 10.

    """
    if base == 10:
        return str(num)
    if base == 1:
        return ('1'*num).zfill(1)
    max_length = math.floor(math.log(num) / math.log(base))
    current_num = num
    return_str = ''
    for notation in range(max_length, -1, -1):
        notation_value = base**notation
        if current_num >= notation_value:
            return_str += str(current_num//notation_value)
            current_num -= (current_num//notation_value)*notation_value
        else:
            return_str += '0'
    return return_str


def str_to_colour_list2(SecretMsg: str):
    """Converts string to list of colours

    Parameters
    ----------
    SecretMsg : str
        Input message to be encoded.

    Returns
    -------
    colour_list : list
        Returns the list of colours which encodes the img.

    """
    r_colour = (255, 0, 0)
    g_colour = (0, 255, 0)
    b_colour = (0, 0, 255)
    m_colour = (255, 0, 255)
    c_colour = (0, 255, 255)
    y_colour = (255, 255, 0)
    colour_list = []
    base_3_list = []

    str_integer_list = list(SecretMsg.encode('utf-8'))
    for a in str_integer_list:
        base_3_num = baseconvert2(a, 3)
        base_3_num = base_3_num.zfill(5)
        base_3_list.append(base_3_num)

    base_3_list.append("00010")
    # Every character in the string is converted from their UTF-8 Decimal
    # to base 3 (used to represent R G and B) Base 6 was tried which included
    # Y M and C, but ultimately failed, as the computer would struggle
    # distinguishing the secondary colours as such.
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


def colour_list_to_image(colour_list: list, image_size: tuple):
    """Converts list of colours into the encoding portion of Datastamp

    Parameters
    ----------
    colour_list : list
        Input list of colours which encodes for data.
    image_size : tuple
        Input size of data encoding image in pixels (generally 32x32).
    out_path : str
        Input the desired output path of the image.

    Returns
    -------
    Does not return any data, instead,
    the compiled image is outputted to the output path

    """
    # The first for loop encodes the data encoding portion of the Datastamp
    col_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    if len(colour_list) > (image_size[0] * image_size[1]):
        return "Colour list is too big for given size of image"
    new_image = PIL.Image.new("RGBA", image_size)
    for pixel_num, col in enumerate(colour_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = new_image.load()
        px[pixel_num, row_num] = col
    # The second for loop encodes random data, to help visually hide the data
    # encoding portion of the datastamp
    background = PIL.Image.new("RGBA", image_size)
    background_datachunk = image_size[0]*image_size[1] // 5
    b64_text = ""
    b64_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                "W", "X", "Y", "Z", "=", "0", "1", "2", "3", "4", "5", "6",
                "7", "8", "9", "+", "/"]
    while len(b64_text) < background_datachunk:
        b64_text = b64_text + random.choice(b64_list)
    b64_text = "".join(list(b64_text)[:(background_datachunk-1)])
    b64_col_list = str_to_colour_list2(b64_text)
    for pixel_num, col in enumerate(b64_col_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = background.load()
        px[pixel_num, row_num] = col

    # The final for loop encodes purely random colours, this is done to fill
    # the last few pixels of the Datastamp, and prevent a blot of black at the
    # end of the coloured portion
    background2 = PIL.Image.new("RGBA", image_size)
    px = background2.load()
    for pixel_num in range(image_size[0] * image_size[1]):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px[pixel_num, row_num] = random.choice(col_list)
        pixel_num = pixel_num + 1
    background2.alpha_composite(background, (0, 0))
    background2.alpha_composite(new_image, (0, 0))
    return background2


if __name__ == "__main__":
    input_str = input(
        "Please input the message you would like to encode in image \n")
    output_path = input("Please input the output path of the encoded file \n")
    str_to_image(input_str, output_path)
    print("done!")
