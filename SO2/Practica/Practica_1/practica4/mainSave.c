#include <stdlib.h>
#include "model/CSVReader.h"
#include "model/User.h"
#include "model/RecommendationMatrix.h"
#include "model/Movie.h"
#include "model/MatrixDiskService.h"
#include "model/HashTableDiskService.h"

int main() {
    int numberOfFiles = 1;
    struct FileMovies fileMovies[numberOfFiles];
    // First we get the movies, their ratings and the rating authors from the CSV file.
    fileMovies[0] = getMoviesFromCSV("./data/reduced_data.txt");
    // Once we have obtained the raw value, we filter the unique users for building the recommendation matrix.
    struct UniqueUsersResult uniqueUsersResult = getUniqueUsers(numberOfFiles, fileMovies);
    int numberOfUniqueUsers;
    struct User *uniqueUsers;
    uniqueUsers = uniqueUsersResult.userList;
    numberOfUniqueUsers = uniqueUsersResult.numberOfUsers;
    // Same procedure for movies.
    struct UniqueMoviesResult uniqueMoviesResult = getUniqueMovies(numberOfFiles, fileMovies);
    int numberOfUniqueMovies;
    struct Movie *uniqueMovies;
    uniqueMovies = uniqueMoviesResult.moviesList;
    numberOfUniqueMovies = uniqueMoviesResult.numberOfMovies;
    // Now we create a hash table that will link the position in the recommendation matrix with movies and users IDs.
    createHashMoviesAndUsers(numberOfUniqueUsers, numberOfUniqueMovies);
    // Now we fill this hash table.
    addUsersToTable(numberOfUniqueUsers, uniqueUsers);
    addMoviesToTable(numberOfUniqueMovies, uniqueMovies);
    // Now we create the recommendation matrix and we fill it with the values obtained previously.
    struct RecommendationMatrix recommendationMatrix = createEmptyRecommendationMatrix(numberOfUniqueUsers, numberOfUniqueMovies);
    fillRecommendationMatrix(numberOfUniqueMovies, uniqueMovies, &recommendationMatrix);
    // Once we have built the matrix, we save the matrix and the hash values into disk. We will save the metadata of
    // the matrix, like the number of rows and columns in one file, and its content in another file. The hash table values
    // are saved in a separate file too.
    char *matrixFilepath = "./matrix.bin";
    char *matrixMetadata = "./meta.bin";
    char *hashFilepath = "./hash.bin";
    saveMatrixIntoDisk(matrixFilepath, matrixMetadata, &recommendationMatrix);
    saveHashTableMoviesAndUsers(hashFilepath, numberOfUniqueUsers, uniqueUsers, numberOfUniqueMovies, uniqueMovies);
    // Freeing hash table resources
    removeMoviesAndUsersFromTable(numberOfUniqueMovies, uniqueMovies, numberOfUniqueUsers, uniqueUsers);
    destroyHashMoviesAndUsers();
    // Freeing recommendation matrix
    freeRecommendationMatrix(&recommendationMatrix);
    // Free raw data obtained from CSV
    for (int i = 0; i < numberOfFiles; i++) {
        freeFileMovies(&fileMovies[i]);
    }
    // Freeing movies and users structures.
    for(int i=0; i < numberOfUniqueMovies; i++) {
        freeMovie(&uniqueMovies[i]);
    }
    free(uniqueMovies);
    free(uniqueUsers);
}