#include <stdio.h>      
#include <sys/socket.h> 
#include <arpa/inet.h>  
#include <stdlib.h>     
#include <string.h>     
#include <unistd.h>     

#define BUFSIZE      100   // Mida del buffer 


int main(int argc, char *argv[])
{
  int len, sock;                  // Descriptor de socket 
  struct sockaddr_in server_addr; // Adreça del servidor 
  unsigned short server_port;     // Port del servidor 
  char *server_ip;                // Adreça IP del servidor en format huma 
  char buffer[BUFSIZE];           // Buffer 

  if (argc != 3) 
  {
    fprintf(stderr, "Us: %s <Server IP> [<Port Servidor>]\n", argv[0]);
    exit(EXIT_FAILURE);
  }

  server_ip = argv[1];            
  server_port = atoi(argv[2]);  

  // Crear una connexió TCP/IP 
  sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (sock < 0) {
    printf("socket() failed\n");
    exit(EXIT_FAILURE);
  }

  // Construeix l'estructura de l'adreça del servidor 
  memset(&server_addr, 0, sizeof(server_addr));         
  server_addr.sin_family      = AF_INET;                
  server_addr.sin_addr.s_addr = inet_addr(server_ip);   
  server_addr.sin_port        = htons(server_port);   

  // Estableix connexio amb el servidor 
  if (connect(sock, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
    printf("connect() failed.\n");
    exit(EXIT_FAILURE);
  }

  printf("Connexió establerta amb el servidor.\n");

  // Enviem una cadena
  printf("Quina cadena vols enviar?\n");
  fgets(buffer, BUFSIZE, stdin);
  
  // Eliminem el '\n' del buffer
  buffer[strlen(buffer)-1] = '\0';

  // L'enviem
  len = strlen(buffer);
  write(sock, &len, 4);
  write(sock, buffer, len);

  // Esperem una resposta del servidor 
  read(sock, &len, 4);
  read(sock, buffer, len);
  buffer[len] = '\0';

  printf("He rebut la seguent cadena com a resposta\n");
  printf("%s\n", buffer);

  // Tanca connexio amb servidor 
  close(sock);

  return EXIT_SUCCESS;
}
