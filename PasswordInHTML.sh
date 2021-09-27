#!/bin/bash

file="$PWD/venv"

if [ -d $file ]; then
	$PWD/venv/bin/python3 main.py
else
	echo "!!!!!Обновление python3 до актуальной версии!!!!!"
	sudo apt reinstall python3 -y
	sudo apt install xclip

	echo "!!!!!Установка python3-venv!!!!!"
	sleep 2
	sudo apt install python3-venv -y

	echo "!!!!!Установка python3-tk=3.8.5-1~20.04.1!!!!!"
	sleep 2
	sudo apt install python3-tk=3.8.5-1~20.04.1


	echo "!!!!!Установка python3-pip!!!!!"
	sleep 2
	sudo apt install python3-pip -y

	echo "!!!!!Создание виртуального окружения!!!!!"
	sleep 2
	python3 -m venv venv
	source "$PWD/venv/bin/activate"
	echo "!!!!!Установка зависимостей!!!!!"
	sleep 2
	pip3 install wheel
	pip3 install -r requirements.txt

	echo "!!!!!Запуск программы!!!!!"
	python3 main.py
fi