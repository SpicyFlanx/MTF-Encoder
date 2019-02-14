#include <stdlib.h>
#include <stdio.h>

static int LINE_MAX_LENGTH = 80;
static int WORD_MAX_LENGTH = 20;


// prototype encode
int encode (FILE * textfile, FILE *output); 



// refactor this
int main(int argc, char **argv) {
	char *infilename[];
	char outfilename[];
        char line[LINE_MAX_LENGTH];
	EncodedWord *list;

	if (argc < 1) {
		exit(1);
	}

	infilename = argv[0];
	FILE *in_file = fopen(infilename, "r");
	FILE *out_file = fopen("vapenation.mtf", "w");

	out_file = magic_number(out_file);



        while (fgets(line, sizeof(line), file)) {
        	// While there's lines to read:
        	// tokenize up to space
	        token = strtok(line, " ");
                while (token != NULL) {
			
			// keep tokenizing!
                        token = strtok(NULL, " ");
                }
        }

           // while there's more lines to read:
		// read line
		// tokenize line
		// assign numbers to new words
		// place numbers for existing words

	// 80 chars max / line = up to 40 words
	// 20 chars max / word

	fclose (in_file);
	fclose (out_file);
}

FILE * magic_number(FILE * out_file) {
	fputc(0xba);
	fputc(0x5e);
	fputc(0xba);
	fputc(0x11);
	return out_file;
}
	
// We'll do a linked list of these fellers
// On second thought, don't really need this
/*
typedef struct EncodedWord EncodedWord;
struct EncodedWord {
		char *word;
		int value;
		EncodedWord *next;
	}
*/

// Prepend an EncodedWord to linkedlist
char* prepend(char *list, char word) {
	word -> next = list;
	return word; // new list address
}

// Append an EncodedWord to linkedlist
char* postpend(EncodedWord *list, EncodedWord *word) {

}

// Delete a word from the list
char* delete(EncodedWord *list, char word) {

}

EncodedWord *move_to_front(EncodedWord *list, )

// check if a word's in the list and return its position, or -1 if not found
int lookup_word(EncodedWord *list, char word) {

}

int encode (FILE * textfile, FILE * output) {
	EncodedWord* list = NULL; // points to linkedlist of words
	int word_num = 1; // To give code values to words

	// get line
	// tokenize line
	// str -> endcodedword
	
	// Read, tokenize each line
	char line[LINE_MAX_LENGTH];
        while (fgets(line, sizeof(line), file)) {
                token = strtok(line, " ");
                while (token != NULL) {
			
                        token = strtok(NULL, " ");
                }
        }
		



	int wordpos = lookup_word(list, );

	if (wordpos == -1){ 
		// word not in list
		// prepend and give number
		prepend(list, )
		word_num++;
	} else {
		// print wordpos
		// move that word to front

	}

}


// Refactor these
char[] readLine(FILE *file) {
	char line[LINE_MAX_LENGTH];
	while (fgets(line, sizeof(line), file)) {
		token = strtok(line, " ");
		while (token != NULL) {
	    		token = strtok(NULL, " ");
		}	
	}
}

something tokenizeLine(somethingelse thestring) {
	char* token;
	token = strtok(thestring, " "); // Get first token
	// do something with the token
	while (token != NULL) {
		token = strtok(NULL, " ");
	}
	// jeep jeep
	return}
