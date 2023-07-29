#!/bin/bash

python -m isort host/app.py server.py tests
python -m black host/app.py server.py tests
python -m flake8 host/app.py server.py tests
python -m mypy host/app.py server.py tests
