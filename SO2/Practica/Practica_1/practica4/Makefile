# typing 'make' will invoke the first target entry in the file 
# (in this case the default target entry)

CFLAGS=-O0 -Wall

default: mainSave mainRecc

# To create the executable file mainSave we need the object files

#assegura que nomes compila els objectes canviats 
mainSave: mainSave.o model/CSVReader.o model/Movie.o model/User.o model/RecommendationMatrix.o model/HashTableDiskService.o model/MatrixDiskService.o dataStructures/set.o
	gcc $(CFLAGS) mainSave.o model/CSVReader.o model/Movie.o model/User.o model/RecommendationMatrix.o model/HashTableDiskService.o model/MatrixDiskService.o dataStructures/set.o -o mainSave -lm

mainRecc: mainRecc.o model/CSVReader.o model/Movie.o model/User.o model/RecommendationMatrix.o model/HashTableDiskService.o model/MatrixDiskService.o dataStructures/set.o
	gcc $(CFLAGS) mainRecc.o model/CSVReader.o model/Movie.o model/User.o model/RecommendationMatrix.o model/HashTableDiskService.o model/MatrixDiskService.o dataStructures/set.o -o mainRecc -lm

# Creating object files
mainSave.o: mainSave.c  
	gcc $(CFLAGS) -c mainSave.c

mainRecc.o: mainRecc.c  
	gcc $(CFLAGS) -c mainRecc.c

model/CSVReader.o: model/CSVReader.c model/CSVReader.h
	gcc $(CFLAGS) -c model/CSVReader.c -Imodel -o model/CSVReader.o

model/Movie.o:  model/Movie.c model/Movie.h 
	gcc $(CFLAGS) -c model/Movie.c -Imodel -o model/Movie.o

model/User.o: model/User.c model/User.h
	gcc $(CFLAGS) -c model/User.c -Imodel -o model/User.o

model/RecommendationMatrix.o: model/RecommendationMatrix.c model/RecommendationMatrix.h
	gcc $(CFLAGS) -c model/RecommendationMatrix.c -Imodel -o model/RecommendationMatrix.o

model/HashTableDiskService.o: model/HashTableDiskService.c model/HashTableDiskService.h
	gcc $(CFLAGS) -c model/HashTableDiskService.c -Imodel -o model/HashTableDiskService.o

model/MatrixDiskService.o: model/MatrixDiskService.c model/MatrixDiskService.h
	gcc $(CFLAGS) -c model/MatrixDiskService.c -Imodel -o model/MatrixDiskService.o

dataStructures/set.o: dataStructures/set.c dataStructures/set.h
	gcc $(CFLAGS) -c dataStructures/set.c -IdataStructures -o dataStructures/set.o

# To start over from scratch, type 'make clean'.  This
# removes the executable file, as well as old .o object
# files and *~ backup files:
#
clean: 
	$(RM) mainSave *.o *~
	$(RM) mainRecc *.o *~
	cd model && $(RM) *.o *~
	cd dataStructures && $(RM) *.o *~


