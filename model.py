import os


def check_and_open_file(file_path):
    if file_path == "":
        return False, ""
    if file_path[-4:] != ".txt":
        return False, "Неверный формат файла"
    with open(file_path, "r") as file:
        return True, file.read()


def save_file(file_path, text):
    with open(file_path, "w") as file:
        file.write(text)


def delete_file(file_path):
    os.remove(file_path)

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
