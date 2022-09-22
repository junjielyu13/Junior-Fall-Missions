#include <stdlib.h>
#include "set.h"

struct Set *createSet(int size) {
    struct Set *set = malloc(sizeof(struct Set));
    (*set).size = size;
    (*set).dataItem = malloc(size*sizeof(struct DataItem));
    for(int i=0; i<size; i++) {
        (*set).dataItem[i].data = 0;
        (*set).dataItem[i].elements = 0;
    }
    return set;
}

void insertInSet(struct Set* set, int value) {
    int hashValue = value%set->size;
    if(set->dataItem[hashValue].elements == 0) {
        set->dataItem[hashValue].elements += 1;
        set->dataItem[hashValue].data = malloc(sizeof(int));
        set->dataItem[hashValue].data[0] = value;
    }
    else {
        /* First we check if the value is already inserted in the set */
        if(!isValueInNode(&(set->dataItem[hashValue]), value)) {
            set->dataItem[hashValue].elements += 1;
            set->dataItem[hashValue].data = (int *) realloc(set->dataItem[hashValue].data,
                                                            set->dataItem[hashValue].elements * sizeof(int));
            set->dataItem[hashValue].data[set->dataItem[hashValue].elements - 1] = value;
        }
    }
}

int isValueInSet(struct Set* set, int value) {
    int hashValue = value % set->size;
    if (set->dataItem[hashValue].elements == 0)
        return 0;
    else {
        if (!isValueInNode(&(set->dataItem[hashValue]), value))
            return 0;
    }
    return 1;
}

void removeFromSet(struct Set* set, int value) {
    int hashValue = value % set->size;
    if (set->dataItem[hashValue].elements != 0) {
        int dataIdx = 0;
        int foundData = 0;
        while(!foundData && !(dataIdx >= set->dataItem[hashValue].elements)) {
            if(set->dataItem[hashValue].data[dataIdx] == value)
                foundData = 1;
            else
                dataIdx++;
        }
        if(foundData) {
            if (set->dataItem[hashValue].elements == 1) {
                free(set->dataItem[hashValue].data);
                set->dataItem[hashValue].data = NULL;
            }
            else {
                int currentElem = 0;
                int *newData = malloc((set->dataItem[hashValue].elements - 1)*sizeof(int));
                for(int i = 0; i < set->dataItem[hashValue].elements; i++) {
                    if(i != dataIdx) {
                        newData[currentElem] = set->dataItem[hashValue].data[i];
                        currentElem +=1;
                    }
                }
                free(set->dataItem[hashValue].data);
                set->dataItem[hashValue].data = newData;
            }
            set->dataItem[hashValue].elements--;
        }
    }
}

int isValueInNode(struct DataItem *dataItem, int value) {
    for(int i=0; i < dataItem->elements; i++) {
        if(dataItem->data[i] == value)
            return 1;
    }
    return 0;
}

void freeSet(struct Set* set) {
    for(int i=0; i<set->size; i++)
        __freeDataItem(&(set->dataItem[i]));
    free(set->dataItem);
    free(set);
}
void __freeDataItem(struct DataItem* dataItem) {
    free(dataItem->data);
}