#!/bin/bash
echo "Creating Migrations..."
python3 manage.py makemigrations
echo ====================================

echo "Starting Migrations..."
python3 manage.py migrate
echo ====================================

echo "Adding Categories..."
python3 codes/load_data.py
echo ====================================

echo "Starting Server..."
python3 manage.py runserver 0.0.0.0:8000