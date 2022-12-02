#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define N 100

int comptador;
pthread_t ntid[N];
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t  cond  = PTHREAD_COND_INITIALIZER;

void barrera(){
    pthread_mutex_lock(&mutex);

    comptador = comptador - 1;
    if(comptador == 0){
        comptador = N;
        pthread_cond_broadcast(&cond);
    }else{
        pthread_cond_wait(&cond, &mutex);
    }

    pthread_mutex_unlock(&mutex);
}

void *thr_fn(void *arg){
    int i, j;
    j = 0;
    for (i = 0; i < 10; i++){
        j++;
        barrera();
        printf("%d ", j);
    }

    return ((void *)0);
}


int main(void){
    int i, err;
    for ( i = 0; i < N; i++){
        err = pthread_create(ntid+i, NULL, thr_fn, NULL);
        if (err != 0){
            printf("no puc crear el fil numero %d.", i);
            exit(1);
        }
    }

    for ( i = 0; i < N; i++){
        err = pthread_join(ntid[i], NULL);
        if(err != 0){
            printf("error pthread_join al fil %d.", i);
            exit(1);
        }
    }
}