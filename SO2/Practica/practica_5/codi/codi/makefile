all: analisi analisi_original

# analisi: analisi.c
# 	gcc -o analisi analisi.c -lpthread

analisi: analisi.c
	gcc -g analisi analisi.c -lpthread

analisi_original: analisi_original.c
	gcc -o analisi_original analisi_original.c -lpthread

clean:
	rm -f analisi
