import math

def wu_line(x1: int, y1: int, x2: int, y2: int):
    points = []
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [(x1, y1, 1.0)], []

    steep = abs(dy) > abs(dx)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1.0

    def plot(px, py, intensity):
        intensity = max(0.0, min(1.0, intensity))
        if intensity > 0.01:
            if steep:
                points.append((py, px, intensity))
            else:
                points.append((px, py, intensity))

    plot(x1, y1, 1.0)

    intery = y1 + gradient
    for x in range(x1 + 1, x2):
        y_int = math.floor(intery)
        frac = intery - y_int
        i1 = 1.0 - frac
        i2 = frac

        plot(x, y_int, i1)
        plot(x, y_int + 1, i2)

        intery += gradient

    if x1 != x2:
        plot(x2, y2, 1.0)

    return points, []
