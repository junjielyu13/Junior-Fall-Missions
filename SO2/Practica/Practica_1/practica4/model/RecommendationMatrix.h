#ifndef PRACTICA4_RECOMMENDATIONMATRIX_H
#define PRACTICA4_RECOMMENDATIONMATRIX_H

#include "User.h"
#include "Movie.h"

struct RecommendationMatrix {
    int numberOfRows;
    int numberOfColumns;
    float *grid;
};

struct HashTableLoadedResult {
    int numberOfUsers;
    int numberOfMovies;
    struct User* userList;
    struct Movie* movieList;
};

void createHashMoviesAndUsers(int numberOfUsers, int numberOfMovies);
struct RecommendationMatrix createEmptyRecommendationMatrix(int numberOfUsers, int numberOfMovies);
float accessRecommendationMatrixValue(int row, int col, struct RecommendationMatrix *recommendationMatrix);
void setRecommendationMatrixValue(int row, int col, float value, struct RecommendationMatrix *recommendationMatrix);
void addUsersToTable(int numberOfUsers, struct User* users);
void addMoviesToTable(int numberOfMovies, struct Movie* movies);
void destroyHashMoviesAndUsers();
int lookRowForUser(int userId);
int lookColForMovie(int movieId);
int getNumberOfMoviesSeenByUser(int rowUser, struct RecommendationMatrix *recommendationMatrix);
int getNumberOfUsersThatHaveSeenMovie(int colMovie, struct RecommendationMatrix *recommendationMatrix);
float similarityUsers(int rowUser1, int rowUser2, struct RecommendationMatrix *recommendationMatrix);
float forecastRating(int colMovieToScore, int rowUser, struct RecommendationMatrix *recommendationMatrix);
int getRecommendedMovieForUser(int rowUser, struct RecommendationMatrix *recommendationMatrix, struct Movie* movies, int numberOfMovies);
void fillRecommendationMatrix(int numberOfMovies, struct Movie* movies, struct RecommendationMatrix *recommendationMatrix);
void freeRecommendationMatrix(struct RecommendationMatrix *recommendationMatrix);
void removeMoviesAndUsersFromTable(int numberOfMovies, struct Movie* movies, int numberOfUsers, struct User* users);

// Private functions

float _getAccSum(int rowUser1, int rowUser2, struct RecommendationMatrix *recommendationMatrix);

#endif //PRACTICA4_RECOMMENDATIONMATRIX_H