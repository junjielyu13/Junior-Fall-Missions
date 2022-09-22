//
// Created by ruben on 15/3/21.
//

#ifndef PRACTICA4_MOVIE_H
#define PRACTICA4_MOVIE_H

#include "Rating.h"
#include "Movie.h"

struct FileMovies {
    struct Movie * movies;
    int numberOfMovies;
};

struct Movie {
    int movieId;
    int numberOfRatings;
    struct Rating *ratings;
};

struct UniqueMoviesResult {
    struct Movie* moviesList;
    int numberOfMovies;
};

struct UniqueMoviesResult getUniqueMovies(int numberOfFiles, struct FileMovies *moviesFromFile);
int getNumberOfUniqueMovies(int numberOfFiles, struct FileMovies *moviesFromFile);
void freeMovie(struct Movie *movie);
void copyRatings(struct Movie* fromMovie, struct Movie* toMovie);
void freeFileMovies(struct FileMovies *fileMovies);

#endif //PRACTICA4_MOVIE_H
