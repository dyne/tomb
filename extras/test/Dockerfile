FROM dyne/devuan:beowulf

RUN apt-get update -y -q && apt-get install -y -q zsh cryptsetup gawk libgcrypt20-dev steghide qrencode python python2.7 python3-pip python3-dev libsodium-dev libssl-dev make gcc g++ sudo gettext file bsdmainutils
RUN pip3 install setuptools wheel

COPY . /Tomb/

WORKDIR /Tomb/extras
RUN ./install_sphinx.sh
RUN cp test/sphinx.cfg /etc/sphinx/config

WORKDIR /Tomb
RUN make --directory=extras/kdf-keys
RUN make --directory=extras/kdf-keys install