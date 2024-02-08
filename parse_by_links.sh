#!/bin/bash
python3 -m venv venv
venv/source/bin/activate
pip install requirements.txt
python main.py