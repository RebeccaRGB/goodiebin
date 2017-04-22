#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

int help() {
	printf("erdrcr - ErroR DetectoR and CorrectoR for binary files\n");
	printf("usage: erdrcr [<paths>] [-o <path>]\n");
	printf("   -i <path>   specify binary files to compare\n");
	printf("   -o <path>   specify file to write corrected data to\n");
	return 0;
}

int erdrcr(int inputc, char ** input, char * output) {
	/* Allocate Memory */
	FILE ** finput;
	FILE * foutput = (FILE *)0;
	char * bytes;
	int i, eof, mask, zeroes, ones;
	char * correction;
	long long addr = 0;
	long long errs = 0;
	long long fatal = 0;
	double percent;
	finput = (FILE **)malloc(sizeof(FILE *) * inputc);
	if (!finput) return 2;
	bytes = (char *)malloc(sizeof(char) * inputc);
	if (!bytes) return 2;
	
	/* Open Files */
	for (i = 0; i < inputc; i++) {
		finput[i] = fopen(input[i], "r");
		if (!finput[i]) return 2;
	}
	if (output) {
		foutput = fopen(output, "w");
		if (!foutput) return 2;
	}
	
	/* Compare */
	for (;;) {
		eof = 0;
		for (i = 0; i < inputc; i++) {
			if (!fread(&bytes[i], sizeof(char), 1, finput[i])) {
				bytes[i] = 0;
				eof++;
			}
		}
		if (eof == inputc) break;
		for (mask = 0x80; mask; mask >>= 1) {
			zeroes = 0;
			ones = 0;
			for (i = 0; i < inputc; i++) {
				if (bytes[i] & mask) ones++;
				else zeroes++;
			}
			if (zeroes && ones) {
				if (zeroes > ones) {
					correction = "0";
					bytes[0] &=~ mask;
				} else if (ones > zeroes) {
					correction = "1";
					bytes[0] |= mask;
				} else {
					correction = "?";
					fatal++;
				}
				if (!errs) printf("Address.Mask\t0's\t1's\tCorrection\n");
				printf("%08llX.%02X:\t%d\t%d\t%s\n", addr, mask, zeroes, ones, correction);
				errs++;
			}
		}
		if (output) fwrite(bytes, sizeof(char), 1, foutput);
		addr++;
	}
	
	/* Close Files */
	for (i = 0; i < inputc; i++) fclose(finput[i]);
	if (output) fclose(foutput);
	
	/* Deallocate Memory */
	free(finput);
	free(bytes);
	
	/* Report */
	if (errs) {
		addr <<= 3;
		percent = 100.0 * errs / addr;
		printf("%lld out of %lld bits mismatched (%g%% error rate)\n", errs, addr, percent);
		if (fatal) {
			percent = 100.0 * fatal / addr;
			printf("%lld out of %lld bits unrecoverable (%g%% error rate)\n", fatal, addr, percent);
		} else {
			printf("all errors correctable\n");
		}
		return 1;
	} else {
		printf("no differences found\n");
		return 0;
	}
}

int main(int argc, char ** argv) {
	int inputc = 0;
	char ** input;
	char * output = (char *)0;
	int i = 1;
	char * arg;
	int ret;
	input = (char **)malloc(sizeof(char *) * argc);
	if (!input) return 2;
	
	while (i < argc) {
		arg = argv[i++];
		if (!strcmp(arg, "--help")) {
			ret = help();
			free(input);
			return ret;
		} else if (i < argc && !strcmp(arg, "-i")) {
			input[inputc++] = argv[i++];
		} else if (i < argc && !strcmp(arg, "-o")) {
			output = argv[i++];
		} else {
			input[inputc++] = arg;
		}
	}
	ret = inputc ? erdrcr(inputc, input, output) : help();
	free(input);
	return ret;
}
