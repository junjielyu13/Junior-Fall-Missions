#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

sem_t buit, ocupat;
int buffer;
int numIters;

void *productor(void *arg){
    int i;
    for ( i = 1; i <= numIters; i++){
        sem_wait(&buit);
        printf("Productor produeix la data %d\n", i);
        buffer = i;
        sem_post(&ocupat);
    }
    return ((void*)0);
}

void *consumidor(void *arg){
    int i, total = 0;
    for ( i = 1; i <= numIters; i++){
        sem_wait(&ocupat);
        printf("Consumidor agafa la dada %d\n", buffer);
        total = total + buffer;
        sem_post(&buit);
    }
    printf("El total es %d\n", total);
    return ((void*)0);
}

int main(int argc, char **argv){
    pthread_t prod, cons;
    if (argc != 2){
        printf("Us: %s <numIters>\n", argv[0]);
        exit(1);
    }

    sem_init(&buit, 0, 1);
    sem_init(&ocupat, 0, 1);

    numIters = atoi(argv[1]);
    pthread_create(&prod, NULL, productor, NULL);
    pthread_create(&cons, NULL, consumidor, NULL); 
    pthread_join(prod, NULL);
    pthread_join(cons, NULL);
}