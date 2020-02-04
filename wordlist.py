import os.path
import numpy as np
import json
import const
class WordList:
    def __init__(self, fn=const.default_fn, wordlist=None, *args, **kwargs):
        self.fn = fn
        self.words = []
        self.size = 0
        self.idx = self.load_cursor()
        if wordlist is None:
            self.load_words(*args, **kwargs)
        else:
            self.words = wordlist
            self.size = len(self.words)

    def load_words(self, fn=None, start=0, end=None, append=False, backup=True):
        if fn is None:
            fn = self.fn
        if not append:
            self.words = []
        if not os.path.exists(fn) and fn[-5:] != '.json':
            fn.append('.json')
        with open(fn, "r") as json_file:
            self.words += json.load(json_file)[start:end]
            self.size = len(self.words)
        if backup:
            backup_fn = fn + '-origin' if fn[-5:] != '.json' else fn[:-5] + '-origin.json'
            with open(backup_fn, "w") as dump_file:
                json.dump(self.words, dump_file)

    def store_words(self, fn=None):
        if fn is None:
            fn = self.fn
        if not os.path.exists(fn) and fn[-5:] != '.json':
            fn.append('.json')
        with open(fn, "w") as out_file:
            json.dump(self.words, out_file)

    def adj_word(self, field, op):
        self.words[self.idx][field] = op(self.words[self.idx].get(field, None))
    def load_cursor(self, fn=".cursor.dat"):
        if not os.path.exists(fn):
            return 0
        with open(fn, "r") as f:
            return int(next(f))

    def store_cursor(self, fn=".cursor.dat"):
        with open(fn, "w") as f:
            f.write(str(self.idx))
    
class SeqWL(WordList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_word(self):
        return self.words[self.idx]

    def shift_word(self, amount):
        self.idx = (self.idx + amount) % self.size
        return self.get_word()

class RandWL(WordList):
    def __init__(self):
        super().__init(*args, **kwargs)
        self.idx = gen_idx()

    def gen_idx(self):
        self.idx = np.random.choice(range(self.size), map(lambda w: w.get('freq', 1), self.words))

    def get_word(self):
        gen_idx()
        return self.words[self.idx]

    def shift_word(self, amount):
        return self.get_word()
