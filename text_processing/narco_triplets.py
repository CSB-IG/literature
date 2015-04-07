# coding: utf-8

from pattern.es import parsetree


theogony = open('data/narco/SresNarco/narco.txt').read()




s = parsetree(theogony, relations=True, lemmata=True)

for e in s:
    try:
        for v in e.verbs:
            if v.subject and v.object:
                subjects = []
                for w in v.subject:
                    if w.type == 'NNP':
                        subjects.append( w.string )
                objects = []
                for w in v.object:
                    if w.type == 'NNP':
                        objects.append( w.string )

                if objects and subjects:
                    print subjects, v.lemmata, objects
                        
    except:
        pass
