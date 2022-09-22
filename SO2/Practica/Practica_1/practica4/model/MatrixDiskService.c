#include "MatrixDiskService.h"
#include <search.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

void saveMatrixIntoDisk(char *matrixFilepath, char *metadataFilepath, struct RecommendationMatrix *recommendationMatrix) {
    FILE *matrixFile, *metadataFile;
    matrixFile = fopen(matrixFilepath, "w");
    metadataFile = fopen(metadataFilepath, "w");
    fwrite(&recommendationMatrix->numberOfRows , sizeof(int), 1, metadataFile);
    fwrite(&recommendationMatrix->numberOfColumns , sizeof(int), 1, metadataFile);
    fwrite(recommendationMatrix->grid, sizeof(float),
           recommendationMatrix->numberOfColumns*recommendationMatrix->numberOfRows, matrixFile);
    fclose(matrixFile);
    fclose(metadataFile);
}

struct RecommendationMatrix loadMatrixFromDisk(char *matrixFilepath, char *metadataFilepath) {
    struct RecommendationMatrix matrix;
    FILE *matrixFile, *metadataFile;
    matrixFile = fopen(matrixFilepath, "r");
    metadataFile = fopen(metadataFilepath, "r");
    if (!matrixFile || !metadataFile) {
        printf("One of both files do not exist. Aborting\n");
        exit(2);
    }
    fread(&matrix.numberOfRows, sizeof(int), 1, metadataFile);
    fread(&matrix.numberOfColumns, sizeof(int), 1, metadataFile);
    float *grid = (float *) mmap(NULL,
                                 matrix.numberOfRows*matrix.numberOfColumns*sizeof(float),
                                 PROT_READ, MAP_SHARED, fileno(matrixFile), 0);
    if(grid == MAP_FAILED) {
        printf("Error allocating matrix. Aborting\n");
        exit(1);
    }
    fclose(matrixFile);
    fclose(metadataFile);
    matrix.grid = grid;
    return matrix;
}