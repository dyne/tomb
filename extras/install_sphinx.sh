#!/bin/sh
set -ex
git clone https://github.com/stef/libsphinx 
cd libsphinx
git submodule update --init --recursive --remote
cd src
sed -i 's|/usr/local|/usr|' makefile
make
sudo make install
ldconfig
pip3 install pwdsphinx
sudo mkdir -p /etc/sphinx