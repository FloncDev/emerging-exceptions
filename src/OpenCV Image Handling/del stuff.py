# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 14:54:49 2023

@author: olive
"""
import typing

def str_to_bit(input_string: typing.AnyStr):
    """Convert any string to list of 0 and 1 in integer format."""
    str_integer_list = list(input_string.encode('utf-8'))
    binary_list = [bin(a).replace('0b', '').zfill(8) for a in str_integer_list]
    str_bit_list = list(''.join(binary_list))
    return [int(b) for b in str_bit_list]


def bit_to_str(input_bit: list):
    """Convert list of 0 and 1 in either integer or string format to the original string."""
    bit_str_list = [str(a) for a in input_bit]
    int_list = [int(''.join(bit_str_list[g:g + 8]), 2) for g in range(0, len(bit_str_list), 8)]
    bin_str = bytes.fromhex(" ".join([hex(i).replace("0x", "") for i in int_list]))
    print(bin_str)
    return bin_str.decode('utf-8')