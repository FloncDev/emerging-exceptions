import typing
from abc import ABC, abstractmethod

MODE_ENCRYPTION = 0xFFFF0800
MODE_DECRYPTION = 0xFFFF0801
mode: typing.TypeAlias = MODE_ENCRYPTION | MODE_DECRYPTION


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
