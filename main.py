import PySimpleGUI as sg
import keyboard as kb
import queue
from reader import *

#sg.change_look_and_feel('DarkAmber')

rd = Reader()
layout = [ [sg.Button('+', disabled=True, key='drag'),
            sg.Text(rd.get_string(), size=(50, 1), font=('Arial', 30), justification='center', pad=(10, 30), key='main_text'), 
            sg.Text(rd.get_cursor(), size=(10, 1), font=('Arial', 10), justification='right', key='idx_text')] ]

window = sg.Window('GRE 1000', layout, keep_on_top = True, no_titlebar=True, alpha_channel=.7, grab_anywhere=True, finalize=True) 

eventQ = queue.Queue()
def guihandle(event, value):
    if event == 'setword':
        rd.set_word(str(value))

kb.add_hotkey('alt+right', eventQ.put, args=(lambda: rd.shift_word(1),))
kb.add_hotkey('alt+left', eventQ.put, args=(lambda: rd.shift_word(-1),))
kb.add_hotkey('alt+up', eventQ.put, args=(lambda: rd.shift_mode(1),))
kb.add_hotkey('alt+down', eventQ.put, args=(lambda: rd.shift_mode(-1),))
kb.add_hotkey('alt+m', eventQ.put, args=(lambda: (window['drag'].update(disabled=False), guihandle(*window.Read()), window['drag'].update(disabled=True)),))
kb.add_hotkey('alt+x', eventQ.put, args=(lambda: exit(window.close()),))

while True:
    window.Read(timeout=0)
    event = eventQ.get()
    event()
    window['main_text'].update(rd.get_string())
    window['idx_text'].update(rd.get_cursor())
