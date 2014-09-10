Estamos minando textos para extraer:

1. los personajes
2. el lugar en el que aparecen los personajes

Usando sus posiciones en el texto creamos redes de interacciones entre los personajes.


El pipeline
===========

args_nouns_extractor.py

Usa PyNLTK para tokenizar y categorizar. Imprime a la salida estándar la lista de nombres mayores a cierta longitud, en el orden en que aparecen.


byte_distance.pl

Greps for byte offsets of pseudonyms of characters in a text. Prints to stdout byte offset, Character.


Luego hay una porción en java que aún no publicamos. Toma la relación de byte_offsets genera la red y la escribe en formato que le gusta a [Cytoscape](http://www.cytoscape.org/])

Esta biblioteca: [cytoscape.js](http://cytoscape.github.io/cytoscape.js/)!




find_names.py y plot_names.py

Hacen lo del byte_distance.pl de encontrar la posición del personaje partiendo desde el byte 0.
Va haciendo combinaciones de 4, 3, 2 y 1 token. 
