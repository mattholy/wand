FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

LABEL maintainer="Mattholy <mattholy@kryta.app>"

COPY ./app /app

ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt