# pull official base image
FROM python:3.9.9-buster

# set work directory
WORKDIR /app/


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

# install dependencies
RUN poetry install --no-dev --no-ansi

# copy entrypoint.sh
#COPY ./entrypoint.sh .

# copy project
COPY . /app/

EXPOSE 8000

#ENV HOME /home/$CELERY_USER
#ENV PATH="$HOME/.pyenv/bin:$PATH"

# run entrypoint.sh
#RUN #chmod +x ./entrypoint.sh
#ENTRYPOINT ["bash", "./entrypoint.sh"]
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["bash", "./entrypoint.sh"]
