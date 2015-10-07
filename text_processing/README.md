# Character networks

**find_names.py** will parse a text and find the sentnces where names
in a dictionary occur, it will output that in a JSON file.

Cal it thusly:


    python find_names.py --text data/narco/SresNarco/capitulo_1.txt \
                         --names data/nombres_verbos/apellidos_uniq.txt data/nombres_verbos/aliasfinal.txt \
                         --json aguas.json

