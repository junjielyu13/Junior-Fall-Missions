#ifndef PRACTICA4_MATRIXDISKSERVICE_H
#define PRACTICA4_MATRIXDISKSERVICE_H

#include "RecommendationMatrix.h"

void saveMatrixIntoDisk(char *matrixFilepath, char *metadataFilepath, struct RecommendationMatrix *recommendationMatrix);
struct RecommendationMatrix loadMatrixFromDisk(char *filepath, char *metadata_filepath);

#endif //PRACTICA4_MATRIXDISKSERVICE_H
