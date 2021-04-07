FROM dyne/devuan:beowulf

RUN echo "deb http://deb.devuan.org/merged chimaera main" >> /etc/apt/sources.list
RUN apt-get update -y -q --allow-releaseinfo-change
RUN apt-get install -y -q -t beowulf zsh cryptsetup gawk libgcrypt20-dev steghide qrencode python python2.7 python3-pip python3-dev libssl-dev make gcc g++ sudo gettext file bsdmainutils
RUN apt-get install -y -q -t chimaera libsodium23 libsodium-dev doas
RUN pip3 install setuptools wheel

COPY . /Tomb/

WORKDIR /Tomb/extras
RUN ./install_sphinx.sh

COPY extras/test/doas.conf /etc/doas.conf

WORKDIR /Tomb
RUN make --directory=extras/kdf-keys
RUN make --directory=extras/kdf-keys install
