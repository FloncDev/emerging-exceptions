import json
import os
from io import BytesIO
import traceback
import PIL.Image
from typing import Annotated, Union

import requests
from dotenv import dotenv_values, find_dotenv
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
import random

try:
    from src.EE.ui.components import Dropdown, Select, SelectOption, Text, TextType
    from src.EE import loader, utils
except ImportError:
    from EE.ui.components import Dropdown, Select, SelectOption, Text, TextType
    from EE import loader, utils


app = FastAPI()
env = dotenv_values(find_dotenv())
pathname = []
with open("README.md") as f:
    text = f.read()

url = "https://api.github.com/markdown"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {env['GITHUB_TOKEN']}",
}

rendered_md = requests.request("POST", url, json={"text": text}, headers=headers).text

rendered_md = (
    rendered_md.replace(">\n<", "><")
    .replace("/div>\n", "/div>")
    .replace("\n", "<br>")
    .replace('"', "")
)


@app.get("/rendered_readme")
async def get_readme():
    """Returns a rendered version of the GitHub README.md"""
    return rendered_md


@app.get("/youtube_id")
async def get_youtube_id():
    """Gets the youtube id form pastebin"""
    return requests.get("https://pastebin.com/raw/Eqm7FezB").content


@app.get("/app")
async def get_app():
    """Returns the app page with all the inputs filled in"""
    with open("src/frontend/app.html") as f:
        return HTMLResponse(f.read())


@app.get("/components")
async def components(module: str = "fourier", encode: bool = False):
    """Return components as html"""
    class_dict = loader.get_library_class(loader.get_script_path())
    print(class_dict)
    match module:
        case "fourier":
            name = 'fourier'

            # options = [
            #     SelectOption("One", "1"),
            #     SelectOption("Two", "2"),
            #     SelectOption("Three", "3"),
            # ]
            # options2 = [
            #     SelectOption("One", "11"),
            #     SelectOption("Two", "22"),
            #     SelectOption("Three", "33"),
            # ]
            # components = [
            #     Text("Title here", "asd", TextType.Small, "Hello, World!"),
            #     Text("Title here", "asdc", TextType.Large, "Hello, World!"),
            #     Select("Hello", "hi", options),
            #     Dropdown("Asd", "g", options2),
            # ]
            #
            # if not encode:
            #     for comp in components:
            #         comp.title = "Another title"


        case "datastamp":
            name = 'pixelQR'


        case "steg":
            name = 'Stego'
    try:
        classes = class_dict[name]()
        components = loader.getOption(classes, encode)
        print(components)
    except:
        components = []
        print('failed')

    with open("src/frontend/components/style.html") as f:
        # noinspection PyUnboundLocalVariable
        html = f.read() + "\n".join(i.html() for i in components)

    return HTMLResponse(html)


@app.post("/process")
async def process_image(
    data: Annotated[str, Form()] = None,
    image: Annotated[Union[None, UploadFile], Form()] = None,
):
    """Process the image with the defined options"""
    class_dict = loader.get_library_class(loader.get_script_path())
    if len(pathname) != 0:
        for pathname_item in pathname:
            os.remove(pathname_item)
            pathname.remove(pathname_item)
    data = json.loads(data)
    img_bytes = BytesIO(await image.read())
    img_obj = PIL.Image.open(img_bytes)
    inputs_data = data['inputs']
    encode = data['is_encode']
    # PIL.Image.open(img_bytes) to open as pillow image
    encode_id = utils.MODE_ENCRYPTION if encode else utils.MODE_DECRYPTION
    print(data)
    inner_data = json.loads(data['inputs'])
    match data["module"]:
        case "fourier":
            name = 'fourier'
            try:
                inner_data['img'] = img_obj
            except:
                return 'Error: PNG image not detected'
            return_data = 'img'
            # print(img_bytes)  # replace with data image stuff

        case "datastamp":
            name = 'pixelQR'
            if not encode:
                try:
                    inner_data['img'] = img_obj
                except:
                    return 'Error: PNG image not detected'
                return_data = 'msg'
            else:
                return_data = 'img'

        case "steg":
            name = 'Stego'
            try:
                inner_data['img'] = img_obj
            except:
                return 'Error: PNG image not detected'
            if encode:
                return_data = 'img'
            else:
                return_data = 'msg'
    print(return_data)
    try:
        return_dict = await class_dict[name]().routine(encode_id, inner_data)
        if return_data == 'img':
            img_data: PIL.Image.Image = return_dict['img_down']
            print(type(img_data))
            print(type(img_data.tobytes()))
            pathname_gen = ''.join(random.choices('0123456789abcdef', k=32)) + '.png'
            # img_data.save(pathname_gen)
            # pathname.append(pathname_gen)
            with BytesIO() as byte_data:
                img_data.save(byte_data, format='png')
                byte_data.seek(0)
                response = Response(byte_data.read(), media_type="image/png")
                return response
            # return Response(img_data.tobytes(), media_type="image/png")
        else:
            return return_dict['msg']
    except:
        traceback.print_exc()
        return 'Failed'

    # return Response(img_bytes.read(), media_type="image/png")
    # return "Text example"


# Make sure this is always at the bottom
app.mount("/", StaticFiles(directory="src/frontend", html=True))
