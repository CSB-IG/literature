APELLIDOS=/home/rgarcia/literature/text_processing/data/nombres_verbos/apellidos_uniq.txt
ALIASES=/home/rgarcia/literature/text_processing/data/nombres_verbos/aliasfinal.txt


python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "El cartel de Sinaloa (Bestseller) - Diego Enrique Osorno.txt" --json cartel_de_sinaloa.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "El cartel incomodo - Jose Reveles.txt" --json cartel_incomodo.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "El imperio del Chapo - Rafael Rodriguez Castaneda.txt" --json imperio_del_chapo.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "El Ultimo Narco_ Chapo - Malcolm Beith.txt" --json ultimo_narco.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "Los Senores del Narco - Anabel Hernandez.txt" --json senores_del_narco.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "Marca de sangre - Hector de Mauleon Rodriguez.txt" --json marca_de_sangre.json &
python ~/literature/text_processing/find_names.py --names $APELLIDOS $ALIASES --text "Narcoleaks - Wilbert Torre.txt" --json narcoleaks.json &


