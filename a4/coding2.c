#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char  magic_number_1[] = {0xBA, 0x5E, 0xBA, 0x11, 0x00};
char  magic_number_2[] = {0xBA, 0x5E, 0xBA, 0x12, 0x00};



/*
 * The encode() function may remain unchanged for A#4.
 */

int encode(FILE *input, FILE *output) {
    return 0;
}


int decode(FILE *input, FILE *output) {
    
    // Check magicnum
    char read_magicnum[5];
    for (int i=0;i<5;i++) {
    	read_magicnum[i] = fgetc( FILE *input );
    }

    // If magicnum not found, print an error
    if (strcmp(read_magicnum, magic_number_1) != 0 
    	&& strcmp(read_magicnum, magic_number_2) != 0) {
    	fprintf(stderr, "Error: magic number not found!");
    	exit(1);
    }

    // read

    // Decoder loop
    // While there's more to be read:

    	// nextbyte = read byte

    	// deal with newline

    	// Case 2

    		// New word

    		// Not a new word

    	// Case 3

    		// New word

    		// Not a new word

    	// Case 1

    		// New word

    		// not a new word

	return 0;

}
