//
// Created by ruben on 15/3/21.
//

#ifndef PRACTICA4_SET_H
#define PRACTICA4_SET_H

struct DataItem {
    int *data;
    int elements;
};

struct Set {
    int size;
    struct DataItem *dataItem;
};

struct Set *createSet(int size);
void freeSet(struct Set* set);
void __freeDataItem(struct DataItem* dataItem);
int isValueInNode(struct DataItem *dataItem, int value);
int isValueInSet(struct Set* set, int value);
void removeFromSet(struct Set* set, int value);
void insertInSet(struct Set* set, int value);

#endif //PRACTICA4_SET_H
