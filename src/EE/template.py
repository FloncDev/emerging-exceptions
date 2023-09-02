"""Basic template to create a plugin"""
import utils


class LibraryExample(utils.LibraryBase):  # noqa: D101
    def __init__(self):
        super().__init__()
        self.enc_input = [{"field": "Encryption Method", 'options': [{"name": "No encryption", "id": "none"}],
                           'type': 'select', 'id': 'en/dec'},
                          {"field": "Message", 'type': 'text_large', 'id': 'msg'},
                          {"field": "Secret(Required to decrypt the image)", 'type': 'text_small', 'id': 'passcode'},
                          {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.dec_input = [{"field": "Encryption Method", 'options': [{"name": "No encryption", "id": "none"}],
                           'type': 'select', 'id': 'en/dec'},
                          {"field": "Secret(Required to decrypt the image)", 'type': 'text_small', 'id': 'passcode'},
                          {"field": "Image", 'type': 'image_button', 'id': 'img'}]
        self.enc_output = [{"type": "image_button", "id": "img_down"}]
        self.dec_output = [{"type": "msg", "id": "msg"}]

    async def routine(self, mode: utils.mode, data_input: dict):  # noqa: D102
        if mode == utils.MODE_ENCRYPTION:
            return {"id": "img_down", "data": data_input['img']}
        if mode == utils.MODE_DECRYPTION:
            return {"id": "msg", "data": "test data"}
