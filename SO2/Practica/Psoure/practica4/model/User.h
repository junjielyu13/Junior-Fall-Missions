#ifndef PRACTICA4_USER_H
#define PRACTICA4_USER_H

#include "Movie.h"

struct User {
    int userId;
};

struct UniqueUsersResult {
    struct User* userList;
    int numberOfUsers;
};

struct UniqueUsersResult getUniqueUsers(int numberOfFiles, struct FileMovies *moviesFromFile);
#endif //PRACTICA4_USER_H
