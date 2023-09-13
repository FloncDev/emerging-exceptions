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
        if isinstance(data_input['img'], utils.pure_image):  # Check if the image is a image object
            init_image: PIL.Image.Image = data_input['img']
        elif isinstance(data_input['img'], utils.image):
            init_image: PIL.Image.Image = utils.load_image(data_input['img'])
        else:
            raise KeyError('Input data: img do not have a correct input')
        key = hashlib.sha512(data_input['passcode'].encode('utf-8')).hexdigest()  # Retrieve SHA-512 value of the key
        size = math.ceil(math.log2(init_image.size[0] * init_image.size[1]))  # Check 2**n size required to allocate any pixel
        integer_key = int(key, 16)  # Turn SHA-512 hex to integer
        if 2 ** (size * 6) > integer_key:  # Check the hash length is enough to allocate 6 pixel on the image
            raise ValueError('The length of the key is not sufficient for the size of the image')
        px = init_image.load()  # Load up Image access object
        protected_key_list, random_seed, pass_key = int_key_decode(integer_key + 1, init_image)
        # ^ Retrieve random seed and encryption key from the colour of 6 pixel select with the hash of the key
        random_instance = random.Random(x=random_seed)  # Retrieve the random instance from random seed
        if func_mode == utils.MODE_ENCRYPTION: # Check if it is encryption/encoding mode
            string_input = data_input['msg']  # Retrieve message from the data_input dictionary
            encryption_box = utils.Encryption(pass_key, utils.MODE_ENCRYPTION)  # Create the encryption box
            encryption_box.setData(string_input)  # Place the data to the encryption box
            data = encryption_box.getResult()  # Retrieve the byte data
            data_bit_list = utils.str_to_bit(data)  # Convert the vyte data to list of bit
            size_data = [int(num) for num in utils.base_convert(len(data_bit_list), 2).zfill(16)]
            # Create a list of 0 and 1 to represent the length of the data
            new_data_list = IDENTIFIER + size_data + data_bit_list  # Combine the list
            for bit in new_data_list:
                coord = get_coord(random_instance, init_image, protected_key_list)  # Retrieve a non-repeated coordinate
                protected_key_list.append(coord)  # Prevent the coordinate being reuse
                ori = px[coord[0], coord[1]]  # Retrieve color data of the coordinate
                px[coord[0], coord[1]] = (ori[0], ori[1], ((ori[2] // 2) * 2) + bit)  # Encode data to the coordinate
            return {'img_down': init_image}  # Return a PIL.Image.Image object

        if func_mode == utils.MODE_DECRYPTION:  # Check for decryption/decode mode
            i = 0  # Set index to 0
            identifier = []  # Preset list to save identifier data from image
            size = []  # Preset list to save size data from image
            while True:
                coord = get_coord(random_instance, init_image, protected_key_list)  # Retrieve coordinate
                if i in list(range(8)):
                    identifier.append(px[coord[0], coord[1]][2] % 2)
                    # Retrieve data on the last significant bit of the Blue channel and append to identifier list
                if i == 8:
                    if IDENTIFIER != identifier:  # Raise error when identifier detected do not match the one specify
                        return {'msg': 'Identifier not matched'}
                if i in list(range(8, 24)):
                    size.append(px[coord[0], coord[1]][2] % 2)  # Retrieve size bit and append to size list
                if i == 23:  # Pause data retrieve after 24 bit
                    break
                i += 1  # Add index by 1 to acknowledge when to stop the while loop
            i = 0  # Reset index to 0
            int_size = int(''.join([str(s) for s in size]), 2)  # Convert list[int] of size data to integer
            data = []  # Preset data list to store bit data
            while True:
                coord = get_coord(random_instance, init_image, protected_key_list)  # Retrieve coordinate
                if i in range(int_size):
                    data.append(px[coord[0], coord[1]][2] % 2)  # Append data bit to the list
                    i += 1  # Add index by 1
                else:
                    break
            decryption_box = utils.Encryption(key=pass_key, enc_type=utils.MODE_DECRYPTION)  # Setup decryption boxx
            decryption_box.setData(utils.bit_to_byte(data))  # Set data to byte data converted from bit data
            result = decryption_box.getResult()  # Get decrypted result
            return {'msg': result}  # Return decrypted result


if __name__ == '__main__':
    lib = Steganography()
    img_obj = asyncio.run(
        lib.routine(utils.MODE_ENCRYPTION, {'img': PIL.Image.open('img.png'), 'passcode': 'test', 'msg': 'test'}))
    img_obj['img_down'].save('img_new.png')
    return_data = asyncio.run(lib.routine(utils.MODE_DECRYPTION, {'img': PIL.Image.open('img_new.png'), 'passcode': 'test'}))
    print(return_data)
