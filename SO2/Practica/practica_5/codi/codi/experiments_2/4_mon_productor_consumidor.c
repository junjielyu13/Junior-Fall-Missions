#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

pthread_mutex_t mutex;
pthread_cond_t cua_cons, cua_prod;
int buffer;
int buit;
int numIters;

void *productor(void *arg){
    int i;
    for ( i = 1; i <= numIters; i++){
        pthread_mutex_lock(&mutex);
        if (!buit){
            pthread_cond_wait(&cua_prod, &mutex);
        }
        printf("Productor produeix la data %d\n", i);
        buffer = i;
        buit = 0;
        pthread_cond_signal(&cua_cons);
        pthread_mutex_unlock(&mutex);    
    }
    return ((void *)0);
}


void *consumidor(void *arg){
    int i, total = 0;
    for ( i = 1; i <= numIters; i++){
        pthread_mutex_lock(&mutex);
        if (buit){
            pthread_cond_wait(&cua_cons, &mutex);
        }
        printf("Consumidor agafa la dada %d\n", buffer);
        total = total + buffer;
        buit = 1;
        pthread_cond_signal(&cua_prod);
        pthread_mutex_unlock(&mutex);
    }
    printf("El total es %d\n", total);
    return ((void *) 0);
}

int main(int argc, char **argv){
    pthread_t prod, cons;
    if (argc != 2) {
        printf("Us: %s <numIters>\n", argv[0]);
        exit(1);
    }
    buit = 1;
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cua_cons, NULL);
    pthread_cond_init(&cua_prod, NULL);

    numIters = atoi(argv[1]);
    pthread_create(&prod, NULL, productor, NULL);
    pthread_create(&cons, NULL, consumidor, NULL);
    pthread_join(prod, NULL);
    pthread_join(cons, NULL);
}