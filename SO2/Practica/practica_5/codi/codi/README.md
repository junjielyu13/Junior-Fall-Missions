
compile: 

* analisi normal 
  gcc analisi.c -o analisi
  gcc analisi_original.c -o analisi_original

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


  gcc programa.c -o programa -lpthread

run:

  ./analisi aeroports.csv fitxer_petit.csv > test_petit.txt
  ./analisi aeroports.csv 2007.csv
  ./analisi aeroports.csv 2008.csv


  ./analisi aeroports.csv 2007.csv > test_2007.txt;
  ./analisi_original aeroports.csv 2007.csv > original_2007.txt;
  diff test_2007.txt original_2007.txt

  ./analisi aeroports.csv 2008.csv > test_2008.txt
  ./analisi_original aeroports.csv 2008.csv > original_2008.txt
  diff test_2008.txt original_2008.txt



make; \
./analisi aeroports.csv fitxer_petit.csv > test_petit.txt; \
./analisi_original aeroports.csv fitxer_petit.csv > original_petit.txt; \
diff test_petit.txt original_petit.txt; \
./analisi aeroports.csv 2007.csv > test_2007.txt; \
./analisi_original aeroports.csv 2007.csv > original_2007.txt; \
diff test_2007.txt original_2007.txt; \
./analisi aeroports.csv 2008.csv > test_2008.txt; \
./analisi_original aeroports.csv 2008.csv > original_2008.txt; \
diff test_2008.txt original_2008.txt

