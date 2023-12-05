#!/usr/bin/env bash
pip install requirements-parser
python3 ./src/assets/tools/flatpak-pip-generator --yaml -r requirements.txt
echo 'Done! See python3-requirements.yaml'