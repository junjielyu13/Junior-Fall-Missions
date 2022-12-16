#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_VALORS 10
#define NUM_ITERS  20

pthread_mutex_t mutex;
pthread_cond_t cua_cons, cua_prod;
int comptador, w, r;

void *thread_prod(void *arg)
{
  int i, value, *valors;

  valors = (int *) arg;

  srand(time(NULL));

  for(i = 1; i < NUM_ITERS; i++) {
    value = rand();
    pthread_mutex_lock(&mutex);
    if (comptador == NUM_VALORS) {
      printf("Productor esperant al wait...\n");
      pthread_cond_wait(&cua_prod, &mutex);
    }
    printf("Productor: valors[%d] = %d\n", w, value);
    valors[w] = value;
    w = (w + 1) % NUM_VALORS;
    comptador++;
    pthread_cond_signal(&cua_cons);
    pthread_mutex_unlock(&mutex);
  }
  
  return ((void *) 0);
}

void *thread_cons(void *arg)
{
  int i, value, *valors;

  valors = (int *) arg; 

  for(i = 1; i < NUM_ITERS; i++) {
    pthread_mutex_lock(&mutex);
    if (comptador == 0) {
      printf("Consumidor esperant al wait...\n");
      pthread_cond_wait(&cua_cons, &mutex);
    }
    value = valors[r];
    printf("Consumidor: valors[%d] = %d\n", r, value);
    r = (r + 1) % NUM_VALORS;
    comptador--;
    pthread_cond_signal(&cua_prod);
    pthread_mutex_unlock(&mutex);
  }

  return ((void *) 0);
}

int main(int argc, char **argv)
{
  pthread_t prod, cons;
  int valors[NUM_VALORS];

  comptador = 0;

  pthread_mutex_init(&mutex, NULL); 
  pthread_cond_init(&cua_cons, NULL);
  pthread_cond_init(&cua_prod, NULL);

  pthread_create(&prod, NULL, thread_prod, (void *) valors);
  pthread_create(&cons, NULL, thread_cons, (void *) valors);
  pthread_join(prod, NULL);
  pthread_join(cons, NULL);
}
