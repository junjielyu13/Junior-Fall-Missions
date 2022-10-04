# <div align="center"> SO2 Pràctica 1 </div>
----
###  <h3 align="right"> Authors: Manuel Liu Wang, Junjie Li </h3>

>

- #### **Exercici1**:  En executar el contenidor es farà un “bind mount” 

    >  #### Dockerfile: FROM gcc
    
    **Compilar**:  <code> 
    docker build -t practica4:v1 .
    </code>
    
    **run with bind mount**: 
    <code> docker run -ti -v $(pwd):/home/appuser/practica4 --name practica4-exercici-1 -d practica:v1
    </code>

    **run on a running container**
    <code>
    docker exec -it practica4-exercici-1 /bin/bash 
    </code>

- ### **Exercici2**: Execució en un contenidor petit

   > #### Dockerfile: FROM buildpack-deps:bullseye-curl

   **Compilar**:     
    <code> 
    docker build -t small-size .
    </code>


- ### **Exercici3**: Execució en un contenidor fent servir volums

    > #### Dockerfile: FROM buildpack-deps:bullseye-curl

    **run with mount volume**: 
    <code> docker run -ti -u root –-name practica4-exercici-3 -v vol-practica4:/home/appuser/practica4 small-size:latest
    </code>


---