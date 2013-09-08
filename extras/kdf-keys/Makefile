
PREFIX ?= /usr/local

all:
	gcc -O2 -o tomb-kdb-pbkdf2 pbkdf2.c -lgcrypt
	gcc -O2 -o tomb-kdb-pbkdf2-getiter benchmark.c -lgcrypt
	gcc -O2 -o tomb-kdb-pbkdf2-gensalt gen_salt.c -lgcrypt
	gcc -O2 -o hexencode hexencode.c

clean:
	rm -f tomb-kdb-pbkdf2 tomb-kdb-pbkdf2-getiter tomb-kdb-pbkdf2-gensalt hexencode

install:
	install -Dm755 tomb-kdb-pbkdf2 ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2
	install -Dm755 tomb-kdb-pbkdf2-getiter ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2-getiter
	install -Dm755 tomb-kdb-pbkdf2-gensalt ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2-gensalt
	install -Dm755 hexencode ${DESTDIR}${PREFIX}/bin/hexencode
	@echo "Tomb-kdb auxiliary binaries installed in ${PREFIX}"
