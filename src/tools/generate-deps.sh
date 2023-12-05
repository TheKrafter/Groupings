#!/usr/bin/env bash
pip install requirements-parser
python3 ./src/tools/flatpak-pip-generator --yaml -r requirements.txt