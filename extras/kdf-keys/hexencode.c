/*
 * A simple utility that reads from stdin and output the hexencoding (on a single line) of the input
 */

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

static int decode_mode = 0;
int main(int argc, char *argv[]) {
	char c;
	char buf[3];
	int read_bytes;
	int opt;
	static struct option long_options[] =
	{
		{"decode", no_argument, &decode_mode, 1},
		{"encode", no_argument, &decode_mode, 0},
		{0,0,0,0}
	};
	int option_index = 0;

	while(1) {
		option_index = 0;
		opt = getopt_long(argc, argv, "", long_options, &option_index);
		if(opt == -1)
			break;
		switch(opt) {
			case 0:
				break;
			case '?':
				return 127;
			default:
				abort();
		}
	}
	if(decode_mode == 0) {
		while(( c = (char)getchar() ) != EOF)
			printf("%02x", c);
		return 0;
	} else {
		while( (read_bytes=fread(buf, sizeof(char), 2, stdin)) != 0) {
			if(read_bytes == 1) buf[1]='\0';
			sscanf(buf, "%x", &c);
			printf("%c", c);
		}
		return 0;
	}
}
