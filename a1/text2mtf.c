

int main(int argc, char **argv) {
	char filename[] = *argv[0];
	FILE *textfile = fopen(filename, "r");
	FILE *out_file = fopen("vapenation", "rw");

	fclose (textfile);
	fclose (out_file);
}

char[] readLine(FILE *file) {
	char line[256];
	fscanf(fptr, "%[^\n]", line);
	return line;
	/*
	while (fgets(line, sizeof(line), file)) {
		// fug
	}
	*/
}

something tokenizeLine(somethingelse thestring) {
	char* token = strtok(thestring, " ")
	// jeep jeep
	return 
}