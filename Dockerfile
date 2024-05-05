FROM python:3.10-slim
WORKDIR /app

RUN pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

COPY . .

CMD ["python", "./app/main.py"]