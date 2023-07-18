#!/bin/bash

python -m isort host server.py tests
python -m black host server.py tests
python -m flake8 host server.py tests
