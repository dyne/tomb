#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_hex(unsigned char *buf, int len)
{
  int i;

  for(i=0;i<len;i++){
    printf("%02x", buf[i]);
  }
}

int main(int argc, char **argv) {
	int len=32;
	int res;
	unsigned char *buf;
	FILE *rand;
	if(argc>=2) {
		if(sscanf(argv[1], "%d", &len) != 1) {
			fprintf(stderr, "Error: len must be an integer\n");
			return 1;
		}
	}
	buf = calloc(len, sizeof(char));
	memset(buf, 9, len);
	rand = fopen("/dev/random", "r");
	res = fread(buf, sizeof(char), len, rand);
	if( res != len) {
		fprintf(stderr, "Error reading /dev/random: %d != %d, \n", res, len);
		fclose(rand);
		free(buf);
		return 2;
	}
	fclose(rand);
	print_hex(buf, len);
	free(buf);
	return 0;
}
