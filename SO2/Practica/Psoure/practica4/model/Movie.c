#include <stdlib.h>
#include "Movie.h"
#include "Rating.h"

/**
 * You should free manually the userList inside UniqueMoviesResult.
 * @param numberOfFiles
 * @param moviesFromFile
 * @return
 */
struct UniqueMoviesResult getUniqueMovies(int numberOfFiles, struct FileMovies *moviesFromFile) {
    struct UniqueMoviesResult result;
    int numberOfUniqueMovies = getNumberOfUniqueMovies(numberOfFiles, moviesFromFile);
    int currentMovieId = 0;
    struct Movie* moviesList = malloc(numberOfUniqueMovies*sizeof(struct Movie));
    for(int i=0; i < numberOfFiles; i++) {
        for(int j=0; j< moviesFromFile[i].numberOfMovies; j++) {
            copyRatings(&moviesFromFile[i].movies[j], &moviesList[currentMovieId]);
            moviesList[currentMovieId].movieId = moviesFromFile[i].movies[j].movieId;
            currentMovieId++;
        }
    }
    result.moviesList = moviesList;
    result.numberOfMovies = numberOfUniqueMovies;
    return result;
}

/**
 * This method is intended to be used only as auxiliary method of getUniqueMovies with toMovie movie without ratings
 * initialized. If not, the method will perform an invalid free.
 * @param fromMovie
 * @param toMovie
 */
void copyRatings(struct Movie* fromMovie, struct Movie* toMovie) {
    toMovie->ratings = malloc(fromMovie->numberOfRatings*sizeof(struct Rating));
    for(int i=0; i<fromMovie->numberOfRatings; i++) {
        toMovie->ratings[i].customerId = fromMovie->ratings[i].customerId;
        toMovie->ratings[i].rating = fromMovie->ratings[i].rating;
    }
    toMovie->numberOfRatings = fromMovie->numberOfRatings;
}

int getNumberOfUniqueMovies(int numberOfFiles, struct FileMovies *moviesFromFile) {
    int numberOfUniqueMovies = 0;
    for(int i=0; i<numberOfFiles; i++)
        numberOfUniqueMovies  += moviesFromFile[i].numberOfMovies;
    return numberOfUniqueMovies;
}

void freeMovie(struct Movie *movie) {
    free((*movie).ratings);
}

void freeFileMovies(struct FileMovies *fileMovies) {
    for(int i=0; i<(*fileMovies).numberOfMovies; i++)
        freeMovie(&(*fileMovies).movies[i]);
    free((*fileMovies).movies);
}
