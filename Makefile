
PREFIX ?= /usr/local

all:
	@echo "Tomb is a script and does not need compilation, it can be simply executed."
	@echo "To install it in /usr/local together with its manpage use 'make install'."

install:
	install tomb $(PREFIX)/bin
	install doc/tomb.1 $(PREFIX)/share/man/man1
