import math
import os
import pathlib
import typing
from abc import ABC, abstractmethod

import PIL.Image

MODE_ENCRYPTION = 0xFFFF0800
MODE_DECRYPTION = 0xFFFF0801
mode: typing.TypeAlias = MODE_ENCRYPTION | MODE_DECRYPTION
b10_int: typing.TypeAlias = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
path: typing.TypeAlias = pathlib.Path | str | os.PathLike
pure_image: typing.TypeAlias = PIL.Image.Image
image: typing.TypeAlias = path | pure_image
message: typing.TypeAlias = typing.AnyStr | typing.Any
secret: typing.TypeAlias = typing.AnyStr


class LibraryBase(ABC):
    """The base of the library instance."""

    def __init__(self):
        pass

    @abstractmethod
    async def routine(self, mode: mode, data_input: dict):
        """A normal routine of an encryption or decryption process."""
        raise NotImplementedError('async Function: routine must be added')


def str_to_bit(input_string: typing.AnyStr) -> list[int]:
    """Convert any string to list of 0 and 1 in integer format."""
    str_integer_list = list(input_string.encode('utf-8'))
    binary_list = [bin(a).replace('0b', '').zfill(8) for a in str_integer_list]
    str_bit_list = list(''.join(binary_list))
    return [int(b) for b in str_bit_list]


def bit_to_str(input_bit: list[int | str]) -> typing.AnyStr:
    """Convert list of 0 and 1 in either integer or string format to the original string."""
    bit_str_list = [str(a) for a in input_bit]
    int_list = []
    for g in range(0, len(bit_str_list), 8):
        int_list.append(int(''.join(bit_str_list[g:g + 8]), 2))
    bin_str = bytes.fromhex(" ".join([hex(i).replace("0x", "") for i in int_list]))
    return bin_str.decode('utf-8')


# def baseconvert(num: int, base: int):
#     final_list = []
#     place_num = 0
#     for i in range(num):
#         try:
#             final_list[place_num]
#         except:
#             final_list.append(0)
#         place_num = 0
#         final_list[place_num] += 1
#         while final_list[place_num] == base:
#             final_list[place_num] = 0
#             place_num = place_num + 1
#             try:
#                 final_list[place_num]
#             except:
#                 final_list.append(0)
#             final_list[place_num] += 1
#     final_list.reverse()
#     final_int = int("".join(map(str, final_list)))
#     return final_int


def base_convert(num: int, base: b10_int) -> str:
    """Convert base-10 number to value in between base- 1-10."""
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
    if current_num != 0:
        raise ValueError(f'Num issue: {current_num}')
    return return_str


def load_path(paths: path) -> pathlib.Path:
    """Load any PathLike object as pathlib.Path"""
    if isinstance(paths, str) or isinstance(paths, os.PathLike):
        return pathlib.Path(paths)
    return paths


def load_image(paths: path) -> PIL.Image.Image:
    """Convert path to PIL.Image.Image instance."""
    images = PIL.Image.open(paths)
    return images
