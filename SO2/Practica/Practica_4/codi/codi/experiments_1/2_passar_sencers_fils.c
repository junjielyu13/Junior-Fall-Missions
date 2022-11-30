#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

pthread_t ntid[10];

void *thr_fn(void *arg){
    long int i = (long int) arg;
    printf("El fil amb ID %ld te assignat el sencer %ld\n", pthread_self(), i);
    return ((void *)i);
}


int main(void){

    long int i;
    int err;
    void *tret;

    for(i = 0; i < 10; i++){
        err = pthread_create(ntid+i, NULL, thr_fn, (void *) i);
        if( err != 0 ){
            printf("no puc crear el fill.\n");
            exit(1);
        }
    }

    for(i = 0; i < 10; i++){
        err = pthread_join(ntid[i], &tret);
        if( err != 0 ){
            printf("error pthread_join al fil %ld\n", i);
            exit(1);
        }
        printf("El fil %ld m'ha retornat el numero %ld\n", i, (long int) tret);
    }

    return 0;

}