from tkinter import *
from tkinter import ttk


def config_window(window, width, height):
    window.geometry(f"{width}x{height}")
    window.resizable(width=False, height=False)
    window.iconphoto(False, PhotoImage(file="icon.png"))


def config_main_menu(window, main_menu):
    window.config(menu=main_menu)


def config_file_menu(file_menu, main_menu, command_dict):
    for label, command in command_dict.items():
        file_menu.add_command(label=label, command=command)
    main_menu.add_cascade(label="Файл", menu=file_menu)


def place_obj(obj, x, y, height=None, width=None):
    if height is not None and width is not None:
        obj.place(x=x, y=y, height=height, width=width)
    elif height is not None and width is None:
        obj.place(x=x, y=y, height=height)
    elif height is None and width is not None:
        obj.place(x=x, y=y, width=width)
    else:
        obj.place(x=x, y=y)


def create_button(master, text, command, x, y, height=None, width=None):
    btn = Button(master=master, text=text, command=command)
    place_obj(btn, x, y, height, width)


def get_combobox(master, values, x, y, height=None, width=None, current=0, state="normal"):
    combobox = ttk.Combobox(master=master, values=values, state=state)
    place_obj(combobox, x, y, height, width)
    combobox.current(current)
    return combobox


def get_frame(master, bg, x, y, height=None, width=None):
    frame = Frame(master=master, border=1, relief=SUNKEN, bg=bg)
    place_obj(frame, x, y, height, width)
    return frame


def create_bind(obj, event, command):
    obj.bind(event, command)


def create_label(master, text, x, y, height=None, width=None):
    lbl = Label(master=master, text=text)
    place_obj(lbl, x, y, height, width)


def get_entry(master, x, y, state="normal", height=None, width=None):
    entry = Entry(master=master, state=state)
    place_obj(entry, x, y, height, width)
    return entry


def get_spinbox(master, x, y, from_=0, to=0, state="normal", command=lambda: True, height=None, width=None):
    spinbox = Spinbox(master=master, from_=from_, to=to, state=state, command=command)
    place_obj(spinbox, x, y, height, width)
    return spinbox

