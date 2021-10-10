#!/bin/bash

echo "!!!!!Создание виртуального окружения!!!!!"
sleep 2
python3 -m venv venv
source "$PWD/venv/bin/activate"

echo "!!!!!Установка зависимостей!!!!!"
sleep 2
pip install wheel
pip install -r requirements.txt

echo "!!!!!Запуск программы!!!!!"
python3 updater.py
