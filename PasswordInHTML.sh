#!/bin/bash

file="$PWD/venv"
path=$PWD
path_to_ico="$PWD/PasswordInHTML.ico"
open_file="$PWD/PasswordInHTML.sh"
open_application="$PWD/PasswordInHTML.py"

if [ -d $file ]; then
	$PWD/venv/bin/python3 PasswordInHTML.py
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

	echo "Создать ярлык программы? [y,n]"
	read yesorno

	if [[ $yesorno == y* ]]; then
    	echo "Создаю ярлык"
		cd /usr/share/applications/
		sudo touch PasswordInHTML.desktop  
		echo "[Desktop Entry]
Name=PasswordInHTML
Comment=Программа для хранения паролей
Exec=sh $open_file
Terminal=false
Type=Application
Icon=$path_to_ico
Path=$path
Categories=System" | sudo tee PasswordInHTML.desktop
	else
    	echo "Отмена создани ярлыка"
	fi

	echo "!!!!!Запуск программы!!!!!"
	cd $path
	python3 $open_application
fi