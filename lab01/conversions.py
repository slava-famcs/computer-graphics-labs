# модуль с функциями перевода между цветовыми моделями rgb, cmyk и hsv
# rgb: r, g, b - целые от 0 до 255
# cmyk: c, m, y, k - целые проценты от 0 до 100
# hsv: h - целые от 0 до 360, s и v - целые проценты от 0 до 100


# ограничиваем значение диапазоном от low до high
def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


# переводим rgb в cmyk
def rgb_to_cmyk(r, g, b):
    r = clamp(r, 0, 255) / 255 # от 0 до 1
    g = clamp(g, 0, 255) / 255
    b = clamp(b, 0, 255) / 255
    # чёрная составляющая это единица минус самый большой канал
    k = 1 - max(r, g, b)
    # у чёрного цвета k = 1, а на ноль делить нельзя
    if k >= 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)


# переводим cmyk в rgb
def cmyk_to_rgb(c, m, y, k):
    c = clamp(c, 0, 100) / 100
    m = clamp(m, 0, 100) / 100
    y = clamp(y, 0, 100) / 100
    k = clamp(k, 0, 100) / 100
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return round(r), round(g), round(b)


# переводим rgb в hsv
def rgb_to_hsv(r, g, b):
    r = clamp(r, 0, 255) / 255
    g = clamp(g, 0, 255) / 255
    b = clamp(b, 0, 255) / 255
    mx = max(r, g, b)
    mn = min(r, g, b)
    d = mx - mn
    # считаем тон в градусах по тому, какой канал самый большой
    if d == 0:
        # серый цвет, тон не определён, берём ноль
        h = 0
    elif mx == r:
        h = 60 * (((g - b) / d) % 6)
    elif mx == g:
        h = 60 * ((b - r) / d + 2)
    else:
        h = 60 * ((r - g) / d + 4)
    # считаем насыщенность
    if mx == 0:
        # чёрный цвет, насыщенность тоже не определена
        s = 0
    else:
        s = d / mx
    v = mx
    return round(h), round(s * 100), round(v * 100)


# переводим hsv в rgb
def hsv_to_rgb(h, s, v):
    # h = 360 это тот же ноль градусов
    h = clamp(h, 0, 360) % 360
    s = clamp(s, 0, 100) / 100
    v = clamp(v, 0, 100) / 100
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c
    # выбираем сектор цветового круга шириной 60 градусов
    if h < 60:
        r, g, b = c, x, 0
    elif h < 120:
        r, g, b = x, c, 0
    elif h < 180:
        r, g, b = 0, c, x
    elif h < 240:
        r, g, b = 0, x, c
    elif h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)


# получаем hex-код цвета вида #ff8800 по rgb
def rgb_to_hex(r, g, b):
    r = int(clamp(round(r), 0, 255))
    g = int(clamp(round(g), 0, 255))
    b = int(clamp(round(b), 0, 255))
    return "#%02x%02x%02x" % (r, g, b)
