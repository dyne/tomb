/*
 * Small program which simply opens a file in a tomb to block the
 *  $ tomb close
 * operation
 *
 * Hard coded assumption on command line arguments
 * 2) Path to open
 * 3) How long to open the file (in seconds and can be optional)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main(int argc, char const *argv[]) {
    FILE *file_ptr;
    unsigned int to_wait=10;

    if ( argc < 2 ) {
        fprintf(stderr, "Usage: %s path [time]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if ( argc == 3 ) {
        to_wait = atoi(argv[2]);
    }

    file_ptr = fopen(argv[1],"w");

    if ( file_ptr == NULL ) {
        fprintf(stderr, "Error while opening the file.\n");
        exit(EXIT_FAILURE);
    }

    sleep(to_wait);

    fclose(file_ptr);

    return 0;
}
