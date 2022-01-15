import os
import re


def check_and_open_file(file_path):
    if file_path == "":
        raise FileNotFoundError
    if file_path[-4:] != ".txt":
        raise FileNotFoundError("Неверный формат файла")
    pages = []
    previous_tail = ""
    p = re.compile(r"""[.!?»"] \w""")
    file = open(file_path, 'r', encoding='utf-8')
    while True:
        new_data = file.read(4096)
        if not new_data:
            break
        if len(new_data) == 4096:
            last_index = [m.end(0) for m in re.finditer(p, new_data)][-1] - 1
            new_tail = new_data[last_index:]
            pages.append(previous_tail + new_data[:last_index])
            previous_tail = new_tail
        else:
            pages.append(previous_tail + new_data)
    file.close()
    return pages


def save_file(file_path, text):
    with open(file_path, encoding="utf-8", mode="w") as file:
        file.write(text)


def delete_file(file_path):
    os.remove(file_path)


def shift_pos(pos, count):
    line = pos.split(".")[0]
    row = int(pos.split(".")[1])
    return f"{line}.{row + int(count)}"


# todo реализовать логику работы с тегами через класс ниже
# todo это поможет сохранять теги и возобновлять форматирование при повторном открытии файла
# class Tag:
#     def __init__(self, id, start=None, end=None, underline=False, style=[NORMAL], type="times new roman", size=22):
#         self.id = id
#         self.start = start
#         self.end = end
#         self.underline = underline
#         self.style = style
#         self.type = type
#         self.size = size
#
#     def update(self, start=None, end=None, underline=None, style=None, type=None, size=None):
#         if start is not None:
#             self.start = start
#         if end is not None:
#             self.end = end
#         if underline is not None:
#             self.underline = underline
#         if style is not None:
#             self.style = style
#         if type is not None:
#             self.type = type
#         if size is not None:
#             self.size = size
