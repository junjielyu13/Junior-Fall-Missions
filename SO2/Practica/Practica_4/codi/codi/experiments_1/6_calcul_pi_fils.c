#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>

#define NUM_FILS 2
#define NUM_RECTS 100000000

double result[NUM_FILS];

double integral(int id){

    int i;
    double mid, height, width, sum = 0.0;
    double area;

    width = 1.0 / (double) NUM_RECTS;
    for (i = id; i < NUM_RECTS; i += NUM_FILS){
        mid = (i + 0.5) * width;
        height = 4.0 / (1.0 + mid * mid);
        sum += height;
    }

    area = width * sum;
    return area;
}

void *thread_fn(void *arg){

    long int i = (long int) arg;
    result[i] = integral(i);
    return ((void *)0);
}

int main(void){
    struct timeval tv1, tv2;
    clock_t t1, t2;
    pthread_t ntid[NUM_FILS];

    double valor_pi;
    long int i;

    gettimeofday(&tv1, NULL);
    t1 = clock();

    for (i = 0; i < NUM_FILS; i++){   
        pthread_create(&(ntid[i]), NULL, thread_fn, (void *)i);
    }

    for (i = 0; i < NUM_FILS; i++)
    {
        pthread_join(ntid[i], NULL);
    }

    valor_pi = 0.0;
    for (i = 0; i < NUM_FILS; i++){
        valor_pi += result[i];
    }

    gettimeofday(&tv2, NULL);
    t2 = clock();

    printf("Valor de pi: %f\n", valor_pi);
    printf("Temps de CPU: %f seconds\n", 
            (double)(t2 - t1) / (double)CLOCKS_PER_SEC);
    printf("Temps cronologic: %f seconds\n",
            (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 + 
            (double) (tv2.tv_sec - tv1.tv_sec));
    
}