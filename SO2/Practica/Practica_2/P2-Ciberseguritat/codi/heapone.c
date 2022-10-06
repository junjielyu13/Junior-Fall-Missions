/*
 * phoenix/heap-zero, by https://exploit.education
 *
 * Can you hijack flow control?
 *
 * Which vegetable did Noah leave off the Ark?
 * Leeks
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define LEVELNAME "phoenix/heapone"

#define BANNER \
    "Welcome to " LEVELNAME ", brought to you by https://exploit.education"

struct heapStructure {
    int priority;
    char *name;
};

void winner() {
    printf("Congratulations, you've completed this level!!!\n");
    exit(0);
}

void start_level(char *argv1, char *argv2)
{
    struct heapStructure *i1, *i2;
    unsigned long int value;
    void *pointer;
    int k;

    for (k = 0; k < 10; k += 1) {
        pointer = (void *) (&i1 + k);
        value = *((unsigned long int *) pointer);
        printf("A la direccio de la pila %p emmagatzema el valor: %p\n", (void *) pointer, (void *) value);
    }

    i1 = malloc(sizeof(struct heapStructure));
    i1->priority = 1;
    i1->name = malloc(8);

    i2 = malloc(sizeof(struct heapStructure));
    i2->priority = 2;
    i2->name = malloc(8);

    pointer = __builtin_return_address(0);
    printf("Original return address: %p\n", pointer);

    strcpy(i1->name, argv1);
    
    pointer = (void *) i2->name;
    printf("A i2->name s'emmagatzema el valor %p\n", pointer);
    
    strcpy(i2->name, argv2);

    pointer = __builtin_return_address(0);
    printf("New return address: %p\n", pointer);

    printf("and that's a wrap folks!\n");
}


int main(int argc, char **argv) {
    printf("%s\n", BANNER);
    if (argc == 3)
        start_level(argv[1], argv[2]);
    else
        printf("Need two arguments\n");
}
