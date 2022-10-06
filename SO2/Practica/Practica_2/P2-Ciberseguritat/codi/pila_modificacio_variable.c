#include <stdio.h>

void funcio()
{
  int a[1000];
  int b;

  b = 5;

  printf("Direccio de b: %p\n", &b);
  printf("Valor de b: %d\n", b);

  printf("Direccio de a[1]: %p\n", &a[1]);
  printf("Direccio de a[0]: %p\n", &a[0]);
  printf("Direccio de a[-1]: %p\n", &a[-1]);

  printf("Modifico el valor: a[-1] = 10\n");
  a[-1] = 10;

  printf("Valor de b: %d\n", b);
}

int main(void)
{
  funcio();
}
