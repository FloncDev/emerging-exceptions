import requests
from dotenv import dotenv_values, find_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
env = dotenv_values(find_dotenv())

with open("README.md") as f:
    text = f.read()

url = "https://api.github.com/markdown"

payload = "{\"text\":\"Hello **world**\"}"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {env['GITHUB_TOKEN']}"
}

rendered_md = requests.request("POST", url, json={"text": text}, headers=headers).text

rendered_md = rendered_md \
    .replace(">\n<", "><") \
    .replace("/div>\n", "/div>") \
    .replace("\n", "<br>")


@app.get("/rendered_readme")
async def get_readme():
    """Returns a rendered version of the GitHub README.md"""
    return rendered_md

# Make sure this is always at the bottom
app.mount("/", StaticFiles(directory="src/frontend", html=True))
