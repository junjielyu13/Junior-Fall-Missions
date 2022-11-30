#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

pthread_t ntid[10];

struct parametres{
    int i;
    int j;
    char str[10];
};

void *thr_fn(void *arg){
    struct parametres *par = (struct parametres *)arg;
    printf("El fil amb sencer %d te assignat la j = %d i str = %s\n", par->i, par->j, par->str);
    return NULL;    
}


int main(void){
    int i;
    void *tret;
    struct parametres par[10];

    for (i = 0; i < 10; i++){
        par[i].i = i;
        par[i].j = 10 - i;
        sprintf(par[i].str, "Hola %d", i);
        pthread_create(ntid+i, NULL, thr_fn, (void *) &par[i]);
    }

    for(i = 0; i < 10; i++){
        pthread_join(ntid[i], &tret);
    }

    return 0;
}