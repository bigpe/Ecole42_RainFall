#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void p(void) {
	unsigned int	check;
	char			input[76];

    fflush(stdout);
    gets(input);
    if ((check & 0xb0000000) == 0xb0000000) {
        printf("(%p)\n", check);
        exit(1);
    }
    puts(input);
    strdup(input);
    return;
}

int main(void) {
	p();
	return 0;
}