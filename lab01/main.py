# окно с превью цвета, ползунками и полями ввода для каждой модели

import tkinter as tk
from tkinter import colorchooser

from conversions import clamp, cmyk_to_rgb, hsv_to_rgb, rgb_to_cmyk, rgb_to_hsv, rgb_to_hex

# имена компонент по моделям
rgb_names = ["r", "g", "b"]
cmyk_names = ["c", "m", "y", "k"]
hsv_names = ["h", "s", "v"]

# словари с виджетами и границами значений, ключ - имя компоненты
scales = {}
entries = {}
limits = {}

# что мы сами записали в поле ввода и в ползунок в последний раз
entry_text = {}
scale_value = {}

# флаг блокировки: пока он включён, виджеты не запускают пересчёт заново
updating = False

root = tk.Tk()
root.title("Цветовые модели cmyk, rgb, hsv")
root.resizable(False, False)


# берём значения компонент из ползунков
def read_scales(names):
    values = []
    for name in names:
        values.append(int(round(scales[name].get())))
    return values


# берём значения компонент из полей ввода
def read_entries(names):
    values = []
    for name in names:
        low, high = limits[name]
        text = entries[name].get().strip()
        try:
            value = int(text)
        except ValueError:
            # ввели не число, оставляем значение ползунка
            value = int(round(scales[name].get()))
        values.append(clamp(value, low, high))
    return values


# собираем значения одной модели, from_scale говорит, кто источник изменения
def collect(names, from_scale):
    if from_scale:
        return read_scales(names)
    return read_entries(names)


# пишем значения в ползунки и в поля ввода
def set_widgets(names, values):
    for name, value in zip(names, values):
        scales[name].set(value)
        entries[name].delete(0, "end")
        entries[name].insert(0, str(value))
        # запоминаем, что записали сами, чтобы отличить это от правки пользователя
        scale_value[name] = value
        entry_text[name] = str(value)


# показываем цвет по rgb: считаем две другие модели, превью и hex-код
# source_names и source_values - модель, из которой пришло изменение
def show_rgb(r, g, b, source_names=None, source_values=None):
    global updating
    r = clamp(int(round(r)), 0, 255)
    g = clamp(int(round(g)), 0, 255)
    b = clamp(int(round(b)), 0, 255)

    # переводим rgb в cmyk и hsv
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, s, v = rgb_to_hsv(r, g, b)

    # включаем блокировку, чтобы виджеты не вызвали пересчёт по кругу
    updating = True
    if source_names is None:
        set_widgets(rgb_names, (r, g, b))
        set_widgets(cmyk_names, (c, m, y, k))
        set_widgets(hsv_names, (h, s, v))
    else:
        # модель-источник пишем её же значениями, а не пересчитанными через rgb,
        # иначе из-за округления её ползунки дрожат при перетаскивании
        if source_names != rgb_names:
            set_widgets(rgb_names, (r, g, b))
        if source_names != cmyk_names:
            set_widgets(cmyk_names, (c, m, y, k))
        if source_names != hsv_names:
            set_widgets(hsv_names, (h, s, v))
        set_widgets(source_names, source_values)
    updating = False

    # обновляем цветной прямоугольник и подпись с hex-кодом
    color = rgb_to_hex(r, g, b)
    preview.configure(bg=color)
    hex_label.configure(text=color)


# изменение пришло от ползунка
def on_scale_move(name):
    if updating:
        return
    # tk иногда сама дёргает команду ползунка без изменения значения,
    # тогда пересчитывать нечего, иначе цвет уползает из-за округления
    if int(round(scales[name].get())) == scale_value.get(name):
        return
    apply_from(name, True)


# изменение пришло от поля ввода
def on_entry_apply(name):
    if updating:
        return
    # поле не правили, пересчитывать нечего, иначе цвет сдвинется из-за округления
    if entries[name].get() == entry_text.get(name):
        return
    apply_from(name, False)


# смотрим, из какой модели пришло изменение, и переводим её в rgb
def apply_from(name, from_scale):
    if name in rgb_names:
        values = collect(rgb_names, from_scale)
        r, g, b = values
        show_rgb(r, g, b, rgb_names, values)
    elif name in cmyk_names:
        values = collect(cmyk_names, from_scale)
        c, m, y, k = values
        r, g, b = cmyk_to_rgb(c, m, y, k)
        show_rgb(r, g, b, cmyk_names, values)
    else:
        values = collect(hsv_names, from_scale)
        h, s, v = values
        r, g, b = hsv_to_rgb(h, s, v)
        show_rgb(r, g, b, hsv_names, values)


# открываем системный выбор цвета из палитры
def choose_color():
    result = colorchooser.askcolor(title="выбор цвета")
    if result[0] is None:
        # диалог закрыли без выбора
        return
    r, g, b = result[0]
    show_rgb(r, g, b)


# одна строка блока: название компоненты, ползунок и поле ввода
def add_row(parent, row, title, name, low, high):
    limits[name] = (low, high)

    label = tk.Label(parent, text=title, width=18, anchor="w")
    label.grid(row=row, column=0, sticky="w")

    scale = tk.Scale(parent, from_=low, to=high, orient="horizontal", length=300,
                     showvalue=False, command=lambda value, n=name: on_scale_move(n))
    scale.grid(row=row, column=1, padx=6, pady=2)

    entry = tk.Entry(parent, width=6, justify="center")
    entry.grid(row=row, column=2, padx=6)
    # значение из поля применяем по enter и когда поле теряет фокус
    entry.bind("<Return>", lambda event, n=name: on_entry_apply(n))
    entry.bind("<FocusOut>", lambda event, n=name: on_entry_apply(n))

    scales[name] = scale
    entries[name] = entry


# верхняя часть окна: превью цвета, hex-код и кнопка выбора из палитры
top = tk.Frame(root)
top.pack(fill="x", padx=10, pady=10)

preview = tk.Canvas(top, width=240, height=110, highlightthickness=1,
                    highlightbackground="#808080")
preview.grid(row=0, column=0, rowspan=2)

hex_label = tk.Label(top, text="#000000", font=("Consolas", 16))
hex_label.grid(row=0, column=1, sticky="w", padx=12)

pick_button = tk.Button(top, text="выбрать из палитры", command=choose_color)
pick_button.grid(row=1, column=1, sticky="w", padx=12)

# блоки моделей, в каждом по строке на компоненту
rgb_frame = tk.LabelFrame(root, text="RGB", padx=8, pady=6)
rgb_frame.pack(fill="x", padx=10)
add_row(rgb_frame, 0, "красный (R)", "r", 0, 255)
add_row(rgb_frame, 1, "зелёный (G)", "g", 0, 255)
add_row(rgb_frame, 2, "синий (B)", "b", 0, 255)

cmyk_frame = tk.LabelFrame(root, text="CMYK", padx=8, pady=6)
cmyk_frame.pack(fill="x", padx=10, pady=(6, 0))
add_row(cmyk_frame, 0, "голубой (C)", "c", 0, 100)
add_row(cmyk_frame, 1, "пурпурный (M)", "m", 0, 100)
add_row(cmyk_frame, 2, "жёлтый (Y)", "y", 0, 100)
add_row(cmyk_frame, 3, "чёрный (K)", "k", 0, 100)

hsv_frame = tk.LabelFrame(root, text="HSV", padx=8, pady=6)
hsv_frame.pack(fill="x", padx=10, pady=(6, 10))
add_row(hsv_frame, 0, "тон (H)", "h", 0, 360)
add_row(hsv_frame, 1, "насыщенность (S)", "s", 0, 100)
add_row(hsv_frame, 2, "яркость (V)", "v", 0, 100)

# начальный цвет при запуске
show_rgb(60, 120, 200)

root.mainloop()
