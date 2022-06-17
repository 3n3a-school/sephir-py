#!/bin/bash

cd /tmp
mkdir install-webdriver
cd install-webdriver

wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
tar -xvf *.tar.gz
sudo cp -ar geckodriver /usr/local/bin/

ls -l
cd /tmp
rm -rf /tmp/install-webdriver