#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

int help() {
	printf("erdrcr - ErroR DetectoR and CorrectoR for binary files\n");
	printf("usage: erdrcr [<options>] [<paths>] [-o <path>]\n");
	printf("   -q          don't print every mismatch; only print summary\n");
	printf("   -e          print extended summary\n");
	printf("   -i <path>   specify binary files to compare\n");
	printf("   -o <path>   specify file to write corrected data to\n");
	return 0;
}

int err(const char * s) {
	perror(s ? s : "erdrcr");
	return 2;
}

int erdrcr(int quiet, int extended, int inputc, char ** input, char * output) {
	/* Allocate Memory */
	FILE ** finput;
	FILE * foutput = (FILE *)0;
	char * bytes;
	int i, eof;
	int di, mask;
	int zeroes, ones;
	char * correction;
	long long amask;
	long long addr = 0;
	long long errs = 0;
	long long fatal = 0;
	double percent;
	long long * histogram;
	long long onAddrLow[64];
	long long onAddrHigh[64];
	long long onData[8];
	
	finput = (FILE **)malloc(sizeof(FILE *) * inputc);
	if (!finput) return err((const char *)0);
	bytes = (char *)malloc(sizeof(char) * inputc);
	if (!bytes) return err((const char *)0);
	histogram = (long long *)malloc(sizeof(long long) * inputc);
	if (!histogram) return err((const char *)0);
	
	/* Initialize Memory */
	for (i = 0; i < inputc; i++) {
		finput[i] = fopen(input[i], "r");
		if (!finput[i]) return err(input[i]);
	}
	if (output) {
		foutput = fopen(output, "w");
		if (!foutput) return err(output);
	}
	
	for (i = 0; i < inputc; i++) histogram[i] = 0;
	for (i = 0; i < 64; i++) onAddrLow[i] = 0;
	for (i = 0; i < 64; i++) onAddrHigh[i] = 0;
	for (i = 0; i < 8; i++) onData[i] = 0;
	
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
		for (di = 7, mask = 0x80; mask; mask >>= 1, di--) {
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
				
				histogram[zeroes]++;
				for (i = 0, amask = 1; (i < 64) && amask; i++, amask <<= 1) {
					if (addr & amask) onAddrHigh[i]++;
					else onAddrLow[i]++;
				}
				onData[di]++;
				
				if (!quiet) {
					if (!errs) printf("Address.Mask\t0's\t1's\tCorrection\n");
					printf("%08llX.%02X:\t%d\t%d\t%s\n", addr, mask, zeroes, ones, correction);
				}
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
		if (extended) {
			printf("\nerror distribution:\n0's\t1's\tErrors\n");
			for (i = 1; i < inputc; i++) printf("%d\t%d\t%lld\n", i, inputc - i, histogram[i]);
			printf("\nerrors on address lines:\nA\tLow\tHigh\tDelta\n");
			for (i = 0, amask = 1, addr >>= 3; (i < 64) && amask && amask < addr; i++, amask <<= 1) {
				printf(
					"A%d\t%lld\t%lld\t%c%lld\n", i, onAddrLow[i], onAddrHigh[i],
					((onAddrLow[i] > onAddrHigh[i]) ? 'L' : (onAddrHigh[i] > onAddrLow[i]) ? 'H' : ' '),
					((onAddrLow[i] > onAddrHigh[i]) ? (onAddrLow[i] - onAddrHigh[i]) : (onAddrHigh[i] - onAddrLow[i]))
				);
			}
			printf("\nerrors on data lines:\nQ\tErrors\n");
			for (i = 0; i < 8; i++) printf("Q%d\t%lld\n", i, onData[i]);
		}
		free(histogram);
		return 1;
	} else {
		printf("no differences found\n");
		free(histogram);
		return 0;
	}
}

int main(int argc, char ** argv) {
	int quiet = 0;
	int extended = 0;
	int inputc = 0;
	char ** input;
	char * output = (char *)0;
	int i = 1;
	char * arg;
	int ret;
	
	input = (char **)malloc(sizeof(char *) * argc);
	if (!input) err((const char *)0);
	
	while (i < argc) {
		arg = argv[i++];
		if (!strcmp(arg, "--help")) {
			ret = help();
			free(input);
			return ret;
		} else if (!strcmp(arg, "-q")) {
			quiet = 1;
		} else if (!strcmp(arg, "-e")) {
			extended = 1;
		} else if (i < argc && !strcmp(arg, "-i")) {
			input[inputc++] = argv[i++];
		} else if (i < argc && !strcmp(arg, "-o")) {
			output = argv[i++];
		} else {
			input[inputc++] = arg;
		}
	}
	ret = inputc ? erdrcr(quiet, extended, inputc, input, output) : help();
	free(input);
	return ret;
}
