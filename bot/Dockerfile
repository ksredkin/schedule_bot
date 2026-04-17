FROM python:3.14
RUN pip install poetry

COPY . /app
WORKDIR /app

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "__main__.py"]