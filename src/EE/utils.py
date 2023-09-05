import math
import os
import pathlib
import typing
from abc import ABC, abstractmethod

import PIL.Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

MODE_ENCRYPTION = 0xFFFF0800
MODE_DECRYPTION = 0xFFFF0801
BLOCK_SIZE = 32
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
    if not isinstance(input_string, bytes):
        str_integer_list = list(input_string.encode('utf-8'))
    else:
        str_integer_list = list(input_string)
    binary_list = [bin(a).replace('0b', '').zfill(8) for a in str_integer_list]
    str_bit_list = list(''.join(binary_list))
    return [int(b) for b in str_bit_list]


def bit_to_str(input_bit: list[int | str]) -> typing.AnyStr:
    """Convert list of 0 and 1 in either integer or string format to the original string."""
    data = bit_to_byte(input_bit)
    try:
        return data.decode('utf-8')
    except AttributeError:
        return data


def bit_to_byte(input_bit: list[int | str]) -> typing.AnyStr:
    """Convert list of 0 and 1 in either integer or string format to the original bytes."""
    bit_str_list = [str(a) for a in input_bit]
    int_list = []
    for g in range(0, len(bit_str_list), 8):
        int_list.append(int(''.join(bit_str_list[g:g + 8]), 2))
    bin_str = bytes(int_list)
    return bin_str


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


class Encryption(object):
    """Class for using AES-256 Encryption in a easier way."""

    def __init__(self, key: typing.AnyStr = None, enc_type: mode = None):
        self.aes = None
        self.key = key.zfill(32)[:32]
        self.enc_type = enc_type
        self.data: str | bytes = ''

    def setKey(self, key: typing.AnyStr):  # noqa: D102
        self.key = key.zfill(32)[:32]

    def setMode(self, enc_type: mode):  # noqa: D102
        if self.enc_type is not None:
            if self.enc_type != enc_type:
                raise ValueError('You are trying to assign a different mode to the one you have set before')
            else:
                pass
        self.enc_type = enc_type

    def setData(self, stream_content: str):
        """Set data to be encrypt or decrypt."""
        self.data = stream_content

    def getResult(self):
        """Get result of the encryption or decryption"""
        if self.data == '':
            raise ValueError('You are trying to encrypt/decrypt nothing')
        if self.enc_type is None or not isinstance(self.enc_type, mode):
            raise ValueError('Please choose a vaild encryption mode')
        if self.key is None:
            raise ValueError('Key have to be provided for the operation')
        self.aes = AES.new(key=self.key.encode('utf-8'), mode=AES.MODE_ECB)
        if self.enc_type == MODE_ENCRYPTION:
            if isinstance(self.data, bytes):
                msg = self.aes.encrypt(pad(self.data, BLOCK_SIZE))
            else:
                msg = self.aes.encrypt(pad(self.data.encode('utf-8'), BLOCK_SIZE))
            return msg
        if self.enc_type == MODE_DECRYPTION:
            if isinstance(self.data, bytes):
                msg = self.aes.decrypt(self.data)
            else:
                msg = self.aes.decrypt(self.data.encode('utf-8'))
            return unpad(msg, BLOCK_SIZE)

# if __name__ == '__main__':
#     enc_box = Encryption('test1', MODE_ENCRYPTION)
#     dec_box = Encryption('test1', MODE_DECRYPTION)
#     enc_box.setData('1234')
#     enc_data = enc_box.getResult()
#     print(enc_data)
#     bit_enc_data = str_to_bit(enc_data)
#     dec_box.setData(bit_to_byte(bit_enc_data))
#     dec_data = dec_box.getResult().decode('utf-8')
#     print(dec_data)
