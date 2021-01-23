#!/bin/sh
set -ex
git clone https://github.com/stef/libsphinx 
cd libsphinx
git submodule update --init --recursive --remote
cd src
sed -i 's|/usr/local|/usr|' makefile
make && make install && ldconfig
cd ../..
git clone https://github.com/stef/pwdsphinx
cd pwdsphinx
python3 setup.py install
mkdir -p /etc/sphinx && cp ../test/sphinx.cfg /etc/sphinx/config && cd /etc/sphinx
openssl req -new -x509 -nodes -out server.crt -keyout server.key -subj '/CN=localhost'
sphinx init
