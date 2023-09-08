# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 21:00:09 2023

@author: TheKek
"""
import math
import random

import lorem
import PIL
from PIL import Image, ImageOps


def str_to_image(secret_str: str, out_path: str, img_size: tuple = (32, 32)):
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
    str
        DESCRIPTION.

    """
    collist = str_to_colour_list2(secret_str)
    colour_list_to_image(collist, img_size, out_path)
    with Image.open(out_path) as im:
        new_image = Image.new("RGB", (33, 34))
        new_image.paste(im, (1, 1))
        w_background = Image.new("L", (35, 36))
        w_background = ImageOps.colorize(
            w_background, (255, 255, 255), (255, 255, 255))
        w_background.paste(new_image, (1, 1))
        new_image = w_background.resize((1000, 1000), 0)
        new_image.save(out_path)
    return out_path


def baseconvert2(num: int, base: int) -> str:
    """Converts from base 10 to a given base

    Function made by Del

    Parameters
    ----------
    num : int
        Input number in base 10.
    base : int
        Input the base the output should be given in.

    Returns
    -------
    str
        Returns the input number converted to the desired base, e.g. 2 in base 2 = 10.

    """
    if base == 10:
        return str(num)
    if base == 1:
        return ('1' * num).zfill(1)
    max_length = math.floor(math.log(num) / math.log(base))
    current_num = num
    return_str = ''
    for notation in range(max_length, -1, -1):
        notation_value = base ** notation
        if current_num >= notation_value:
            return_str += str(current_num // notation_value)
            current_num -= (current_num // notation_value) * notation_value
        else:
            return_str += '0'
    return return_str


def str_to_colour_list2(SecretMsg: str | bytes):
    """Converts string to list of colours

    Parameters
    ----------
    SecretMsg : str | bytes
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
    if isinstance(SecretMsg, bytes):
        str_integer_list = list(SecretMsg)

    else:
        str_integer_list = list(SecretMsg.encode('utf-8'))
    for a in str_integer_list:
        base_3_num = baseconvert2(a, 3)
        base_3_num = base_3_num.zfill(5)
        base_3_list.append(base_3_num)

    base_3_list.append("00010")

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


def colour_list_to_image(colour_list: list, image_size: tuple, out_path: str):
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
    Does not return any data, instead, the compiled image is outputted to the output path

    """
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

    background = PIL.Image.new("RGBA", image_size)

    background_datachunk = image_size[0] * image_size[1] // 5
    lorem_text = ""

    while len(lorem_text) < background_datachunk:
        lorem_text = lorem_text + lorem.text()
    lorem_text = "".join(list(lorem_text)[:(background_datachunk - 1)])
    lorem_col_list = str_to_colour_list2(lorem_text)
    for pixel_num, col in enumerate(lorem_col_list):
        row_num = 0
        while pixel_num >= image_size[0]:
            row_num = row_num + 1
            pixel_num = pixel_num - image_size[0]
        px = background.load()
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

    background2.alpha_composite(background, (0, 0))
    background2.alpha_composite(new_image, (0, 0))
    background2.save(out_path)


if __name__ == "__main__":
    input_str = input(
        "Please input the message you would like to encode in image \n")
    output_path = input("Please input the output path of the encoded file \n")
    str_to_image(input_str, output_path)
    print("done!")
