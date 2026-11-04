def bresenham_line(x1: int, y1: int, x2: int, y2: int):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    steep = dy > dx
    if steep:
        dx, dy = dy, dx

    err = 2 * dy - dx
    x, y = x1, y1

    for _ in range(dx + 1):
        points.append((x, y, 1.0))
        if err >= 0:
            if steep:
                x += sx
            else:
                y += sy
            err -= 2 * dx
        if steep:
            y += sy
        else:
            x += sx
        err += 2 * dy

    return points, []
