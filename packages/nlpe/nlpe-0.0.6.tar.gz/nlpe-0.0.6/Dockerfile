# syntax = docker/dockerfile:1
ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION
WORKDIR /nlpe

# install nlpe
COPY . .
RUN pip install .

