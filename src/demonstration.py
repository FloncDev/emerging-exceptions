import asyncio

from PIL.Image import open

from EE import utils, loader

while True:
    if input('Encode/Decode[E/d]:').lower().startswith('E'):
        mode = utils.MODE_ENCRYPTION
    else:
        mode = utils.MODE_DECRYPTION
    match input('Option[Stego/Datastamp]:').lower():
        case 'stego':
            name = 'Stego'
        case 'datastamp':
            name = 'pixelQR'
    if input('Encode/Decode[E/d]:').lower().startswith('E'):
        mode = utils.MODE_ENCRYPTION
    else:
        mode = utils.MODE_DECRYPTION
    classes = loader.get_library_class(loader.get_script_path())[name]()
    if name == 'Stego' and mode == utils.MODE_ENCRYPTION:
        path_to_image = input('[Read    ]Path to original image: ')
        path_to_new = input('[Generate]Path to the encoded image: ').strip()
        if not path_to_new.endswith('.png'):
            path_to_new += '.png'
        encryption_key = input('Key: ')
        content = input('Content: ')
        return_data = asyncio.run(classes.routine(mode,
                                                  {'img': open(path_to_image), 'passcode': encryption_key,
                                                   'msg': content}))
        return_data['img_down'].save(path_to_new)
    elif name == 'Stego' and mode == utils.MODE_DECRYPTION:
        path_to_image = input('[Read    ]Path to the encoded image: ')
        encryption_key = input('Key: ')
        return_data = asyncio.run(classes.routine(mode, {'img': open(path_to_image), 'passcode': encryption_key}))
        print(f"Message: {return_data['msg'].decode('utf-8')}")
    elif name == 'pixelQR' and mode == utils.MODE_ENCRYPTION:
        path_to_new = input('[Generate]Path to the encoded image: ').strip()
        if not path_to_new.endswith('.png'):
            path_to_new += '.png'
        encryption_key = input('Key: ')
        content = input('Content: ')
        return_data = asyncio.run(
            classes.routine(mode, {'passcode': encryption_key, 'msg': content, 'en/dec': 'aes256'}))
        return_data['img_down'].save(path_to_new)
    elif name == 'pixelQR' and mode == utils.MODE_DECRYPTION:
        path_to_image = input('[READ    ]Path to the photo include encoded content: ')
        encryption_key = input('Key: ')
        return_data = asyncio.run(classes.routine(mode,
                                                  {'img': open(path_to_image), 'passcode': encryption_key,
                                                   'en/dec': 'aes256'}))
