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
typedef struct Word Word;
struct Word {
	char *word;
	Word *next;

};

Word *prepend(Word *wordlist, Word *new_word);
Word *removeWord(Word *wordlist, char *word);
Word *fetchAtIndex(Word *wordlist, int index);
Word *newWord(char *word);


Word *newWord(char *word) {
	Word *newp;

	newp = (Word *) malloc(sizeof(Word));
	if (newp == NULL) {
		fprintf(stderr, "malloc of %u bytes failed", sizeof(Word));
		exit(1);
	}
	newp->word = word;
	newp->next = NULL;
}

Word *prepend(Word *wordlist, Word *new_word) {
	new_word -> next = wordlist;
	return new_word;
}

Word *removeWord(Word *wordlist, char *word) {
	// Copied from the slides lmao
	Word *curr, *prev;

	prev = NULL;
	for (curr = wordlist; curr != NULL; curr = curr -> next) {
		// Iterate thru and look for word
		if (strcmp(word, curr -> word) == 0) {
			if (prev == NULL) {
				// First thing in list is to be removed
 				wordlist = curr -> next;
			} else {
				prev -> next = curr -> next;
			}
			free(curr);
			return wordlist;
		}
		prev = curr;
	}
	fprintf(stderr, "removeWord: %s not found", word);
	exit(1);
}


Word *fetchAtIndex(Word *wordlist, int index) {
	Word *curr = wordlist;
	// printf("first word: %s", curr->word);
	// printf("searching for index %d \n", index);
	int count = 0;
	while (curr != NULL) {
		// printf("%s ", curr->word);
		if (count == index - 1) {
			return(curr);
		}
		count++;
		curr = curr->next;
	}
	fprintf(stderr, "fuckup supreme");
	exit(1);

}

void printAtIndex(Word *wordlist, int index) {
	Word *curr = wordlist;
	int count = 0;
	while (curr != NULL) {
		if (count == index) {
			printf("found");
			printf("%s \n", curr -> word);
			return;
		}
		count++;
		curr = curr -> next;
	}
	printf("found: %s\n", curr -> word);

}

void *printAllWords(Word *wordlist) {
	Word *curr = wordlist;
  	while (curr != NULL) {
  		printf("%s ", curr -> word); 
  		curr = curr -> next;
  	}
}


int decode(FILE *input, FILE *output) {
    
    // Check magicnum
    char read_magicnum[5]; // It's gotta be 5 for the end char
    for (int i=0;i<4;i++) {
    	char c = fgetc(input);
    	read_magicnum[i] = c;
    	//fprintf(stderr, c);
    	//fputc(c, stderr);
    }
    read_magicnum[4] = '\0';
    
    fputc('\n', stderr);
    
    // Check magicnum
    
    if (strcmp(read_magicnum, magic_number_1) != 0 
    	&& strcmp(read_magicnum, magic_number_2) != 0) {
    		fprintf(stderr, "Error: magic number not found!");
    		exit(1);
    }
    
    unsigned int c;
    int wordlistcount = 0;
    Word *wordlist = NULL; // holy frig didn't explicitly set this to null and it 
    					   // totally destroyed my linkedlist functions

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
    		c = fgetc(input);
    	}

		// Case 2
		
    	else if (c == 249) {
    		//printf ("Case 2 \n");
    		// extra byte of encoding
    		c = fgetc( input ); // Get code byte
    		if (ferror(input)) {
    			printf("read error!\n" );
    		}

    		//printf("word uhh thing %d \n", c);
    		//printf("wordlistcount %d \n", wordlistcount);

    		if (c + 121 > wordlistcount) {

    			c = fgetc(input); // get first char of word
    			int count = 0;

    			char *word; // Allocate memory for word
    			word = (char *) malloc( sizeof(char) );
    			if (word == NULL) {
    				fprintf(stderr, "Malloc error! ");
    				abort();
    			}

    			while (c < 129 && c != '\n' && !feof(input) ) {
    				word[count] = c;
    				char *newpointer = realloc(word, sizeof(char) * (count + 2));
    				// +1 because count starts at 0 and +1 for end char
    				// realloc every char probably not very efficient but it is easy
    				if (newpointer == NULL) {
    					fprintf(stderr, "realloc error! ");
    					exit(1);
    				}
    				word = newpointer;
    				count++;
    				c = fgetc(input);
    				// !! this ends on a symbol byte! !!
    			}

    			// End the string so we don't print gobbledygook
    			word[count] = '\0';

    			Word *new = newWord(word);
    			wordlist = prepend(wordlist, new);
    			//printf("New word: %s \n", new->word);
    			fputs(new->word, output);
    			if (c != '\n' && c != EOF) { // Add spaces only between words
					fputc(' ', output);
				}

    			wordlistcount++; 
    		} else {

    			int n = (c + 121);
    			//printf("fetch %d \n", n);
    			char *oldword = fetchAtIndex(wordlist, n)->word;
    			//printf("Old word: %s \n", oldword); // debug
    			
    			// MTF stuff
    			Word *mtf = newWord(oldword);
    			wordlist = removeWord(wordlist, oldword);
    			wordlist = prepend(wordlist, mtf);

    			fputs(oldword, output);
    			
    			c = fgetc(input);
				if (c != '\n' && c != EOF) {
					fputc(' ', output);
				}
    		}
    	}
    	
    	// Case 3
    	else if (c == 250) {
    		// printf ("Case 3 \n");
    		// 3 bytes of encoding
    		// Get encoding bytes and do the math
    		int n = (fgetc(input) * 256) + 376;
    		n += (fgetc(input));

    		
    		if (n > wordlistcount) {
    			// new word
    			c = fgetc(input); // get first char of word
    			int count = 0;

    			char *word; // Allocate memory for word
    			word = (char *) malloc( sizeof(char) );
    			if (word == NULL) {
    				fprintf(stderr, "Malloc error! ");
    				abort();
    			}

    			while (c < 129 && c != '\n' && !feof(input) ) {
    				word[count] = c;
    				char *newpointer = realloc(word, sizeof(char) * (count + 2));
    				// +1 because count starts at 0 and +1 for end char
    				// realloc every char probably not very efficient but it is easy
    				if (newpointer == NULL) {
    					fprintf(stderr, "realloc error! ");
    					exit(1);
    				}
    				word = newpointer;
    				count++;
    				c = fgetc(input);
    				// !! this ends on a symbol byte! !!
    			}

    			// End the string so we don't print gobbledygook
    			word[count] = '\0';

    			Word *new = newWord(word);
    			wordlist = prepend(wordlist, new);
    			// printf("New word: %s \n", new->word);
    			fputs(new->word, output);
    			if (c != '\n' && c != EOF) { // Add spaces only between words
					fputc(' ', output);
				}

    			wordlistcount++;

    		} else {
    			// Old word

    			char *oldword = fetchAtIndex(wordlist, n)->word; 
    			// printf("Old word: %s \n", oldword); // debug
    			
    			// MTF stuff
    			Word *mtf = newWord(oldword);
    			wordlist = removeWord(wordlist, oldword);
    			wordlist = prepend(wordlist, mtf);

    			fputs(oldword, output);
    			
    			c = fgetc(input);
				if (c != '\n' && c != EOF) {
					fputc(' ', output);
				}
    		}
    	}

    	// Case 1
    	else {
    		// new word
    		if (c - 128 > wordlistcount) {

    			c = fgetc(input); // get first char of word
    			int count = 0;

    			char *word; // Allocate memory for word
    			word = (char *) malloc( sizeof(char) );
    			if (word == NULL) {
    				fprintf(stderr, "Malloc error! ");
    				abort();
    			}

    			while (c < 129 && c != '\n' && !feof(input) ) {
    				word[count] = c;
    				char *newpointer = realloc(word, sizeof(char) * (count + 2));
    				// +1 because count starts at 0 and +1 for end char
    				// realloc every char probably not very efficient but it is easy
    				if (newpointer == NULL) {
    					fprintf(stderr, "realloc error! ");
    					exit(1);
    				}
    				word = newpointer;
    				count++;
    				c = fgetc(input);
    				// !! this ends on a symbol byte! !!
    			}

    			// End the string so we don't print gobbledygook
    			word[count] = '\0';

    			Word *new = newWord(word);
    			wordlist = prepend(wordlist, new);
    			//printf("New word: %s \n", new->word);
    			fputs(new->word, output);
    			if (c != '\n' && c != EOF) { // Add spaces only between words
					fputc(' ', output);
				}

    			wordlistcount++;
			
    		} else {

    			int n = (c-128);
    			char *oldword = fetchAtIndex(wordlist, n)->word;
    			//printf("Old word: %s \n", oldword); // debug
    			
    			// MTF stuff
    			Word *mtf = newWord(oldword);
    			wordlist = removeWord(wordlist, oldword);
    			wordlist = prepend(wordlist, mtf);

    			fputs(oldword, output);
    			
    			c = fgetc(input);
				if (c != '\n' && c != EOF) {
					fputc(' ', output);
				}

    		}

    	}

    }

    // printAtIndex(wordlist, 15);
    // printf("\n");
    // printAllWords(wordlist);
	return 0;

}
