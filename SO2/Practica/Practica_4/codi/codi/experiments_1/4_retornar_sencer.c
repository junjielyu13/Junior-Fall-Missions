#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *thr_fn(void *arg){
    long int valor = 1;
    printf("fil 1 retorna 1\n");
    return ((void *)valor);
}

int main(void){
    int err;
    pthread_t tid1;
    void *tret;

    err = pthread_create(&tid1, NULL, thr_fn, NULL);
    if(err != 0){
        printf("no puc crear fil 1.\n");
        exit(1);
    }

    err = pthread_join(tid1, &tret);
    if(err != 0){
        printf("error pthread_join al fil 1.\n");
        exit(1);
    }

    printf("codi de sortida del fil 1: %ld\n", (long int)tret);

    return 0;
}
