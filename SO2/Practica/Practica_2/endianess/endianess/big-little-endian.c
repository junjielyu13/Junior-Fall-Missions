#include <stdio.h>

int main() {
  int a = 0x0A0B0C0D;
  unsigned char *c = (unsigned char *)(&a);

  if (*c == 0x0D)
    printf("little-endian\n");
  else
    printf("big-endian\n");

  return 0;
}
