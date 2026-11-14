PROG = tomb
PREFIX ?= /usr/local
MANDIR ?= ${PREFIX}/share/man

deps:
	@if [ -r /etc/debian_version ]; then \
	apt-get install -qy zsh cryptsetup file gnupg pinentry-curses; fi
	@if [ -r /etc/fedora-release ]; then \
	yum install -y zsh cryptsetup file gnupg pinentry-curses; fi
	@if [ -r /etc/alpine-release ]; then \
	apk add zsh cryptsetup file gpg pinentry-tty e2fsprogs findmnt; fi

all:
	@echo
	@echo "Tomb is a script and does not need compilation, it can be simply executed."
	@echo
	@echo "To install it in /usr/local together with its manpage use 'make install'."
	@echo
	@echo "To run Tomb one needs to have some tools installed on the system:"
	@echo "Sudo, cryptsetup, pinentry and gnupg."
	@echo

install:
	install -Dm755 ${PROG} ${DESTDIR}${PREFIX}/bin/${PROG}
	install -Dm644 doc/${PROG}.1 ${DESTDIR}${MANDIR}/man1/${PROG}.1
	@echo
	@echo "Tomb is installed successfully. To install language translations, make sure"
	@echo "gettext is also installed, then 'cd extras/translations' and 'make install' there."
	@echo
	@echo "Look around the extras/ directory, it contains other interesting modules."
	@echo

test:
	bash extras/test/run --suite all

test-smoke:
	bash extras/test/run --suite smoke

test-harness:
	python3 -m unittest discover -s extras/test/tests -v

test-legacy:
	$(MAKE) -C extras/test

test-qemu:
	bash extras/test/qemu/run --image "$(QEMU_IMAGE)"

.PHONY: test test-smoke test-harness test-legacy test-qemu

lint:
	shellcheck -s bash -e SC1058,SC1073,SC1072,SC1009 tomb
