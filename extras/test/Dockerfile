FROM dyne/devuan:chimaera

RUN echo "deb http://deb.devuan.org/merged chimaera main" >> /etc/apt/sources.list
RUN apt-get update -y -q --allow-releaseinfo-change
RUN apt-get install -y -q zsh cryptsetup gpg gawk libgcrypt20-dev steghide qrencode python python2.7 python3-pip python3-dev libssl-dev make gcc sudo gettext bsdmainutils file pinentry-curses xxd libsodium23 libsodium-dev doas
RUN pip3 install setuptools wheel

COPY . /Tomb/

COPY extras/test/doas.conf /etc/doas.conf
RUN chmod 400 /etc/doas.conf

WORKDIR /Tomb
RUN make --directory=extras/kdf-keys
RUN make --directory=extras/kdf-keys install
