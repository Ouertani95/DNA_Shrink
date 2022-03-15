#!/bin/bash

cd /usr/local/lib/python3.8/dist-packages/
sudo rm dnashrink_bioinfo-0.1.0-py3.8.egg easy-install.pth
cd /usr/local/bin
sudo rm easy_install dnashrink
cd
cd Desktop/S2_Master/ALGO/PROJET_ALGO/
sudo rm -r build/ dist/ dnashrink_bioinfo.egg-info/