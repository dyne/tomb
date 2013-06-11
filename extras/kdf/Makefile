
all:
	gcc -O2 -o tomb-kdb-pbkdf2 pbkdf2.c -lgcrypt
	gcc -O2 -o tomb-kdb-pbkdf2-getiter benchmark.c -lgcrypt
	gcc -O2 -o tomb-kdb-pbkdf2-gensalt gen_salt.c -lgcrypt
	gcc -O2 -o hexencode hexencode.c

clean:
	rm -f tomb-kdb-pbkdf2-getiter tomb-kdb-pbkdf2 tomb-kdb-pbkdf2-gensalt hexencode