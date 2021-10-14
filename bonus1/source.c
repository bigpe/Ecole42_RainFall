int main(int ac,char **av) {
  int		ret;
  char		buffer[40];
  int 		number;

  number = atoi(av[1]);
  if (number <= 9) {
    memcpy(buffer, av[2], number * 4);
    if (number == 0x574f4c46) {
      execl("/bin/sh","sh",0);
    }
    return  0;
  }
  return 1;
}