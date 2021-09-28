#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char **argv) {
    int number = atoi(argv[1]);
    uid_t uid;
    gid_t gid;

    if (number == 423) {
        setrgid(getegid());
        setruid(geteuid());
        execv("/bin/sh", NULL);
    }
	else {
		fwrite("No !\n", 1, 5, stderr);
    }
    return 0;
}