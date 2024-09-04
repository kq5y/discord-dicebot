FROM python:3.10-slim
WORKDIR /app

ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "-u", "./app/main.py"]