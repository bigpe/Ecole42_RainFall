#include <stdio.h>
#include <stdlib.h>

void run(void)
{
  fwrite("Good... Wait what?\n", 1, 19, stdout);
  system("/bin/sh");
  return;
}

int main(void)
{
  char input[76];

  gets(input);
  return 0;
}