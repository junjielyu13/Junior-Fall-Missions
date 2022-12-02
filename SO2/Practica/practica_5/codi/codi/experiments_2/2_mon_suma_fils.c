#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>

#define MAXFILS 500
#define NITERS  1000

pthread_t ntid[MAXFILS];
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int a;

void *thr_fn(void *arg){
    pthread_mutex_lock(&mutex);
    a++;
    pthread_mutex_unlock(&mutex);
    return ((void *)0);
}

int main(void){
    
    int i, j;
    int err;
    
    for ( j = 0; i < NITERS; j++){
        a = 0;

        for (i = 0; i < MAXFILS; i++){
            err = pthread_create(ntid+i, NULL, thr_fn, NULL);
            if (err != 0){
                printf("no puc crear el fil numero %d\n", i);
                exit(1);
            }
        }

        for (i = 0; i < MAXFILS; i++){
            err = pthread_join(ntid[i], NULL);
            if (err != 0){
                printf("error pthread_join al fil %d\n", i);
                exit(1);
            }
        }

        if(a != MAXFILS){
            printf("fil principal: iteracio j = %d, a = %d\n", j, a);
        }
        
    }
    
}
