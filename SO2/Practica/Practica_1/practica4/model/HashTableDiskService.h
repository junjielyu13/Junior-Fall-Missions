#ifndef PRACTICA4_HASHTABLEDISKSERVICE_H
#define PRACTICA4_HASHTABLEDISKSERVICE_H

#include "RecommendationMatrix.h"

void saveHashTableMoviesAndUsers(char* filepath, int numberOfUsers, struct User* users, int numberOfMovies, struct Movie* movies);
struct HashTableLoadedResult loadHashTableMoviesAndUsers(char *filepath);

#endif //PRACTICA4_HASHTABLEDISKSERVICE_H
