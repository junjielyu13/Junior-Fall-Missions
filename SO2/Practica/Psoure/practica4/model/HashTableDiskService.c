#include "HashTableDiskService.h"
#include <search.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void saveHashTableMoviesAndUsers(char* filepath, int numberOfUsers, struct User* users, int numberOfMovies, struct Movie* movies) {
    ENTRY pairRow, *ep;
    int idx;
    FILE *hashTableFile = fopen(filepath, "w");
    fwrite(&numberOfMovies, sizeof(int), 1, hashTableFile);
    fwrite(&numberOfUsers, sizeof(int), 1, hashTableFile);
    char key[10];
    for(int i=0; i<numberOfMovies; i++) {
        sprintf(key, "m%d", movies[i].movieId);
        pairRow.key = key;
        ep = hsearch(pairRow, FIND);
        if (ep != NULL) {
            idx = (int)(intptr_t)(ep->data);
            fwrite(&movies[i].movieId, sizeof(int), 1, hashTableFile);
            fwrite(&idx, sizeof(int), 1, hashTableFile);
        }
    }
    for(int i=0; i<numberOfUsers; i++) {
        sprintf(key, "u%d", users[i].userId);
        pairRow.key = key;
        ep = hsearch(pairRow, FIND);
        if (ep != NULL) {
            idx = (int)(intptr_t)(ep->data);
            fwrite(&users[i].userId, sizeof(int), 1, hashTableFile);
            fwrite(&idx, sizeof(int), 1, hashTableFile);
        }
    }
    fclose(hashTableFile);
}

/*
 * The lists of users and movies returned in the struct HashTableLoadedResult contains only IDs with the purpose of
 * deleting the hash table.
 */
struct HashTableLoadedResult loadHashTableMoviesAndUsers(char *filepath) {
    struct HashTableLoadedResult hashTableLoaded;
    ENTRY pairRow, *ep;
    int idx, movieId, userId;
    char key[10];
    FILE *hashTableFile = fopen(filepath, "r");
    fread(&hashTableLoaded.numberOfMovies, sizeof(int), 1, hashTableFile);
    fread(&hashTableLoaded.numberOfUsers, sizeof(int), 1, hashTableFile);
    createHashMoviesAndUsers(hashTableLoaded.numberOfUsers, hashTableLoaded.numberOfMovies);
    hashTableLoaded.userList = malloc(hashTableLoaded.numberOfUsers*sizeof(struct User));
    hashTableLoaded.movieList = malloc(hashTableLoaded.numberOfMovies*sizeof(struct Movie));
    for(int i=0; i < hashTableLoaded.numberOfMovies; i++) {
        fread(&movieId, sizeof(int), 1, hashTableFile);
        fread(&idx, sizeof(int), 1, hashTableFile);
        sprintf(key, "m%d", movieId);
        pairRow.key = strdup(key);
        pairRow.data = (void *) (intptr_t) idx;
        hashTableLoaded.movieList[i].movieId = movieId;
        ep = hsearch(pairRow, ENTER);
        if (ep == NULL) {
            fprintf(stderr, "entry failed\n");
            exit(EXIT_FAILURE);
        }
    }
    for(int i=0; i < hashTableLoaded.numberOfUsers; i++) {
        fread(&userId, sizeof(int), 1, hashTableFile);
        fread(&idx, sizeof(int), 1, hashTableFile);
        sprintf(key, "u%d", userId);
        pairRow.key = strdup(key);
        pairRow.data = (void *) (intptr_t) idx;
        hashTableLoaded.userList[i].userId = userId;
        ep = hsearch(pairRow, ENTER);
        if (ep == NULL) {
            fprintf(stderr, "entry failed\n");
            exit(EXIT_FAILURE);
        }
    }
    fclose(hashTableFile);
    return hashTableLoaded;
}