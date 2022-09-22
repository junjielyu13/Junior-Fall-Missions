#include "User.h"
#include "Movie.h"
#include "../dataStructures/set.h"

#include <stdlib.h>
#include <stdio.h>

#define MAX_AUXILIAR_USERS 500000

/**
 * You should free manually the userList inside UniqueUsersResult.
 * @param numberOfFiles
 * @param moviesFromFile
 * @return
 */
struct UniqueUsersResult getUniqueUsers(int numberOfFiles, struct FileMovies *moviesFromFile) {
    struct User *users = malloc(MAX_AUXILIAR_USERS*sizeof(struct User));
    struct UniqueUsersResult result;
    int numberOfUniqueUsers = 0;
    int currentUserId;
    struct Set *uniqueUsers = createSet(50000);
    for(int i=0; i<numberOfFiles; i++) {
        for(int j=0; j<moviesFromFile[i].numberOfMovies; j++) {
            for(int t=0; t < moviesFromFile[i].movies[j].numberOfRatings; t++) {
                currentUserId = moviesFromFile[i].movies[j].ratings[t].customerId;
                if(!isValueInSet(uniqueUsers, currentUserId)) {
                    insertInSet(uniqueUsers, currentUserId);
                    users[numberOfUniqueUsers].userId = currentUserId;
                    numberOfUniqueUsers++;
                }
            }
        }
    }
    freeSet(uniqueUsers);
    users = (struct User*) realloc(users, numberOfUniqueUsers*sizeof(struct Movie));
    if(users == NULL) {
        printf("Memory management failed. Contact professors\n");
        exit(1);
    }
    result.userList = users;
    result.numberOfUsers = numberOfUniqueUsers;
    return result;
}