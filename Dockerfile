FROM python:3.11

COPY . /app
WORKDIR /app

RUN rm -r .venv

RUN pip install poetry
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.backend.main:app", "--port", "8000", "--host", "0.0.0.0"]
