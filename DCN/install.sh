#!/bin/bash

sudo apt-get install -y build-essential checkinstall
sudo apt-get install -y screen
sudo apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

cd /opt
sudo wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tgz
sudo tar xzf Python-3.8.1.tgz

cd Python-3.8.1
sudo ./configure --enable-optimizations
sudo make altinstall

cd /opt
sudo rm -f Python-3.8.1.tgz

pip3.8 install openpyxl==3.0.3 mysql-connector-python==8.0.19 python-nmap==0.6.1 webdavclient3
