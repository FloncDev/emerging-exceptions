import asyncio
import base64
import random

# import ImageDecoding
# import ImageEncoding

try:
    from .. import utils
    import ImageDecoding
    import ImageEncoding
except ImportError:
    from EE import utils
    from EE.pixelQR import ImageDecoding, ImageEncoding


class PixelQR(utils.LibraryBase):  # noqa: E501
    """Class for access to Scannable Image."""

    def __init__(self):
        super().__init__()
        self.enc_input = [{"field": "Encryption Method", 'options': [{"name": "No encryption", "id": "none"},
                                                                     {"name": "AES-256", "id": "aes256"}],
                           'type': 'select', 'id': 'en/dec'},
                          {"field": "Message", 'type': 'text_large', 'id': 'msg'},
                          {"field": "Password(Optional if you have encryption)", 'type': 'text_small',
                           'id': 'passcode'}]
        self.dec_input = [{"field": "Encryption Method", 'options': [{"name": "No encryption", "id": "none"},
                                                                     {"name": "AES-256", "id": "aes256"}],
                           'type': 'select', 'id': 'en/dec'},
                          {"field": "Password(Optional if you have encryption)", 'type': 'text_small',
                           'id': 'passcode'},
                          {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.enc_output = [{"type": "image_button", "id": "img_down"}]
        self.dec_output = [{"type": "msg", "id": "msg"}]

    async def routine(self, func_mode: utils.mode, data_input: dict):  # noqa: C901
        """Routine for the entire image process with given input."""
        if func_mode == utils.MODE_ENCRYPTION:
            if data_input['en/dec'] == 'aes256':
                encryption_box = utils.Encryption(data_input['passcode'], utils.MODE_ENCRYPTION)
                encryption_box.setData(data_input['msg'].encode('utf-8'))
                data = base64.b64encode(encryption_box.getResult()).decode('utf-8')
            else:
                data = data_input['msg']
            img_obj = ImageEncoding.str_to_image(data)
            return {'img_down': img_obj}
        if func_mode == utils.MODE_DECRYPTION:
            if data_input['en/dec'] == 'aes256':
                data = ImageDecoding.photo_to_str(data_input['img'])
                bytedata = base64.b64decode(data)
                decryption_box = utils.Encryption(data_input['passcode'], utils.MODE_DECRYPTION)
                decryption_box.setData(bytedata)
                result = decryption_box.getResult().decode('utf-8')
            else:
                result = ImageDecoding.photo_to_str(data_input['img'])
            return {'msg': result}


if __name__ == '__main__':
    lib = PixelQR()
    path = asyncio.run(
        lib.routine(utils.MODE_ENCRYPTION, {'passcode': 'test',
                                            'msg': 'test', 'en/dec': 'aes256'}))
    print(asyncio.run(lib.routine(utils.MODE_DECRYPTION, {'passcode': 'test',
                                                          'en/dec': 'aes256', 'img': path['img_down']})))
