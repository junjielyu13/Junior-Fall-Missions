#ifndef PRACTICA4_CSVREADER_H
#define PRACTICA4_CSVREADER_H

#include <stdio.h>
#include "Movie.h"

struct Rating getRating(char* line);
void addRatingsToMovie(struct Movie *movie, struct Rating *ratingsToAdd, int numberOfRatings);
void addMovieToCurrentMovies(struct Movie *movies, struct Movie *movieToAdd, int indexToAdd);
int lineIsMovie(char *line);
int getMovieId(char *line);
struct FileMovies getMoviesFromFile(FILE* trainingData);
struct FileMovies getMoviesFromCSV(const char  *filepath);

#endif //PRACTICA4_CSVREADER_H
