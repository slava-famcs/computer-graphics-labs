def castle_pitteway_line(x1: int, y1: int, x2: int, y2: int):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx == 0 and dy == 0:
        return [(x1, y1, 1.0)], []

    steep = dy > dx
    if steep:
        dx, dy = dy, dx

    if dy == 0:
        code = "s" * dx
    elif dy == dx:
        code = "d" * dx
    else:
        u = dx - dy
        v = dy
        m1 = "s"
        m2 = "d"

        while u != v:
            if u > v:
                u -= v
                m2 = m1 + m2[::-1]
            else:
                v -= u
                m1 = m2 + m1[::-1]

        base_word = m2 + m1[::-1]
        code = base_word * u

    cx, cy = x1, y1
    points.append((cx, cy, 1.0))

    for move in code:
        if move == 's':
            if steep:
                cy += sy
            else:
                cx += sx
        elif move == 'd':
            cx += sx
            cy += sy
        points.append((cx, cy, 1.0))

    return points, []
