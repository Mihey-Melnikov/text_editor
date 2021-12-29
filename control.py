from tkinter import *
from tkinter import messagebox, filedialog, colorchooser, font
from _tkinter import TclError
import model
import view


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title("2M NotePad")
        width = 800
        height = 600
        view.config_window(self.window, width, height)

        self.curr_file = None
        self.tag_number = 0
        self.tag_dict = {}

        self.main_menu = Menu(master=self.window)
        view.config_main_menu(self.window, self.main_menu)

        self.file_menu = Menu(master=self.main_menu, tearoff=0)
        view.config_file_menu(self.file_menu, self.main_menu,
                              {"Открыть": self.open_file, "Сохранить": self.save_file,
                               "Сохранить как": self.save_file_as, "Удалить": self.delete_file})

        settings_frame = LabelFrame(master=self.window, text="Настройки текста")
        view.place_obj(settings_frame, x=10, y=10, height=height / 6 + 10, width=width - 20)

        view.create_button(master=settings_frame, text="B", command=lambda: self.stylize_text(style=font.BOLD),
                           x=10, y=50, height=25, width=25)
        view.create_button(master=settings_frame, text="I", command=lambda: self.stylize_text(style=font.ITALIC),
                           x=40, y=50, height=25, width=25)
        view.create_button(master=settings_frame, text="U", command=lambda: self.stylize_text(underline=True),
                           x=70, y=50, height=25, width=25)
        view.create_button(master=settings_frame, text="↺", command=lambda: self.undo(),
                           x=100, y=50, height=25, width=25)
        view.create_button(master=settings_frame, text="↻", command=lambda: self.redo(),
                           x=130, y=50, height=25, width=25)
        view.create_button(master=settings_frame, text="Применить",
                           command=lambda: self.text.config(font=self.get_font()),
                           x=210, y=10, height=20, width=80)
        view.create_button(master=settings_frame, text="Цвет текста", command=lambda: self.choose_text_color(),
                           x=350, y=10, height=20, width=80)
        view.create_button(master=settings_frame, text="Цвет фона", command=lambda: self.choose_back_color(),
                           x=480, y=10, height=20, width=80)

        self.font_type = view.get_combobox(master=settings_frame, values=["arial", "calibri", "times new roman"],
                                           x=10, y=10, current=2)
        self.font_size = view.get_combobox(master=settings_frame, values=list(range(10, 61, 4)),
                                           x=160, y=10, width=40, current=3)

        self.text_color = view.get_frame(master=settings_frame, bg="#000000", x=440, y=10, width=20, height=20)
        self.back_color = view.get_frame(master=settings_frame, bg="#ffffff", x=570, y=10, width=20, height=20)

        self.text = Text(master=self.window, undo=True, font=self.get_font())
        view.place_obj(self.text, x=10, y=height / 5 + 10, height=height * 4 / 5 - 40, width=width - 35)

        scroll_text_ver = Scrollbar(master=self.window, orient="vertical", command=self.text.yview)
        view.place_obj(scroll_text_ver, x=775, y=height / 5 + 10, height=height * 4 / 5 - 40)
        self.text["yscrollcommand"] = scroll_text_ver.set

        view.create_bind(self.text, "<Control-o>", lambda _: self.open_file())
        view.create_bind(self.text, "<Control-s>", lambda _: self.save_file())
        view.create_bind(self.text, "<Control-d>", lambda _: self.delete_file())

        self.change_file_name()

    def show(self):
        self.window.mainloop()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        without_err, text = model.check_and_open_file(file_path)
        if without_err:
            self.text.delete(1.0, END)
            self.curr_file = file_path
            self.change_file_name(file_path.split("/")[-1])
            self.text.insert(INSERT, text)
        else:
            if text == "":
                return
            elif text == "Неверный формат файла":
                messagebox.showerror(text, "Откройте файл с расширением .txt")

    def save_file(self):
        if self.curr_file is None:
            self.save_file_as()
            return
        model.save_file(self.curr_file, self.text.get(1.0, END))

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename()
        if file_path == "":
            return
        self.curr_file = file_path
        self.change_file_name(file_path.split("/")[-1])
        model.save_file(self.curr_file, self.text.get(1.0, END))

    def delete_file(self):
        if self.curr_file is None:
            messagebox.showerror("Ошибка файла", "Файла не существует")
            return
        model.delete_file(self.curr_file)
        self.curr_file = None
        self.text.delete(1.0, END)
        self.change_file_name()

    def change_file_name(self, new_name=None):
        if new_name is None:
            self.window.title("2M NotePad")
        else:
            self.window.title(f"2M NotePad ― {new_name}")

    def stylize_text(self, underline=False, style=NORMAL, type="", size=""):
        if type == "":
            type = self.font_type.get()
        if size == "":
            size = self.font_size.get()
        tag_name = self.tag_number + 1
        self.text.tag_config(tag_name, font=(type, size, style), underline=underline)
        self.text.tag_add(tag_name, "sel.first", "sel.last")
        self.tag_number += 1

    def get_font(self, style=NORMAL, type="", size=""):
        if type == "":
            type = self.font_type.get()
        if size == "":
            size = self.font_size.get()
        return type, size, style

    def undo(self):
        try:
            self.text.edit_undo()
        except TclError:
            pass

    def redo(self):
        try:
            self.text.edit_redo()
        except TclError:
            pass

    def choose_text_color(self):
        (rgb, hx) = colorchooser.askcolor()
        self.text_color.config(bg=hx)
        self.text.config(fg=hx)

    def choose_back_color(self):
        (rgb, hx) = colorchooser.askcolor()
        self.back_color.config(bg=hx)
        self.text.config(bg=hx)
