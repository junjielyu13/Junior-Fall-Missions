#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_FILS_PRODUCTOR 1
#define NUM_FILS_CONSUMIDOR 2
#define B_BUFFER 10
#define N_BLOCK 1000

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t prod = PTHREAD_COND_INITIALIZER;
pthread_cond_t cons = PTHREAD_COND_INITIALIZER;

#define MAXCHAR 500
#define LEN_CODE_AIRPORT 3
#define STR_CODE_AIRPORT (LEN_CODE_AIRPORT + 1) // Incluimos el caracter de final de palabra '\0'
#define NUM_AIRPORTS 303

#define COL_ORIGIN_AIRPORT 17
#define COL_DESTINATION_AIRPORT 18

/**
 * Reserva espacio para una matriz de tamaño nrow x ncol,
 * donde cada elemento de la matriz tiene size bytes
 */

void **malloc_matrix(int nrow, int ncol, size_t size)
{
  int i;

  void **ptr = NULL;

  ptr = (void **)malloc(sizeof(void *) * nrow);
  for (i = 0; i < nrow; i++)
  {
    ptr[i] = NULL;
    ptr[i] = (void *)calloc(1, size * ncol);
  }

  return ptr;
}

/**
 * Libera una matriz de tamaño con nrow filas. Utilizar
 * la funcion malloc_matrix para reservar la memoria
 * asociada.
 */

void free_matrix(void **matrix, int nrow)
{
  int i;

  for (i = 0; i < nrow; i++)
  {
    free(matrix[i]);
  }

  free(matrix);
}

/**
 * Leer el fichero fname que contiene los codigos
 * IATA (3 caracteres) de los aeropuertos a analizar.
 * En total hay NUM_AIRPORTS a leer, un valor prefijado
 * (para simplificar el código). Los codigos de los
 * aeropuertos se alacenan en la matriz airports, una
 * matriz cuya memoria ha sido previamente reservada.
 */

void read_airports(char **airports, char *fname)
{
  int i;
  char line[MAXCHAR];

  FILE *fp;

  /*
   * eow es el caracter de fin de palabra
   */
  char eow = '\0';

  fp = fopen(fname, "r");
  if (!fp)
  {
    printf("ERROR: could not open file '%s'\n", fname);
    exit(1);
  }

  i = 0;
  while (i < NUM_AIRPORTS)
  {
    fgets(line, 100, fp);
    line[3] = eow;

    /* Copiamos los datos al vector */
    strcpy(airports[i], line);

    i++;
  }

  fclose(fp);
}

/**
 * Dada la matriz de con los codigos de los aeropuertos,
 * así como un código de aeropuerto, esta función retorna
 * la fila asociada al aeropuerto.
 */

int get_index_airport(char *code, char **airports)
{
  int i;

  for (i = 0; i < NUM_AIRPORTS; i++)
    if (strcmp(code, airports[i]) == 0)
    {
      return i;
    }

  return -1;
}

/**
 * Dada la matriz num_flights, se imprimen por pantalla el
 * numero de destinos diferentes que tiene cada aeropuerto.
 */

void print_num_flights_summary(int **num_flights, char **airports)
{
  int i, j, num;

  for (i = 0; i < NUM_AIRPORTS; i++)
  {
    num = 0;

    for (j = 0; j < NUM_AIRPORTS; j++)
    {
      if (num_flights[i][j] > 0)
        num++;
    }

    printf("Origin: %s -- Number of different destinations: %d\n", airports[i], num);
  }
}

/**
 * Esta funcion se utiliza para extraer informacion del fichero CSV que
 * contiene informacion sobre los vuelos. En particular, dada una linea
 * leida de fichero, la funcion extra el origen y destino de los vuelos.
 */

int extract_fields_airport(char *origin, char *destination, char *line)
{
  /*Recorre la linea por caracteres*/
  char caracter;
  /* i sirve para recorrer la linea
   * iterator es para copiar el substring de la linea a char
   * coma_count es el contador de comas
   */
  int i, iterator, coma_count;
  /* start indica donde empieza el substring a copiar
   * end indica donde termina el substring a copiar
   * len indica la longitud del substring
   */
  int start, end, len;
  /* invalid nos permite saber si todos los campos son correctos
   * 1 hay error, 0 no hay error
   */
  int invalid = 0;
  /* found se utiliza para saber si hemos encontrado los dos campos:
   * origen y destino
   */
  int found = 0;
  /*
   * eow es el caracter de fin de palabra
   */
  char eow = '\0';
  /*
   * contenedor del substring a copiar
   */
  char word[STR_CODE_AIRPORT];
  /*
   * Inicializamos los valores de las variables
   */
  start = 0;
  end = -1;
  i = 0;
  coma_count = 0;
  /*
   * Empezamos a contar comas
   */
  do
  {
    caracter = line[i++];
    if (caracter == ',')
    {
      coma_count++;
      /*
       * Cogemos el valor de end
       */
      end = i;
      /*
       * Si es uno de los campos que queremos procedemos a copiar el substring
       */
      if (coma_count == COL_ORIGIN_AIRPORT || coma_count == COL_DESTINATION_AIRPORT)
      {
        /*
         * Calculamos la longitud, si es mayor que 1 es que tenemos
         * algo que copiar
         */
        len = end - start;

        if (len > 1)
        {

          if (len > STR_CODE_AIRPORT)
          {
            printf("ERROR len code airport\n");
            exit(1);
          }

          /*
           * Copiamos el substring
           */
          for (iterator = start; iterator < end - 1; iterator++)
          {
            word[iterator - start] = line[iterator];
          }
          /*
           * Introducimos el caracter de fin de palabra
           */
          word[iterator - start] = eow;
          /*
           * Comprobamos que el campo no sea NA (Not Available)
           */
          if (strcmp("NA", word) == 0)
            invalid = 1;
          else
          {
            switch (coma_count)
            {
            case COL_ORIGIN_AIRPORT:
              strcpy(origin, word);
              found++;
              break;
            case COL_DESTINATION_AIRPORT:
              strcpy(destination, word);
              found++;
              break;
            default:
              printf("ERROR in coma_count\n");
              exit(1);
            }
          }
        }
        else
        {
          /*
           * Si el campo esta vacio invalidamos la linea entera
           */

          invalid = 1;
        }
      }
      start = end;
    }
  } while (caracter && invalid == 0);

  if (found != 2)
    invalid = 1;

  return invalid;
}

void printids(const char *s)
{
  pid_t pid;
  pthread_t tid;

  pid = getpid();
  tid = pthread_self();
  printf("%s pid %u tid %u (0x%x)\n", s, (unsigned int)pid, (unsigned int)tid, (unsigned int)tid);
}


typedef struct Node {
  char **lines;
  int nelems;
} Node;


// create a new Node
Node *CreateNode()
{


  Node *node = malloc(sizeof(Node));
  if (!node)
  {
    printf("ERROR: could not allocate memory for node\n");
    exit(1);
  }

  node->lines = malloc(sizeof(char *) * N_BLOCK);
  if (!node->lines)
  {
    printf("ERROR: could not allocate memory for lines in node\n");
    free(node);
    exit(1);
  }

  int i;
  for (i = 0; i < N_BLOCK; i++)
  {
    node->lines[i] = calloc(1, sizeof(char) * MAXCHAR);

    if (!node->lines[i])
    {
      printf("ERROR: could not allocate memory for line of lines in node\n");
      free(node->lines);
      free(node);
      exit(1);
    }
  }

  node->nelems = 0;

  return node;
}

//  Destory node 
void DestroyNode(Node *node)
{
  int i;
  for (i = 0; i < N_BLOCK; i++)
  {
    free(node->lines[i]);
  }
  free(node->lines);
  free(node);
  node = NULL;
}

typedef struct Queue
{
  Node **buffer;
  int front;
  int rear;
  int size;
  int capacity;
  int finish;
  pthread_mutex_t lock;
} Queue;

// create a queue for buffer 
Queue *CreateQueue()
{

  Queue *queue = malloc(sizeof(Queue));
  if (!queue)
  {
    printf("ERROR: could not allocate memory for queue\n");
    exit(1);
  }

  int i, j;

  queue->buffer = malloc(sizeof(Node *) * B_BUFFER);
  if (!queue->buffer)
  {
    printf("ERROR: could not allocate memory for queue buffer\n");
    free(queue);
    exit(1);
  }

  for (i = 0; i < B_BUFFER; i++)
  {
    queue->buffer[i] = malloc(sizeof(Node *));
    if (!queue->buffer[i])
    {
      printf("ERROR: could not allocate memory for lines in queue buffer\n");
      free(queue->buffer);
      free(queue);
      exit(1);
    }

    queue->buffer[i]->lines = malloc(sizeof(char *) * N_BLOCK);
    if (!queue->buffer[i]->lines)
    {
      printf("ERROR: could not allocate memory for line of lines in queue buffer\n");
      free(queue->buffer);
      free(queue);
      exit(1);
    }

    for (j = 0; j < N_BLOCK; j++)
    {
      queue->buffer[i]->lines[j] = calloc(1, sizeof(char) * MAXCHAR);
      if (!queue->buffer[i]->lines[j])
      {
        printf("ERROR: could not allocate memory for line of lines in queue buffer\n");
        free(queue->buffer[i]->lines);
        free(queue->buffer[i]);
        free(queue->buffer);
        free(queue);
        exit(1);
      }
    }

    queue->buffer[i]->nelems = 0;
  }

  queue->front = -1;
  queue->rear = -1;
  queue->size = 0;
  queue->capacity = B_BUFFER;
  queue->finish = 0;

  int result = pthread_mutex_init(&queue->lock, NULL);
  if (result != 0)
  {
    printf("ERROR: could not initialize mutex\n");
    free(queue->buffer);
    free(queue);
    exit(1);
  }

  return queue;
}

// destroy queue
void DestroyQueue(Queue *queue)
{

  int i, j;
  for (i = 0; i < B_BUFFER; i++)
  {
    for (j = 0; j < N_BLOCK; j++)
    {
      free(queue->buffer[i]->lines[j]);
    }
    free(queue->buffer[i]->lines);
    free(queue->buffer[i]);
  }
  free(queue->buffer);

  pthread_mutex_destroy(&queue->lock);

  free(queue);
  queue = NULL;
}

int isFull(Queue *queue)
{
  return (queue->size == queue->capacity);
}
 
int isEmpty(Queue *queue)
{
  return (queue->size == 0);
}

// insert node into queue
int addElement(Queue *queue, Node *info)
{

  int result = pthread_mutex_lock(&queue->lock);
  if (result != 0)
  {
    printf("ERROR: could not acquire lock on mutex\n");
    return 0; // fail
  }

  if (isFull(queue))
  {
    printf("ERROR: queue is full\n");
    pthread_mutex_unlock(&queue->lock);
    return 0; // fail
  }

  queue->rear++;
  queue->rear %= queue->capacity;
  queue->buffer[queue->rear] = info;
  queue->size++;

  result = pthread_mutex_unlock(&queue->lock);
  if (result != 0)
  {
    printf("ERROR: could not release lock on mutex\n");
    return 0; // fail
  }

  return 1; // success
}


// get last inserted node from queue
Node *getElement(Queue *queue)
{

  int result = pthread_mutex_lock(&queue->lock);
  if (result != 0)
  {
    printf("ERROR: could not acquire lock on mutex\n");
    return ((void *)0);
  }

  if (isEmpty(queue))
  {
    return ((void *)0);
  }

  queue->front = (queue->front + 1) % queue->capacity;
  Node *element = queue->buffer[queue->front];
  queue->size--;

  result = pthread_mutex_unlock(&queue->lock);
  if (result != 0)
  {
    printf("ERROR: could not release lock on mutex\n");
    return ((void *)0);
  }

  return element;
}

typedef struct param_prod
{
  FILE *fp;
  Queue *queue;
  int done;
} param_prod;

typedef struct param_cons
{
  FILE *fp2;
  int **num_flights;
  char **airports;
  Queue *queue;
  int done;
} param_cons;


void *productor(void *arg)
{

  param_prod *par = (struct param_prod *)arg;
  FILE *fp = par->fp;
  Queue *queue = par->queue;
  char temp[MAXCHAR];

  while (1)
  {

    pthread_mutex_lock(&mutex);

    while (isFull(queue))
    {
      // if queue is full, produce waiting threads
      pthread_cond_wait(&prod, &mutex);
    }

    // create new node for queue
    Node *temp = CreateNode();

    while (temp->nelems < N_BLOCK && !feof(fp))
    {
      // put information into node 
      fgets(temp->lines[temp->nelems], MAXCHAR, fp);
      temp->nelems++;
    }

    // add new node to queue
    addElement(queue, temp);

    // now queue isn't empty, call consumer to consume
    pthread_cond_signal(&cons);
    pthread_mutex_unlock(&mutex);

    if (feof(fp))
    {
      // if file is over, call consuemr, and set queue to finish
      queue->finish = 1;
      pthread_cond_signal(&cons);
      pthread_mutex_unlock(&mutex);
      return ((void *)0);
      ;
    }
  }

  return ((void *)0);
}


void *consumidor(void *arg)
{

  param_cons *par = (struct param_cons *)arg;
  int **num_flights = par->num_flights;
  char **airports = par->airports;
  Queue *queue = par->queue;

  char origin[STR_CODE_AIRPORT], destination[STR_CODE_AIRPORT];
  int invalid, index_origin, index_destination;

  while (1)
  {

    if (queue->finish && isEmpty(queue))
    {
      // if queue is finish and queue is empty it means all data has been written
      return ((void *)0);
    }

    pthread_mutex_lock(&mutex);


    while (isEmpty(queue))
    {
      if (queue->finish && isEmpty(queue))
      {
        pthread_mutex_unlock(&mutex);
        return ((void *)0);
      }

      // if queue is empty, consumer waiting for producer to produce information
      pthread_cond_wait(&cons, &mutex);
    }

    // get information from queue
    Node *temp = getElement(queue);


    for (int i = 0; i < temp->nelems; i++)
    {
      // update information on num_flights
      invalid = extract_fields_airport(origin, destination, temp->lines[i]);

      if (!invalid)
      {
        index_origin = get_index_airport(origin, airports);
        index_destination = get_index_airport(destination, airports);

        if ((index_origin >= 0) && (index_destination >= 0))
        {
          num_flights[index_origin][index_destination]++;
        }
      }
    }

    // for now, queue isn't empty, call producer to produce information
    pthread_cond_signal(&prod);
    pthread_mutex_unlock(&mutex);

    if (queue->finish && isEmpty(queue))
    {
      // if queue is finish and queue is empty it means all data has been written, queit thread
      pthread_mutex_unlock(&mutex);
      break;
    }
  }

  return ((void *)0);
}

/**
 * Dado un fichero CSV que contiene informacion entre multiples aeropuertos,
 * esta funcion lee cada linea del fichero y actualiza la matriz num_flights
 * para saber cuantos vuelos hay entre cada cuidad origen y destino.
 */
void read_airports_data(int **num_flights, char **airports, char *fname)
{
  char line[MAXCHAR];
  int i;

  pthread_t ntid_prod[NUM_FILS_PRODUCTOR];
  pthread_t ntid_cons[NUM_FILS_CONSUMIDOR];

  param_prod par_prod[NUM_FILS_PRODUCTOR];
  param_cons par_cons[NUM_FILS_CONSUMIDOR];

  FILE *fp;

  fp = fopen(fname, "r");
  if (!fp)
  {
    printf("ERROR: could not open '%s'\n", fname);
    exit(1);
  }

  /* Leemos la cabecera del fichero */
  fgets(line, MAXCHAR, fp);

  Queue *queue = CreateQueue();

  // thread productor
  for (i = 0; i < NUM_FILS_PRODUCTOR; i++)
  {
    par_prod[i].fp = fp;
    par_prod[i].queue = queue;
    pthread_create(ntid_prod + i, NULL, productor, (void *)&par_prod[i]);
  }

  // thread consumidor
  for (i = 0; i < NUM_FILS_CONSUMIDOR; i++)
  {

    par_cons[i].num_flights = num_flights;
    par_cons[i].airports = airports;
    par_cons[i].queue = queue;
    pthread_create(ntid_cons + i, NULL, consumidor, (void *)&par_cons[i]);
  }

  for (i = 0; i < NUM_FILS_PRODUCTOR; i++)
  {
    pthread_join(ntid_prod[i], NULL);
  }

  for (i = 0; i < NUM_FILS_CONSUMIDOR; i++)
  {
    pthread_join(ntid_cons[i], NULL);
  }

  DestroyQueue(queue);
  fclose(fp);
}

/**
 * Esta es la funcion principal que realiza los siguientes procedimientos
 * a) Lee los codigos IATA del fichero de aeropuertos
 * b) Lee la informacion de los vuelos entre diferentes aeropuertos y
 *    actualiza la matriz num_flights correspondiente.
 * c) Se imprime para cada aeropuerto origen cuantos destinos diferentes
 *    hay.
 * d) Se imprime por pantalla lo que ha tardado el programa para realizar
 *    todas estas tareas.
 */

int main(int argc, char **argv)
{
  char **airports;
  int **num_flights;

  if (argc != 3)
  {
    printf("%s <airport.csv> <flights.csv>\n", argv[0]);
    exit(1);
  }

  struct timeval tv1, tv2;

  // Tiempo cronologico
  gettimeofday(&tv1, NULL);

  // Reserva espacio para las matrices
  airports = (char **)malloc_matrix(NUM_AIRPORTS, STR_CODE_AIRPORT, sizeof(char));
  num_flights = (int **)malloc_matrix(NUM_AIRPORTS, NUM_AIRPORTS, sizeof(int));

  // Lee los codigos de los aeropuertos
  read_airports(airports, argv[1]);

  // Lee los datos de los vuelos
  read_airports_data(num_flights, airports, argv[2]);

  // Imprime un resumen de la tabla
  print_num_flights_summary(num_flights, airports);

  // Libera espacio
  free_matrix((void **)airports, NUM_AIRPORTS);
  free_matrix((void **)num_flights, NUM_AIRPORTS);

  // Tiempo cronologico
  gettimeofday(&tv2, NULL);

  // Tiempo para la creacion del arbol
  printf("Tiempo para procesar el fichero: %f segundos\n",
         (double)(tv2.tv_usec - tv1.tv_usec) / 1000000 +
             (double)(tv2.tv_sec - tv1.tv_sec));

  return 0;
}
