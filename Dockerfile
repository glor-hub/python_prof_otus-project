# pull official base image
FROM python:3.9.9-buster

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock

# install dependencies
RUN poetry install --no-dev --no-ansi

# copy entrypoint.sh
COPY ./entrypoint.sh ./entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["bash", "./entrypoint.sh"]
