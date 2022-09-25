#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <ctype.h>
#include <sys/mman.h>
#include <sys/stat.h>

#define FILE "file.txt"

int main(int argc, char **argv)
{
  struct stat st;

  int i, fd, len;
  int vowels, consonants, digits, spaces, puncts;
  char c, *file_memory;

  stat(FILE, &st);
  len = st.st_size;

  fd = open(FILE, O_RDWR, S_IRUSR | S_IWUSR);
  if (fd == -1) {
      printf("Could not open file '%s'\n", FILE);
      exit(1);
  }

  file_memory = mmap(0, len, PROT_READ | PROT_WRITE, 
      MAP_SHARED, fd, 0);

  close(fd);

  vowels = 0;
  consonants = 0;
  digits = 0;
  spaces = 0;
  puncts = 0;

  for(i = 0; i < len; i++) {
    c = file_memory[i];

    if (isalpha(c)) {
      c = tolower(c);

      if ((c == 'a') || (c == 'e') || (c == 'i') || (c == 'o') || (c == 'u'))
        vowels++;
      else
        consonants++;
    } 
    else if (isdigit(c))
      digits++;
    else if (ispunct(c))
      puncts++;
    else if (isspace(c))
      spaces++;
  }

  printf("Summary:\n");
  printf(" Vowels: %d\n", vowels);
  printf(" Consonants: %d\n", consonants);
  printf(" Digits: %d\n", digits);
  printf(" Space chars: %d\n", spaces);
  printf(" Puntuacion chars: %d\n", puncts);

  munmap(file_memory, len);
}
