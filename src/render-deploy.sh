#!/usr/bin/env bash
set -e

pipenv shell
flask --app src.app db upgrade
gunicorn src.wsgi:app