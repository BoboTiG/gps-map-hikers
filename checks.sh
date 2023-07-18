#!/bin/bash

python -m isort host server.py
python -m black host server.py
python -m flake8 host server.py
