#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import os.path

from static import QUALITY_KEY, RECURSIVE_KEY, INPUT_KEY, OUTPUT_KEY, EXTENSION_KEY, \
    SKIP_STAT_KEY, AVIF_KEY, DIR_TREE_KEY, DEFAULT_EXTENSIONS, DEFAULT_QUALITY

_location = os.path.dirname(__file__)
_launch_string = f'python {_location}/main.py'


_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("600x300+639+236")
        top.minsize(120, 1)
        top.maxsize(4484, 1062)
        top.resizable(1,  1)
        top.title("Конвертация в heic/avif")

        self.top = top
        self.recursive = tk.IntVar(value=1)
        self.use_avif = tk.IntVar()
        self.copy_attrs = tk.IntVar(value=1)
        self.recreate_dirs = tk.IntVar(value=1)
        self.quality = tk.IntVar(value=DEFAULT_QUALITY)

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.867, rely=0.133, height=26, width=67)
        self.Button1.configure(text='''Обзор''')
        self.Button1.configure(command=self.button_1_click)

        self.Entry1 = tk.Entry(self.top)
        self.Entry1.place(relx=0.05, rely=0.133, height=20, relwidth=0.79)
        self.Entry1.configure(validate='focusout')
        self.Entry1.configure(validatecommand=self.validate)
        self.Entry1.configure(invalidcommand=self.on_invalid)

        self.Entry2 = tk.Entry(self.top)
        self.Entry2.place(relx=0.05, rely=0.31, height=20, relwidth=0.79)
        self.Entry2.configure(validate='focusout')
        self.Entry2.configure(validatecommand=self.validate)
        self.Entry2.configure(invalidcommand=self.on_invalid)

        self.Button2 = tk.Button(self.top)
        self.Button2.place(relx=0.867, rely=0.31, height=26, width=67)
        self.Button2.configure(text='''Обзор''')
        self.Button2.configure(command=self.button_2_click)

        self.Label2 = tk.Label(self.top)
        self.Label2.place(relx=0.05, rely=0.243, height=14, width=104)
        self.Label2.configure(anchor='w')
        self.Label2.configure(compound='left')
        self.Label2.configure(text='''Output dir:''')

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.05, rely=0.067, height=14, width=94)
        self.Label1.configure(anchor='w')
        self.Label1.configure(compound='left')
        self.Label1.configure(text='''Input dir:''')

        self.Checkbutton1 = tk.Checkbutton(self.top)
        self.Checkbutton1.place(relx=0.05, rely=0.433, relheight=0.057
                , relwidth=0.302)
        self.Checkbutton1.configure(anchor='w')
        self.Checkbutton1.configure(compound='left')
        self.Checkbutton1.configure(justify='left')
        self.Checkbutton1.configure(text='''Process subdirs''')
        self.Checkbutton1.configure(variable=self.recursive)

        self.Spinbox1 = tk.Spinbox(self.top, from_=0.0, to=100.0, textvariable=self.quality)
        self.Spinbox1.place(relx=0.167, rely=0.833, relheight=0.063
                , relwidth=0.075)

        self.Checkbutton4 = tk.Checkbutton(self.top)
        self.Checkbutton4.place(relx=0.05, rely=0.733, relheight=0.05
                , relwidth=0.435)
        self.Checkbutton4.configure(anchor='w')
        self.Checkbutton4.configure(compound='left')
        self.Checkbutton4.configure(justify='left')
        self.Checkbutton4.configure(text='''Use avif instead of heic''')
        self.Checkbutton4.configure(variable=self.use_avif)

        self.Checkbutton3 = tk.Checkbutton(self.top)
        self.Checkbutton3.place(relx=0.05, rely=0.633, relheight=0.057
                , relwidth=0.452)
        self.Checkbutton3.configure(anchor='w')
        self.Checkbutton3.configure(compound='left')
        self.Checkbutton3.configure(justify='left')
        self.Checkbutton3.configure(text='''Copy creation/modification time''')
        self.Checkbutton3.configure(variable=self.copy_attrs)

        self.Checkbutton2 = tk.Checkbutton(self.top)
        self.Checkbutton2.place(relx=0.05, rely=0.533, relheight=0.057
                , relwidth=0.418)
        self.Checkbutton2.configure(anchor='w')
        self.Checkbutton2.configure(compound='left')
        self.Checkbutton2.configure(justify='left')
        self.Checkbutton2.configure(text='''Recreate subdirs''')
        self.Checkbutton2.configure(variable=self.recreate_dirs)

        self.Label3 = tk.Label(self.top)
        self.Label3.place(relx=0.05, rely=0.833, height=21, width=64)
        self.Label3.configure(anchor='w')
        self.Label3.configure(compound='left')
        self.Label3.configure(text='''Quality''')

        self.Label4 = tk.Label(self.top)
        self.Label4.place(relx=0.50, rely=0.433, height=21, width=200)
        self.Label4.configure(anchor='w')
        self.Label4.configure(compound='left')
        self.Label4.configure(text='''Extensions to process:''')

        self.Entry3 = tk.Entry(self.top)
        self.Entry3.place(relx=0.50, rely=0.52, height=20, relwidth=0.4)
        self.Entry3.insert(0, DEFAULT_EXTENSIONS)

        self.Button3 = tk.Button(self.top)
        self.Button3.place(relx=0.867, rely=0.833, height=26, width=67)
        self.Button3.configure(state='disabled')
        self.Button3.configure(text='''Process''')
        self.Button3.configure(command=self.launch)

    def validate(self):
        self.get_launch_string()
        if self.Entry1.get() and self.Entry2.get():
            self.Button3.configure(state='active')
            return True
        return False

    def on_invalid(self):
        self.Button3.configure(state='disabled')

    def button_1_click(self):
        self.set_entry_text(self.Entry1, askdirectory())

    def button_2_click(self):
        self.set_entry_text(self.Entry2, askdirectory())

    def set_entry_text(self, e: tk.Entry, text):
        e.delete(0, tk.END)
        e.insert(0, text)
        self.validate()
        self.get_launch_string()

    def get_launch_string(self):
        launch_string = f'python "{_location}/main.py" ' \
                        f'{INPUT_KEY} {self.Entry1.get()} ' \
                        f'{OUTPUT_KEY} {self.Entry2.get()} ' \
                        f'{QUALITY_KEY} {self.Spinbox1.get()} ' \
                        f'{EXTENSION_KEY} "{self.Entry3.get()}"'

        if self.recursive.get():
            launch_string += f' {RECURSIVE_KEY}'
        if self.use_avif.get():
            launch_string += f' {AVIF_KEY}'
        if not self.copy_attrs.get():
            launch_string += f' {SKIP_STAT_KEY}'
        if self.recreate_dirs.get():
            launch_string += f' {DIR_TREE_KEY}'

        return launch_string

    def launch(self):
        os.system(self.get_launch_string())


def start_up():
    ttk = Toplevel1(tk.Tk())
    ttk.top.mainloop()


if __name__ == '__main__':
    start_up()




