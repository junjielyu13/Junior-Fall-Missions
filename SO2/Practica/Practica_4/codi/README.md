

### SO2 PRACTICA 4:
    
**Compile**:
```
    $: gcc analisi.c -o analisi -lpthread
```

 * o with Makefile:
```
    $: make
```

**Analisi with valgrind**:
```
    $: gcc -g analisi.c -o analisi -lpthread; \
       valgrind --leak-check=full -s ./analisi aeroports.csv fitxer_petit.csv 2> errors.txt
```
**Run**:

```
    $: ./analisi aeroports.csv fitxer_petit.csv
```

**Compare two files**:
```
    $: make; \
       ./analisi aeroports.csv fitxer_petit.csv > test_petit.txt; \
       ./analisi_original aeroports.csv fitxer_petit.csv > original_petit.txt; \
       diff test_petit.txt original_petit.txt; \
```




