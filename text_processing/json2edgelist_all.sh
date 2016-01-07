python json2pickle.py --json data/narco/LibrosNarcoTxt/cartel_de_sinaloa.json --pickle data/narco/cartel_de_sinaloa.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/cartel_incomodo.json --pickle data/narco/cartel_incomodo.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/imperio_del_chapo.json --pickle data/narco/imperio_del_chapo.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/marca_de_sangre.json --pickle data/narco/marca_de_sangre.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/narcoleaks.json --pickle data/narco/narcoleaks.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/senores_del_narco.json --pickle data/narco/senores_del_narco.pickle
python json2pickle.py --json data/narco/LibrosNarcoTxt/ultimo_narco.json --pickle data/narco/ultimo_narco.pickle

 
python pickle2edgelist.py --pickle data/narco/ultimo_narco.pickle > data/narco/LibrosNarcoTxt/ultimo_narco.csv
python pickle2edgelist.py --pickle data/narco/cartel_de_sinaloa.pickle > data/narco/LibrosNarcoTxt/cartel_de_sinaloa.csv
python pickle2edgelist.py --pickle data/narco/cartel_incomodo.pickle > data/narco/LibrosNarcoTxt/cartel_incomodo.csv
python pickle2edgelist.py --pickle data/narco/imperio_del_chapo.pickle > data/narco/LibrosNarcoTxt/imperio_del_chapo.csv
python pickle2edgelist.py --pickle data/narco/marca_de_sangre.pickle > data/narco/LibrosNarcoTxt/marca_de_sangre.csv
python pickle2edgelist.py --pickle data/narco/narcoleaks.pickle > data/narco/LibrosNarcoTxt/narcoleaks.csv
python pickle2edgelist.py --pickle data/narco/senores_del_narco.pickle > data/narco/LibrosNarcoTxt/senores_del_narco.csv
