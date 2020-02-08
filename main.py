import PySimpleGUI as sg
import keyboard as kb
import signal
import queue
import const
from reader import *

rd = Reader()
layout = [ [sg.Button('+', disabled=False, key='pin'),
            sg.Text(rd.get_string(), size=(40, 1), font=('Arial', 30), justification='center', pad=(5, 30), key='main_text'), 
            sg.Text(rd.get_cursor(), size=(10, 1), font=('Arial', 10), justification='right', key='idx_text')] ]

window = sg.Window('GRE 1000', layout, keep_on_top = True, no_titlebar=True, alpha_channel=const.alpha, location=const.default_window_position, grab_anywhere=False, finalize=True) 

eventQ = queue.Queue() #(func, (args))
def sched(func):
    def ret(*args):
        eventQ.put((func, args))
    return ret

def toggle_hide():
    if toggle_hide.toggled:
        window.un_hide()
    else:
        window.hide()
    toggle_hide.toggled = not toggle_hide.toggled
toggle_hide.toggled = False

def drag():
    window.Read(timeout=0)
    window.GrabAnyWhereOn()
    window.Read(timeout=3000)
    window.GrabAnyWhereOff()
    window.Read(timeout=0)

def exit_by_sig(sig, frame):
    rd.close()
    window.close()
    exit(0)
signal.signal(signal.SIGTERM, exit_by_sig)

kb.add_hotkey('alt+/', sched(rd.shift_word), [1])
kb.add_hotkey('alt+.', sched(rd.shift_word), [-1])
kb.add_hotkey('alt+m', sched(rd.shift_word), [-10])
kb.add_hotkey('right ctrl+alt', sched(rd.shift_mode), [1])
kb.add_hotkey('alt+p', rd.pronounce)
kb.add_hotkey('alt+d', sched(drag))
kb.add_hotkey('alt+h', sched(toggle_hide))
kb.add_hotkey('alt+x', sched(os.kill), [os.getpid(), signal.SIGTERM])

while True:
    window.Read(timeout=0)
    event = eventQ.get()
    event[0](*event[1])
    window['main_text'].update(rd.get_string())
    window['idx_text'].update(rd.get_cursor())
