#!/bin/sh

set -e

sudo ln -sfn /etc/nginx/sites-available/maintenance.conf /etc/nginx/sites-enabled/nginx.conf
sudo systemctl reload nginx.service


# Stop the application

sudo systemctl stop portfolio-webapp-gunicorn.service

# Update code

cd /home/wagtail/portfolio-webapp
git pull origin main


# Activate virtual environment

source venv/bin/activate


# Install Python dependencies

python3 -m pip install --upgrade pip
pip install .


# Set up Django server

python manage.py migrate --noinput
python compile_scss.py
python manage.py collectstatic --noinput


# Start Django server

sudo systemctl start portfolio-webapp-gunicorn.service


# Change back to normal mode

sudo ln -sfn /etc/nginx/sites-available/standard.conf /etc/nginx/sites-enabled/nginx.conf
sudo systemctl reload nginx.service