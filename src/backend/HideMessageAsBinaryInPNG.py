# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:20:59 2023

@author: TheKekening
"""

import PIL
from PIL import Image


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


def dict_contract(pixel_dict):  # noqa: D103
    new_list = []
    for i in pixel_dict:
        new_list = new_list + i
    return new_list


def alpha_img(img_path: str, out_path: str):
    """Convert normal RGB image to RGBA so it contain alpha channel for modifying purpose."""
    with Image.open(img_path) as im:
        new_img = PIL.Image.new("RGBA", im.size, None)
        old_img = im.crop((0, 0) + (im.size))
        new_img.paste(old_img, (0, 0))
    new_img.save(out_path)
    return


def str_to_list(secret_msg: str):
    """Converting string of secret message to binary format."""
    out_list = ["0"] * len(secret_msg)
    for i, a in enumerate(secret_msg):
        mid = str(bin(ord(a)))
        final = mid.replace("0b", "")
        if len(final) != 8:
            final = "0" * (8 - len(final)) + final
        out_list[i] = final
    return out_list


def hide_msg(img_path: str, secret_msg: str, out_path: str):
    """
    Hide secret message to an image which can be decode with hide_msg

    Parameters
    ----------
    img_path : str
        Input Image Path.
    secret_msg: str
        The secret message.
    out_path: str
        Output Inamge Path.
    """
    bin_msg = str_to_list(secret_msg)
    pix_hor_num = 0
    pix_ver_num = 0
    alpha_img(img_path, out_path)
    with Image.open(out_path) as im:
        px = im.load()
        img_size = (im.size[0] * im.size[1])
        iteration_number = img_size // 8
        if iteration_number < len(bin_msg):
            return "Image too small to encode message"
        for i in range(len(bin_msg)):
            for j in range(len(bin_msg[i])):
                if pix_hor_num > im.size[0] - 1:
                    pix_hor_num = 0
                    pix_ver_num = pix_ver_num + 1
                sel_pixel = px[pix_hor_num, pix_ver_num]
                if int(bin_msg[i][j]) == 1:
                    r_value = sel_pixel[0]
                    g_value = sel_pixel[1]
                    b_value = sel_pixel[2]
                    px[pix_hor_num, pix_ver_num] = (r_value, g_value, b_value, 254)
                pix_hor_num = pix_hor_num + 1
        im.save(out_path)
    return "done"


def decrypt_img(img_path: str) -> str:
    """
    Retrieve the Secret Message from the encoded image

    Parameters
    ----------
    img_path : str
        Input Image Path.
    Returns
    -------
    secret_msg : str
        Return string hidden in the image from hide_msg
    """
    pixel_dict = pixelise(img_path)
    decoded_bin = []
    for i in range(len(pixel_dict)):
        for j in pixel_dict[str(i)]:
            if j[3] == 254:
                decoded_bin.append(1)
            elif j[3] == 255:
                decoded_bin.append(0)
    j = 0
    byte_list = []
    while "".join(map(str, decoded_bin[j:j + 8])) != "00000000" and "".join(map(str, decoded_bin[j:j + 8])) != "":
        byte_list.append(decoded_bin[j:j + 8])
        j = j + 8
    new_str_list = ['0'] * len(byte_list)
    for i in range(len(byte_list)):
        selected_byte = "".join(map(str, byte_list[i]))
        new_str_list[i] = chr(int(selected_byte, 2))

    return "".join(new_str_list)
