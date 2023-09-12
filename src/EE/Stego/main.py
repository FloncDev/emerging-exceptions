import asyncio
import hashlib
import math
import random

import PIL.Image

try:
    from .. import utils
except ImportError:
    from EE import utils

IDENTIFIER = [0, 1, 1, 0, 1, 0, 1, 1]


def decode_key(key: int, size: int, length: int) -> list[int]:  # noqa: D103
    keyList = []
    for i in range(length, 0, -1):
        keyList.append((key % (size ** i)) // (size ** (i - 1)))
    return keyList


def list_int_to_int(int_list: list[int], max_int: int) -> int:  # noqa: D103
    num = 0
    for i, a in enumerate(int_list):
        num += a * (max_int ** i)
    return num


def int_key_decode(int_key: int, img: PIL.Image.Image) -> tuple[list[tuple[int, int]], int, str]:  # noqa: D103
    key_list = decode_key(int_key, img.size[0] * img.size[1], 6)
    coord_list_0 = []
    protected_coord_list = []
    for key_data in key_list:
        data = (key_data % img.size[0], key_data // img.size[0])
        coord_list_0.append(data)
        protected_coord_list.append(data)
    # noinspection PyTypeChecker
    px = img.load()
    colour_data_0 = [px[x, y] for x, y in coord_list_0]
    colour_data_0_int = [list_int_to_int(d, 256) for d in colour_data_0]
    random_seed = (colour_data_0_int[0] * colour_data_0_int[1]) + 1
    pass_key = utils.bit_to_byte(list(utils.base_convert(
        (colour_data_0_int[2] * colour_data_0_int[3] * colour_data_0_int[4] * colour_data_0_int[5]) + 1, 2)))
    return protected_coord_list, random_seed, pass_key


def get_coord(random_instance: random.Random, img: PIL.Image.Image, protected: list) -> tuple[int, int]:  # noqa: D103
    while True:
        coord = (random_instance.randint(0, img.size[0] - 1),
                 random_instance.randint(0, img.size[1] - 1))
        if coord in protected:
            continue
        else:
            return coord


class Steganography(utils.LibraryBase):  # noqa: E501
    """Class for access to Steganography."""

    def __init__(self):
        super().__init__()
        self.enc_input = [{"field": "Message", 'type': 'text_large', 'id': 'msg'},
                          {"field": "Secret(Required to decrypt the image)", 'type': 'text_small', 'id': 'passcode'},
                          {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.dec_input = [{"field": "Secret(Required to decrypt the image)", 'type': 'text_small', 'id': 'passcode'},
                          {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.enc_output = [{"type": "image_button", "id": "img_down"}]
        self.dec_output = [{"type": "msg", "id": "msg"}]

    async def routine(self, func_mode: utils.mode, data_input: dict):  # noqa: C901
        """Routine for the entire image process with given input."""
        if isinstance(data_input['img'], utils.pure_image):
            init_image: PIL.Image.Image = data_input['img']
        elif isinstance(data_input['img'], utils.image):
            init_image: PIL.Image.Image = utils.load_image(data_input['img'])
        else:
            raise KeyError('Input data: img do not have a correct input')
        key = hashlib.sha512(data_input['passcode'].encode('utf-8')).hexdigest()
        size = math.ceil(math.log2(init_image.size[0] * init_image.size[1]))
        integer_key = int(key, 16)
        if 2 ** (size * 6) > integer_key:
            raise ValueError('The length of the key is not sufficient for the size of the image')
        px = init_image.load()
        protected_key_list, random_seed, pass_key = int_key_decode(integer_key + 1, init_image)
        random_instance = random.Random(x=random_seed)
        if func_mode == utils.MODE_ENCRYPTION:
            string_input = data_input['msg']
            encryption_box = utils.Encryption(pass_key, utils.MODE_ENCRYPTION)
            encryption_box.setData(string_input)
            data = encryption_box.getResult()
            data_bit_list = utils.str_to_bit(data)
            size_data = [int(num) for num in utils.base_convert(len(data_bit_list), 2).zfill(16)]
            new_data_list = IDENTIFIER + size_data + data_bit_list
            for bit in new_data_list:
                coord = get_coord(random_instance, init_image, protected_key_list)
                protected_key_list.append(coord)
                ori = px[coord[0], coord[1]]
                px[coord[0], coord[1]] = (ori[0], ori[1], ((ori[2] // 2) * 2) + bit)
            return {'img_down': init_image}

        if func_mode == utils.MODE_DECRYPTION:
            i = 0
            identifier = []
            size = []
            while True:
                coord = get_coord(random_instance, init_image, protected_key_list)
                if i in list(range(8)):
                    identifier.append(px[coord[0], coord[1]][2] % 2)
                if i == 8:
                    if IDENTIFIER != identifier:
                        return {'msg': 'Identifier not matched'}
                if i in list(range(8, 24)):
                    size.append(px[coord[0], coord[1]][2] % 2)
                if i == 23:
                    break
                i += 1
            i = 0
            int_size = int(''.join([str(s) for s in size]), 2)
            data = []
            while True:
                coord = get_coord(random_instance, init_image, protected_key_list)
                if i in range(int_size):
                    data.append(px[coord[0], coord[1]][2] % 2)
                    i += 1
                else:
                    break
            decryption_box = utils.Encryption(key=pass_key, enc_type=utils.MODE_DECRYPTION)
            decryption_box.setData(utils.bit_to_byte(data))
            result = decryption_box.getResult()
            return {'msg': result}


if __name__ == '__main__':
    lib = Steganography()
    img_obj = asyncio.run(
        lib.routine(utils.MODE_ENCRYPTION, {'img': PIL.Image.open('img.png'), 'passcode': 'test', 'msg': 'test'}))
    img_obj['img_down'].save('img_new.png')
    return_data = asyncio.run(lib.routine(utils.MODE_DECRYPTION, {'img': PIL.Image.open('img_new.png'), 'passcode': 'test'}))
    print(return_data)
