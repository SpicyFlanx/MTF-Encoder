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

// Wordlist struct here


int decode(FILE *input, FILE *output) {
    
    // Check magicnum
    char read_magicnum[5]; // It's gotta be 5 for the end char
    for (int i=0;i<4;i++) {
    	char c = fgetc(input);
    	read_magicnum[i] = c;
    	//fprintf(stderr, c);
    	//fputc(c, stderr);
    }
    
    fputc('\n', stderr);
    
    // Check magicnum
    if (strcmp(read_magicnum, magic_number_1) != 0 
    	&& strcmp(read_magicnum, magic_number_2) != 0) {
    		fprintf(stderr, "Error: magic number not found!");
    		exit(1);
    }
    
    int c;
    int wordlistcount = 0;
    // need linkdlist for words

    // read

    // Decoder loop
    // While there's more to be read:
    c = fgetc(input);
    while (!feof(input)) {

    	/*
    	fputc(c, stderr);
    	printf ("%d", c);
		*/

    	if ( feof(input) ) {
    		// Stop at EOF
    		fprintf(stderr, "eof");
    		break;
    	}


    	// deal with newline
    	if (c == '\n') {
    		fputc( c , output );
    	}

		// Case 2
    	else if (c == 249) {
    		printf ("Case 2 \n");
    	}
    	
    	// Case 3
    	else if (c == 250) {
    		printf ("Case 3 \n");
    	}

    	else {
    		printf ("Case 1 \n");

    		printf("Wordlist length: %d symbol thingy: %d  %c \n", wordlistcount, c-128, c);
    		
    		// new word
    		if (c - 128 > wordlistcount) { // TODO: determine if c - 128 > # words on list
    			printf("New word: ");

    			c = fgetc(input); // First char of word

    			// Allocate memory for word
    			// Make it have space for 20 chars cause why not
    			char* word = (char*) malloc( sizeof(char)*20 );
    			if (!word) {
    				fprintf(stderr, "Malloc error! ");
    				abort();
    			}

    			int count = 0;
    			while (c < 129 && c != '\n' && !feof(input) ) {
    				// printf("aaaa");
    				fprintf(stderr, "%c", c);
    				// Read until another symbol char, or newline, or EOF
    				// add each char to word
    				// realloc if more space needed
    				// word[count] = c;
    				c = fgetc(input);
    			}
    			free(word);

    			// write word to file
    			// write a space between words
    			// prepend / append word to list
    			printf("\n");
    			//printf("%d", c);
    			wordlistcount++;
			
    		} else {
    			printf("Old word, number %d \n", c-128);
    			c = fgetc(input);

    			// Not a new word
    			// resolve symbol into wordlist index

    			// do MTF stuff
    				// Delete word from LL
    				// Put word at front of LL

    			// Write out the word
    			// Add a space between words
			
    		}

    	}

    }

	return 0;

}
