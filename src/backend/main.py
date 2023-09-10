import json
from io import BytesIO
from typing import Annotated

import requests
from dotenv import dotenv_values, find_dotenv
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.EE.ui.components import Dropdown, Select, SelectOption, Text, TextType

app = FastAPI()
env = dotenv_values(find_dotenv())

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
    match module:
        case "fourier":
            options = [
                SelectOption("One", "1"),
                SelectOption("Two", "2"),
                SelectOption("Three", "3"),
            ]
            options2 = [
                SelectOption("One", "11"),
                SelectOption("Two", "22"),
                SelectOption("Three", "33"),
            ]
            components = [
                Text("Title here", "asd", TextType.Small, "Hello, World!"),
                Text("Title here", "asdc", TextType.Large, "Hello, World!"),
                Select("Hello", "hi", options),
                Dropdown("Asd", "g", options2),
            ]

            if not encode:
                for comp in components:
                    comp.title = "Another title"

        case "datastamp":
            components = [Text("Title here", "asd", TextType.Small, "Hello, World!")]

        case "steg":
            components = [Text("Title here", "asd", TextType.Small, "Hello, World!")]

    with open("src/frontend/components/style.html") as f:
        html = f.read() + "\n".join(i.html() for i in components)

    return HTMLResponse(html)


@app.post("/process")
async def process_image(
    image: Annotated[UploadFile, Form()], data: Annotated[str, Form()]
):
    """Process the image with the defined options"""
    data = json.loads(data)
    img_bytes = BytesIO(await image.read())
    # PIL.Image.open(img_bytes) to open as pillow image

    match data["module"]:
        case "fourier":
            print(img_bytes)  # replace with data image stuff

        case "datastamp":
            pass

        case "steg":
            pass


# Make sure this is always at the bottom
app.mount("/", StaticFiles(directory="src/frontend", html=True))
