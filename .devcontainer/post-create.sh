#! /bin/bash

# loads environment variables from .env when shell starts
PRE='export $(cat '
POST='/.env | xargs)'
CMD=$PRE$1$POST
echo $CMD >> ~/.bashrc

# install poetry
poetry config virtualenvs.in-project true
poetry install --no-root
