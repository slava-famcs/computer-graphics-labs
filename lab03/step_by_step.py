def step_by_step_line(x1: int, y1: int, x2: int, y2: int):
    points = []
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [(x1, y1, 1.0)], []

    if abs(dx) >= abs(dy):
        k = dy / dx
        b = y1 - k * x1
        step = 1 if x2 >= x1 else -1
        for x in range(x1, x2 + step, step):
            y = round(k * x + b)
            points.append((x, y, 1.0))
    else:
        k_inv = dx / dy
        b_inv = x1 - k_inv * y1
        step = 1 if y2 >= y1 else -1
        for y in range(y1, y2 + step, step):
            x = round(k_inv * y + b_inv)
            points.append((x, y, 1.0))

    return points, []
