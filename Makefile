PROG = tomb
PREFIX ?= /usr/local
MANDIR ?= /usr/share/man

all:
	@echo
	@echo "Tomb is a script and does not need compilation, it can be simply executed."
	@echo
	@echo "To install it in /usr/local together with its manpage use 'make install'."
	@echo
	@echo "To run Tomb one needs to have some tools installed on the system:"
	@echo "Sudo, cryptsetup, pinentry and gnupg. Also wipe is recommended."
	@echo

install:
	@install -Dm755 ${PROG} ${DESTDIR}${PREFIX}/bin/${PROG}
	@install -Dm666 doc/${PROG}.1 ${DESTDIR}${MANDIR}/man1/${PROG}.1

test:
	make -C extras/test
