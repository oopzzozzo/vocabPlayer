import PySimpleGUI as sg
import keyboard as kb
import signal
import queue
import const
from reader import *

#sg.change_look_and_feel('DarkAmber')

rd = Reader()
layout = [ [sg.Button('+', disabled=True, key='drag'),
            sg.Text(rd.get_string(), size=(40, 1), font=('Arial', 30), justification='center', pad=(5, 30), key='main_text'), 
            sg.Text(rd.get_cursor(), size=(10, 1), font=('Arial', 10), justification='right', key='idx_text')] ]

window = sg.Window('GRE 1000', layout, keep_on_top = True, no_titlebar=True, alpha_channel=const.alpha, location=const.default_window_position, grab_anywhere=True, finalize=True) 

eventQ = queue.Queue()
def guihandle(event, value):
    if event == 'setword':
        rd.set_word(str(value))

def exit_by_sig(sig, frame):
    rd.close()
    window.close()
    exit(0)
signal.signal(signal.SIGTERM, exit_by_sig)

kb.add_hotkey('alt+/', eventQ.put, args=(lambda: rd.shift_word(1),))
kb.add_hotkey('alt+.', eventQ.put, args=(lambda: rd.shift_word(-1),))
kb.add_hotkey('alt+m', eventQ.put, args=(lambda: rd.shift_word(-10),))
kb.add_hotkey('right ctrl+alt', eventQ.put, args=(lambda: rd.shift_mode(1),))
kb.add_hotkey('alt+d', eventQ.put, args=(lambda: (window['drag'].update(disabled=False), guihandle(*window.Read()), window['drag'].update(disabled=True)),))
kb.add_hotkey('alt+h', eventQ.put, args=(lambda: window.hide(),))
kb.add_hotkey('alt+shift+h', eventQ.put, args=(lambda: window.un_hide(),))
kb.add_hotkey('alt+x', eventQ.put, args=(lambda: os.kill(os.getpid(), signal.SIGTERM),))


while True:
    window.Read(timeout=0)
    event = eventQ.get()
    event()
    window['main_text'].update(rd.get_string())
    window['idx_text'].update(rd.get_cursor())
