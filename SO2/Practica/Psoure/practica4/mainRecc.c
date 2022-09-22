#include <stdio.h>
#include <stdlib.h>
#include "model/RecommendationMatrix.h"
#include "model/MatrixDiskService.h"
#include "model/HashTableDiskService.h"

enum EXEC_MODE {
    NUMBER_OF_MOVIES = 1,
    NUMBER_OF_USERS = 2,
    FORECAST = 3,
    PREDICT = 4
};

void getNumberOfMovies(int userId, struct RecommendationMatrix *recommendationMatrix) {
    int rowUser, numberOfMoviesSeenByUser;
    if(userId == 0) {
        printf("User id is not a valid number. Try again");
        exit(EXIT_FAILURE);
    }
    rowUser = lookRowForUser(userId);
    if(rowUser == -1) {
        printf("User id is not a valid id. Try again");
        exit(EXIT_FAILURE);
    }
    numberOfMoviesSeenByUser = getNumberOfMoviesSeenByUser(rowUser, recommendationMatrix);
    printf("The number of movies seen by the user %d is %d\n", userId, numberOfMoviesSeenByUser);
}

void getNumberOfUsers(int movieId, struct RecommendationMatrix *recommendationMatrix) {
    int colMovie, numberOfUsersThatHaveSeenMovie;
    if(movieId == 0) {
        printf("Movie id is not a valid number. Try again");
        exit(EXIT_FAILURE);
    }
    colMovie = lookColForMovie(movieId);
    if(colMovie == -1) {
        printf("Movie id is not a valid id. Try again");
        exit(EXIT_FAILURE);
    }
    numberOfUsersThatHaveSeenMovie = getNumberOfUsersThatHaveSeenMovie(colMovie, recommendationMatrix);
    printf("The number of users that have seen the movie %d is %d\n", movieId, numberOfUsersThatHaveSeenMovie);
}

void getForecast(int userId, int movieId, struct RecommendationMatrix *recommendationMatrix) {
    int colMovie, rowUser;
    if(userId == 0 || movieId == 0) {
        printf("User id or movie id are not proper numbers. Try again");
        exit(EXIT_FAILURE);
    }
    colMovie = lookColForMovie(movieId);
    rowUser = lookRowForUser(userId);
    if(colMovie == -1 || rowUser == -1) {
        printf("User id or movie id are not valid ids. Try again");
        exit(EXIT_FAILURE);
    }
    double forecastedRating = forecastRating(colMovie, rowUser, recommendationMatrix);
    printf("U:%d - M:%d - The forecasted rating was %f\n", userId, movieId, forecastedRating);
}

void getPredict(int userId, struct RecommendationMatrix *recommendationMatrix, struct Movie* movies, int numberOfMovies)  {
    int rowUser, recommendedMovieId;
    if(userId == 0) {
        printf("User id is not a valid number. Try again");
        exit(EXIT_FAILURE);
    }
    rowUser = lookRowForUser(userId);
    if(rowUser == -1) {
        printf("User id is not a valid id. Try again");
        exit(EXIT_FAILURE);
    }
    //Recommending movie.
    recommendedMovieId = getRecommendedMovieForUser(rowUser, recommendationMatrix, movies, numberOfMovies);
    printf("The recommended movie for user %d is %d\n", userId, recommendedMovieId);
}

int main(int argc, char *argv[]) {
    if(argc < 2) {
        printf("User id or movie id not specified properly. Try again");
        exit(EXIT_FAILURE);
    }
    int executionMode = atoi(argv[1]);
    if(executionMode < 1 || executionMode > 4) {
        printf("Not valid selection: Try again");
        exit(1);
    }
    // Firstly we load the matrix computed and saved in the other program.
    struct RecommendationMatrix recommendationMatrixLoaded;
    recommendationMatrixLoaded = loadMatrixFromDisk("./matrix.bin", "./meta.bin");
    // Secondly, we load the hash table and the movie and user ids.
    struct HashTableLoadedResult hashTableLoadedResult;
    int numberOfMovies, numberOfUsers;
    struct Movie* movies;
    struct User* users;
    hashTableLoadedResult = loadHashTableMoviesAndUsers("./hash.bin");
    numberOfMovies = hashTableLoadedResult.numberOfMovies;
    numberOfUsers = hashTableLoadedResult.numberOfUsers;
    movies = hashTableLoadedResult.movieList;
    users = hashTableLoadedResult.userList;
    // Now we execute the desired behaviour
    int userId, movieId;
    switch (executionMode) {
        case NUMBER_OF_MOVIES:
            userId = atoi(argv[2]);
            getNumberOfMovies(userId, &recommendationMatrixLoaded);
            break;
        case NUMBER_OF_USERS:
            movieId = atoi(argv[2]);
            getNumberOfUsers(movieId, &recommendationMatrixLoaded);
            break;
        case FORECAST:
            userId = atoi(argv[2]);
            movieId = atoi(argv[3]);
            getForecast(userId, movieId, &recommendationMatrixLoaded);
            break;
        case PREDICT:
            userId = atoi(argv[2]);
            getPredict(userId, &recommendationMatrixLoaded, movies, numberOfMovies);
            break;
    }
    //Freeing resources.
    removeMoviesAndUsersFromTable(numberOfMovies, movies, numberOfUsers, users);
    freeRecommendationMatrix(&recommendationMatrixLoaded);
    destroyHashMoviesAndUsers();
    free(movies);
    free(users);
}

