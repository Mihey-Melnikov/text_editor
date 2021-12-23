import tkinter.font
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkinter.font import *
import os
import random


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title("NotePad")
        width = 800
        height = 600
        self.window.geometry(f"{width}x{height}")
        self.window.resizable(width=False, height=False)
        self.window.iconphoto(False, PhotoImage(file="icon.png"))

        self.curr_file = None

        self.main_menu = Menu(master=self.window)
        self.window.config(menu=self.main_menu)
        self.file_menu = Menu(master=self.main_menu, tearoff=0)
        self.file_menu.add_command(label="Открыть", command=self.open_file)
        self.file_menu.add_command(label="Сохранить", command=self.save_file)
        self.file_menu.add_command(label="Сохранить как", command=self.save_file_as)
        self.file_menu.add_command(label="Удалить", command=self.delete_file)
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)

        self.settings_frame = LabelFrame(master=self.window, text="Настройки текста")
        self.settings_frame.place(x=10, y=10, height=height / 4 - 20, width=width - 20)

        self.file_name = Entry(master=self.settings_frame, state="readonly")
        self.file_name.place(x=5, y=5, width=150)
        self.bold_btn = Button(master=self.settings_frame, text="B", command=lambda: self.text_by_style(BOLD))
        self.bold_btn.place(x=5, y=80, height=25, width=25)
        self.bold_btn = Button(master=self.settings_frame, text="I", command=lambda: self.text_by_style(ITALIC))
        self.bold_btn.place(x=35, y=80, height=25, width=25)
        self.bold_btn = Button(master=self.settings_frame, text="U", command=lambda: print("error!!!"))
        self.bold_btn.place(x=65, y=80, height=25, width=25)
        self.font_type = ttk.Combobox(master=self.settings_frame, values=["arial", "calibri", "times new roman"])
        self.font_type.place(x=50, y=50)
        self.font_size = ttk.Combobox(master=self.settings_frame, values=list(range(10, 61, 4)))
        self.font_size.place(x=200, y=50, width=40)
        self.apply_btn = Button(master=self.settings_frame, text="Применить",
                                command=lambda: self.text.config(font=self.get_font()))
        self.apply_btn.place(x=250, y=50, height=20, width=80)

        self.text = Text(master=self.window, undo=True, font=self.get_font())
        self.text.place(x=10, y=height / 4, height=height * 3 / 4 - 30, width=width - 20)
        scroll_text_ver = Scrollbar(master=self.text, orient="vertical")
        scroll_text_ver.config(command=self.text.yview)
        scroll_text_ver.pack(side="right", fill="y")
        scroll_text_hor = Scrollbar(master=self.text, orient="horizontal")
        scroll_text_hor.config(command=self.text.xview)
        scroll_text_hor.pack(side="bottom", fill="x")

        self.text.bind("<Control-o>", lambda _: self.open_file())
        self.text.bind("<Control-s>", lambda _: self.save_file())
        self.text.bind("<Control-d>", lambda _: self.delete_file())

        # self.text.tag_config("bold", font=self.get_font())
        # self.text.tag_config("italic", font=('arial', 20, ITALIC))
        # self.text.tag_config("underlined", font=('arial', 20), underline=True)

        self.change_file_name("-")

    def show(self):
        self.window.mainloop()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path == "":
            return
        if file_path[-4:] != ".txt":
            messagebox.showerror("Неверный формат файла", "Откройте файл с расширением .txt")
            return
        self.text.delete(1.0, END)
        self.curr_file = file_path
        self.change_file_name(file_path.split("/")[-1])
        with open(file_path, "r") as file:
            text = file.read()
            self.text.insert(INSERT, text)

    def save_file(self):
        if self.curr_file is None:
            self.save_file_as()
            return
        with open(self.curr_file, "w") as file:
            text = self.text.get(1.0, END)
            file.write(text)

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename()
        if file_path == "":
            return
        self.curr_file = file_path
        self.change_file_name(file_path.split("/")[-1])
        with open(file_path, "w") as file:
            text = self.text.get(1.0, END)
            file.write(text)

    def delete_file(self):
        if self.curr_file is None:
            messagebox.showerror("Ошибка файла", "Файла не существует")
            return
        os.remove(self.curr_file)
        self.curr_file = None
        self.text.delete(1.0, END)
        self.change_file_name("-")

    def change_file_name(self, new_name):
        self.file_name.config(state="normal")
        self.file_name.delete(0, END)
        self.file_name.insert(0, new_name)
        self.file_name.config(state="readonly")

    def text_by_style(self, style):
        tag_name = random.randint(1, 999999)  # костыль
        self.text.tag_config(tag_name, font=self.get_font(style))
        self.text.tag_add(tag_name, "sel.first", "sel.last")

    def get_font(self, style=NORMAL):
        font_type = self.font_type.get()
        if font_type == "":
            font_type = "arial"
        font_size = self.font_size.get()
        if font_size == "":
            font_size = 20
        return font_type, font_size, style
