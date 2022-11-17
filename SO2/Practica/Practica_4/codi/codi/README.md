
compile: 

* analisi normal 
  gcc analisi.c -o analisi

* analisi with pthread 
  gcc analisi.c -o analisi -lpthread

* analisi with openmp
  gcc analisi.c -o analisi -fopenmp

* analisi with valgrind
  gcc -g analisi.c -o analisi 
  valgrind --leak-check=full -s ./analisi aeroports.csv fitxer_petit.csv 2> errors.txt

* altre callgrind
  valgrind --tool=callgrind ./analisi aeroports.csv fitxer_petit.csv
  kcachegrind callgrind.out.<pid>,

* memcheck:
  valgrind --tool=memcheck ./analisi aeroports.csv fitxer_petit.csv

* analisi with valgrind practica4
  gcc -g analisi.c -o analisi -lpthread
  valgrind --leak-check=full -s ./analisi aeroports.csv fitxer_petit.csv 2> errors.txt