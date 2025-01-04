#!/usr/bin/env bash
set -e

pipenv shell
flask --app src.app db upgrade
pipenv run gunicorn src.wsgi:app