#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "Movie.h"
#include "Rating.h"
#include "CSVReader.h"

#define AUXILIAR_NUMBER_OF_MOVIES 20000
#define AUXILIAR_NUMBER_OF_RATINGS 500000

struct Rating getRating(char* line) {
    struct Rating rating;
    int customerId = atoi(strtok(line, ","));
    int ratingValue = atoi(strtok(NULL, ","));
    rating.customerId = customerId;
    rating.rating = ratingValue;
    return rating;
}

void addRatingsToMovie(struct Movie *movie, struct Rating *ratingsToAdd, int numberOfRatings) {
    (*movie).ratings = malloc(numberOfRatings * sizeof(struct Rating));
    (*movie).numberOfRatings = numberOfRatings;
    for(int i=0; i < numberOfRatings; i++) {
      (*movie).ratings[i].customerId = ratingsToAdd[i].customerId;
      (*movie).ratings[i].rating = ratingsToAdd[i].rating;
    }
}

void addMovieToCurrentMovies(struct Movie *movies, struct Movie *movieToAdd, int indexToAdd) {
    movies[indexToAdd].movieId = (*movieToAdd).movieId;
    movies[indexToAdd].ratings = (*movieToAdd).ratings;
    movies[indexToAdd].numberOfRatings = (*movieToAdd).numberOfRatings;
    (*movieToAdd).movieId = -1;
    (*movieToAdd).ratings = NULL;
}

int lineIsMovie(char *line) {
    int hasComma = 0;
    int idx = 0;
    int lineSize = strlen(line);
    while (!hasComma && idx < lineSize) {
        if(line[idx] == ',')
            hasComma = 1;
        idx++;
    }
    return 1 - hasComma;
}

int getMovieId(char *line) {
    return atoi(strtok(line, ":"));
}

struct FileMovies getMoviesFromFile(FILE* trainingData) {
    char line[1024]; 
    int movieId = -1;
    struct Movie *currentMovies = malloc(AUXILIAR_NUMBER_OF_MOVIES*sizeof(struct Movie));
    int currentIndexOfMovies = 0; // It coincides with the number of movies available.
    struct Movie currentMovie;
    struct Rating *currentRatings = malloc(AUXILIAR_NUMBER_OF_RATINGS*sizeof(struct Rating));
    int currentIndexOfRatings = 0; // It coincides with the number of ratings available per movie when reading.
    struct Rating currentRating;
    struct FileMovies moviesToReturn;

    while(fgets(line, sizeof(line), trainingData)) {
            if(lineIsMovie(line)) {
                if(movieId != -1) {
                    addRatingsToMovie(&currentMovie, currentRatings, currentIndexOfRatings);
                    addMovieToCurrentMovies(currentMovies, &currentMovie, currentIndexOfMovies); //Put ratings too
                    currentIndexOfMovies++;
                    currentIndexOfRatings = 0; 
                }
                movieId = getMovieId(line);
                currentMovie.movieId = movieId;
            }
            else {
                currentRating = getRating(line);
                currentRatings[currentIndexOfRatings].customerId = currentRating.customerId;
                currentRatings[currentIndexOfRatings].rating = currentRating.rating;
                currentIndexOfRatings++;
            }
        }
    // When we finish iterating we have one last movie to save.
    addRatingsToMovie(&currentMovie, currentRatings, currentIndexOfRatings);
    addMovieToCurrentMovies(currentMovies, &currentMovie, currentIndexOfMovies);
    currentIndexOfMovies++;
    // currentIndexOfMovies is the number of movies
    currentMovies = (struct Movie*) realloc(currentMovies, currentIndexOfMovies*sizeof(struct Movie));
    if(currentMovies == NULL) {
        printf("Memory management failed. Contact professors\n");
        exit(1);
    }
    moviesToReturn.movies = currentMovies;
    moviesToReturn.numberOfMovies = currentIndexOfMovies;
    // We only free currentRatings as we keep using currentMovies as returnable variable
    free(currentRatings);
    return moviesToReturn;
}



struct FileMovies getMoviesFromCSV(const char  *filepath) {
    FILE* trainingData = fopen(filepath, "r");
    struct FileMovies moviesToReturn;
    if (!trainingData) 
    {
        printf("Failed to open text file, does the file exist?\n");
        exit(1);
    }
    moviesToReturn = getMoviesFromFile(trainingData);
    fclose(trainingData);
    return moviesToReturn;
}