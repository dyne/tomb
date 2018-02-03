
PREFIX ?= /usr/local

all:
	$(CC) -O2 -o tomb-kdb-pbkdf2 pbkdf2.c -lgcrypt
	$(CC) -O2 -o tomb-kdb-pbkdf2-getiter benchmark.c -lgcrypt
	$(CC) -O2 -o tomb-kdb-pbkdf2-gensalt gen_salt.c -lgcrypt
	$(CC) -O2 -o tomb-kdb-hexencode hexencode.c

test:
	@echo "Running Tomb-kdb tests"
	./test.sh

clean:
	rm -f tomb-kdb-pbkdf2 tomb-kdb-pbkdf2-getiter tomb-kdb-pbkdf2-gensalt tomb-kdb-hexencode

install:
	install -Dm755 tomb-kdb-pbkdf2 ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2
	install -Dm755 tomb-kdb-pbkdf2-getiter ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2-getiter
	install -Dm755 tomb-kdb-pbkdf2-gensalt ${DESTDIR}${PREFIX}/bin/tomb-kdb-pbkdf2-gensalt
	install -Dm755 tomb-kdb-hexencode ${DESTDIR}${PREFIX}/bin/tomb-kdb-hexencode
	@echo "Tomb-kdb auxiliary binaries installed in ${DESTDIR}${PREFIX}/bin"
