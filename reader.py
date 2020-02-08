from wordlist import *
import pyttsx3 as tts

class Reader:
    def __init__(self, wl=SeqWL(), idx=0):
        self.wordlist = wl
        self.speaker = tts.init()
        self.modes = ['word', 'meaning', 'eg']
        self.cnt = len(self.modes)
        self.idx = 0
        self.history = [wl.get_word()]

    def pronounce(self):
        self.speaker.say(self.history[-1]['word'])
        self.speaker.runAndWait()

    def get_string(self):
        return self.history[-1][self.modes[self.idx]]

    def get_cursor(self):
        return str(self.wordlist.idx+1) + '/' + str(self.wordlist.size)

    def set_word(self, idx):
        self.wordlist.idx = idx
        self.history.append(self.wordlist.get_word())

    def shift_word(self, amount):
        self.history.append(self.wordlist.shift_word(amount))

    def shift_mode(self, amount):
        self.idx = (self.idx + amount) % self.cnt
        while self.modes[self.idx] not in self.history[-1].keys():
            self.idx = (self.idx + amount) % self.cnt

    def adjust_freq(self, factor):
        self.words.adj_word('freq', lambda x: x*factor)

    def close(self):
        self.wordlist.store_cursor()


