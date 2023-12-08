FROM python:3.10
LABEL maintainer = "julianwalter1593@gmail.com"

COPY ./requirements.txt /requirements.txt
COPY ./olxcrawler /olxcrawler
WORKDIR /olxcrawler

RUN python -m venv venv && \
    venv/bin/pip install --upgrade pip && \
    venv/bin/pip install -r ../requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH = "/olxcrawler/venv/bin:$PATH"

USER django-user

RUN /bin/bash -c "source /olxcrawler/venv/bin/activate"
