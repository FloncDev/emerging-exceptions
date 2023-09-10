# Emerging Exceptions

## Developer Environment Setup

We are using [Poetry](https://python-poetry.org/) for dependency management, to install:
```shell
pip install poetry
poetry config virtualenvs.in-project true
poetry install
```

and then to use the virtual environment (optional but recommended):
```shell
poetry shell
```
And then to exit, simply `exit`.

To run the web server, from the root directory run:
```shell
uvicorn src.backend.main:app --port 8080
```

On some rare case, `EE` cannot be loaded correctly in `../src/EE`.
You can run this from the root directory:

```shell
pip install -e ./src/
```

