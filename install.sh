#!env bash

# create a virtual environment (venv)
python3 -m venv venv

# activate the venv
source venv/bin/activate

# install the requirements to the venv
pip install -r requirements.txt

# deactivate the venv
deactivate
