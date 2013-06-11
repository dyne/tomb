#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/time.h>

#include <gcrypt.h>

static long bench(int ic) {
	char *pass = "mypass";
	unsigned char *salt = "abcdefghijklmno";
	int salt_len = strlen(salt);
	int result_len = 64;
	unsigned char *result = calloc(result_len, sizeof(char));
	struct timeval start, end;
	long microtime;

	gettimeofday(&start, NULL);
	gcry_kdf_derive( pass, strlen(pass), GCRY_KDF_PBKDF2, GCRY_MD_SHA1, salt, salt_len, ic, result_len, result);
	gettimeofday(&end, NULL);
	microtime = 1000000*end.tv_sec+end.tv_usec - (1000000*start.tv_sec+start.tv_usec);

	return (long)microtime;
}
int main(int argc, char *argv[])
{
	long desired_time = 1000000;
	long microtime;
	int ic=100;
	int tries=0;
	if(argc >= 2)
		sscanf(argv[1], "%ld", &desired_time);
	if (!gcry_check_version ("1.5.0")) {
		fputs ("libgcrypt version mismatch\n", stderr);
		exit (2);
	}
	/* Allocate a pool of 16k secure memory.  This make the secure memory
	available and also drops privileges where needed.  */
	gcry_control (GCRYCTL_INIT_SECMEM, 16384, 0);
	/* It is now okay to let Libgcrypt complain when there was/is
	a problem with the secure memory. */
	gcry_control (GCRYCTL_RESUME_SECMEM_WARN);
	/* Tell Libgcrypt that initialization has completed. */
	gcry_control (GCRYCTL_INITIALIZATION_FINISHED, 0);


	microtime = bench(ic);
	while( abs(desired_time-microtime) > (desired_time/10) /*little difference */ 
			&& tries++ <= 5) {
		float ratio = (float)desired_time/microtime;
		if(ratio > 1000) ratio=1000.0;
		ic*=ratio;
		if(ic<1) ic=1;
		microtime = bench(ic);
	} 
	printf("%d\n", ic);
	return 0;

}
