import requests
from dotenv import dotenv_values, find_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.EE.ui.components import Text, TextType

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
            components = []

        case "datastamp":
            components = []

        case "steg":
            components = [Text("Title here", "asd", TextType.Small, "Hello, World!")]
            print(components[0].type)

    with open("src/frontend/components/style.html") as f:
        html = f.read() + "\n".join(i.html() for i in components)

    return HTMLResponse(html)


# Make sure this is always at the bottom
app.mount("/", StaticFiles(directory="src/frontend", html=True))
