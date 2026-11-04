def dda_line(x1: int, y1: int, x2: int, y2: int):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return [(x1, y1, 1.0)], []

    x_inc = dx / steps
    y_inc = dy / steps

    x = float(x1)
    y = float(y1)

    for _ in range(steps + 1):
        points.append((round(x), round(y), 1.0))
        x += x_inc
        y += y_inc

    return points, []
