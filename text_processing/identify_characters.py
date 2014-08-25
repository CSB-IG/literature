# seek NNPs that have no 'character' field.
# contiguous NNPs are offered, user chooses lists of them
# and binds them to character names.
# if contiguous NNPs are non-characters user adds None character.
# when looping next few NNPs are to be shown. If lists of tokens are
# found that are in characters' list, add 'character' field to them
# automatically next time they're found


import argparse
from pymongo import MongoClient, collection

import curses

parser = argparse.ArgumentParser(description='Tokenize text, load it into mongoDB.')

parser.add_argument('--uri', type=str, required=True, help='DB uri, e.g. mongodb://localhost:27017/my_database')
parser.add_argument('--collection', type=str, required=True, help='MongoDB collection, e.g. the name of the text')


args   = parser.parse_args()

client = MongoClient(args.uri)
db     = client.get_default_database()
collec = collection.Collection( db, args.collection )

    

class CharacterList:
    characters = []
    def __init__(self, height = 45, width = 40, x = 80, y = 0):
        self.update_chars()
        self.win = curses.newwin(height, width, y, x)
        self.win.bkgd(' ', curses.color_pair(2))

    def update_chars(self):
        self.characters = sorted(list(set([t['character'] for t in collec.find({'character': {'$exists': True}})])))
        
    def render(self):
        self.win.clear()
        self.win.box()
        self.win.addstr(0,1,"[ Characters ]", curses.color_pair(2))
        y = 1
        for character in self.characters:
            if character:
                self.win.addstr(y,1,
                                character,
                                curses.color_pair(2))
                y+=1
        self.win.refresh()



class TokenScroll:
    tokens = []
    def __init__(self, height = 15, width = 40, x = 0, y = 0):
        self.win = curses.newwin(height, width, y, x)
        self.win.bkgd(' ', curses.color_pair(2))
        self.update_tokens()

    def update_tokens(self):
        (height, width) = self.win.getmaxyx()
        self.tokens = []
        tmp = []

        self.tokens = [t for t in collec.find({'tag': 'NNP',
                                               'character': {'$exists': False}}).limit(height-2)]

        
    def render(self):
        self.win.clear()
        self.win.box()
        self.win.addstr(0,1,"[ NNP Tokens ]", curses.color_pair(2))
        y = 1
        for token in self.tokens:
            self.win.addstr(y,1,
                                  "%s %s" % (token['index'], token['token']),
                                  curses.color_pair(2))
            y+=1
        self.win.refresh()



class CharacterBuild:
    tokens = []
    def __init__(self, height=15, width=40, x=40):
        y = 0
        self.win = curses.newwin(height, width, y, x)
        self.win.bkgd(' ', curses.color_pair(1))


    def add_token(self, token):
        self.tokens.append(token)

    def render(self):
        self.win.clear()
        self.win.box()
        self.win.addstr(0,1,"[ build character ]", curses.color_pair(1))
        y = 1
        for token in self.tokens:
            self.win.addstr(y,1, "%s %s" % (token['index'], token['token']),
                            curses.color_pair(1))
            y+=1
            
        self.win.refresh()

    def build(self, name):
        # tag selected tokens as characters
        for t in self.tokens:
            t['character'] = name
            collec.save(t)

        # search all others and tag them too

        # need to do this over and over until the array of tokens are no longer found or something
        next_tokens = []
        for t in self.tokens:
            next_tokens.append(collec.find_one({'tag': 'NNP',
                                               'character': {'$exists': False},
                                               'token': t['token'] }))

        if len(self.tokens)>1:
            contiguous = True
            for n in range(0,len(next_tokens)-1):
                if next_tokens[n+1]['index'] != next_tokens[n]['index']+1:
                    contiguous = False
        
            if contiguous:
                for t in next_tokens:
                    t['character'] = name
                    collec.save(t)
        else:
            # what if it's just one token?
            pass
        # empty build area
        self.tokens = []

        
def getCharacterName(height = 1, width = 40, x = 40, y = 0):
    name_win = curses.newwin(height, width, y, x)
    name_win.bkgd(' ', curses.color_pair(3))
    curses.echo()
    #curses.curs_set(1)
    name = name_win.getstr(0,0,39)
    del name_win
    curses.noecho()
    #curses.curs_set(0)
    return name
    

def noneCharacter(token):
    token['character'] = None
    collec.save(token)

    for t in collec.find({'tag': 'NNP',
                          'character': {'$exists': False},
                          'token': token['token']}):
        t['character'] = None
        collec.save(t)

    
def main(stdscr):
    # initialize curses environment
    curses.curs_set(1)
    stdscr.nodelay(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)

    (height, width) = stdscr.getmaxyx()

    ts = TokenScroll(height=height, width=width/3)
    cb = CharacterBuild(width=width/3, x=width/3)
    char_list = CharacterList(height=height, width=width/3, x=(width/3)*2)
    
    while 1:
        cb.render()
        char_list.render()
        ts.render()
        ts.win.move(1,1)
        
        c = ts.win.getch()
        if c == ord('a'):
            cb.add_token(ts.tokens.pop(0))

        elif c == ord('c'):
            # ask for character's name
            if len(cb.tokens):
                name = getCharacterName(width=width/3, x=width/3)
                stdscr.refresh()
                # add character field to tokens in CharacterBuild object
                cb.build(name)
                ts.update_tokens()
                char_list.update_chars()
        elif c == ord('d'):
            cb.tokens = []
        elif c == ord('n'):
            noneCharacter(ts.tokens.pop(0))
            ts.update_tokens()
        elif c == ord('q'):
            break  # Exit the while()


curses.wrapper(main)
