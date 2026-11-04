def bresenham_circle(xc: int, yc: int, r: int):
    points = []
    if r < 0:
        return points, []

    x = 0
    y = r
    d = 3 - 2 * r

    def add_points(cx, cy, px, py):
        pts = [
            (cx + px, cy + py, 1.0), (cx - px, cy + py, 1.0),
            (cx + px, cy - py, 1.0), (cx - px, cy - py, 1.0),
            (cx + py, cy + px, 1.0), (cx - py, cy + px, 1.0),
            (cx + py, cy - px, 1.0), (cx - py, cy - px, 1.0)
        ]
        for pt in pts:
            if pt not in points:
                points.append(pt)

    while x <= y:
        add_points(xc, yc, x, y)
        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    return points, []
