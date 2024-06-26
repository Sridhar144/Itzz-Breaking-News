#!/bin/bash

echo "BUILD START"
python3.9 -m ensurepip
python3.9 -m pip install --upgrade pip

# Install dependencies
python3.9 -m pip install -r requirements.txt
cd News-Aggregator

# Collect static files
python3.9 manage.py collectstatic --noinput --clear --settings=News-Aggregator.settings

# Move the collected static files to the correct directory
mkdir -p ../staticfiles_build
cp -r static/* ../staticfiles_build/

echo "BUILD END"
