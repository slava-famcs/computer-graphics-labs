import tkinter as tk
from tkinter import ttk, messagebox

from step_by_step import step_by_step_line
from dda import dda_line
from bresenham_line import bresenham_line
from bresenham_circle import bresenham_circle
from castle_pitteway import castle_pitteway_line
from wu_line import wu_line


class RasterizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Лабораторная работа №3")
        self.root.geometry("1280x820")
        self.root.minsize(1024, 700)

        self.cell_size = 28
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.current_pixels = []
        self.ideal_shape = None
        self.show_ideal = tk.BooleanVar(value=True)

        self._setup_styles()
        self._build_ui()

        self.root.after(100, self.run_selected_algorithm)

    def _setup_styles(self):
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TFrame", background="#f4f6f9")
        style.configure("TLabelframe", background="#f4f6f9", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe.Label", background="#f4f6f9", foreground="#2c3e50")
        style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), foreground="#ffffff", background="#2980b9")
        style.map("Accent.TButton", background=[("active", "#1f6391")])
        style.configure("TRadiobutton", background="#f4f6f9", font=("Segoe UI", 10))
        style.configure("TCheckbutton", background="#f4f6f9", font=("Segoe UI", 10))

    def _build_ui(self):
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        left_panel = ttk.Frame(main_paned, padding=12, width=420)
        main_paned.add(left_panel, weight=0)

        right_panel = ttk.Frame(main_paned, padding=6)
        main_paned.add(right_panel, weight=1)

        algo_frame = ttk.LabelFrame(left_panel, text=" Выбор алгоритма ", padding=10)
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        self.algo_var = tk.StringVar(value="bres_line")
        algos = [
            ("Пошаговый алгоритм (отрезок)", "step"),
            ("Алгоритм ЦДА (отрезок)", "dda"),
            ("Алгоритм Брезенхема (отрезок)", "bres_line"),
            ("Алгоритм Брезенхема (окружность)", "bres_circle"),
            ("Алгоритм Кастла-Питвея", "castle"),
            ("Алгоритм Ву (сглаживание)", "wu"),
        ]
        for text, val in algos:
            rb = ttk.Radiobutton(
                algo_frame, text=text, variable=self.algo_var, value=val, command=self._on_algo_change
            )
            rb.pack(anchor=tk.W, pady=2)

        coord_frame = ttk.LabelFrame(left_panel, text=" Координаты ", padding=10)
        coord_frame.pack(fill=tk.X, pady=(0, 10))

        grid_f = ttk.Frame(coord_frame)
        grid_f.pack(fill=tk.X)

        self.lbl_x1 = ttk.Label(grid_f, text="X1 (или Xc):")
        self.lbl_x1.grid(row=0, column=0, sticky=tk.W, padx=4, pady=4)
        self.ent_x1 = ttk.Entry(grid_f, width=8)
        self.ent_x1.insert(0, "-2")
        self.ent_x1.grid(row=0, column=1, padx=4, pady=4)

        self.lbl_y1 = ttk.Label(grid_f, text="Y1 (или Yc):")
        self.lbl_y1.grid(row=0, column=2, sticky=tk.W, padx=4, pady=4)
        self.ent_y1 = ttk.Entry(grid_f, width=8)
        self.ent_y1.insert(0, "-1")
        self.ent_y1.grid(row=0, column=3, padx=4, pady=4)

        self.lbl_x2 = ttk.Label(grid_f, text="X2 (или R):")
        self.lbl_x2.grid(row=1, column=0, sticky=tk.W, padx=4, pady=4)
        self.ent_x2 = ttk.Entry(grid_f, width=8)
        self.ent_x2.insert(0, "9")
        self.ent_x2.grid(row=1, column=1, padx=4, pady=4)

        self.lbl_y2 = ttk.Label(grid_f, text="Y2:")
        self.lbl_y2.grid(row=1, column=2, sticky=tk.W, padx=4, pady=4)
        self.ent_y2 = ttk.Entry(grid_f, width=8)
        self.ent_y2.insert(0, "5")
        self.ent_y2.grid(row=1, column=3, padx=4, pady=4)

        btn_frame = ttk.Frame(coord_frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btn_frame, text="Построить", style="Accent.TButton", command=self.run_selected_algorithm).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4)
        )
        ttk.Button(btn_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Центрировать", command=self.reset_view).pack(side=tk.LEFT, padx=(4, 0))

        scale_frame = ttk.LabelFrame(left_panel, text=" Масштаб ", padding=10)
        scale_frame.pack(fill=tk.X, pady=(0, 10))

        scale_top = ttk.Frame(scale_frame)
        scale_top.pack(fill=tk.X)
        ttk.Label(scale_top, text="Размер клетки (px):").pack(side=tk.LEFT)
        self.lbl_scale_val = ttk.Label(scale_top, text="28 px", font=("Segoe UI", 10, "bold"))
        self.lbl_scale_val.pack(side=tk.RIGHT)

        self.scale_slider = ttk.Scale(
            scale_frame, from_=10, to=80, orient=tk.HORIZONTAL, command=self._on_scale_slider
        )
        self.scale_slider.set(self.cell_size)
        self.scale_slider.pack(fill=tk.X, pady=4)

        ttk.Checkbutton(
            scale_frame,
            text="Показывать идеальную геометрическую кривую (красным)",
            variable=self.show_ideal,
            command=self.redraw_canvas,
        ).pack(anchor=tk.W, pady=2)

        self.canvas = tk.Canvas(right_panel, bg="#ffffff", highlightthickness=1, highlightbackground="#bdc3c7")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        status_bar = ttk.Frame(right_panel)
        status_bar.pack(fill=tk.X, pady=(4, 0))
        self.lbl_cursor = ttk.Label(
            status_bar,
            text="Курсор: (0, 0) | ЛКМ — перемещение, колесико — масштаб",
            font=("Segoe UI", 9),
        )
        self.lbl_cursor.pack(side=tk.LEFT)

        self.canvas.bind("<Configure>", lambda e: self.redraw_canvas())
        self.canvas.bind("<ButtonPress-1>", self._on_pan_start)
        self.canvas.bind("<B1-Motion>", self._on_pan_move)
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind("<Button-4>", self._on_mouse_wheel)
        self.canvas.bind("<Button-5>", self._on_mouse_wheel)

    def _on_algo_change(self):
        is_circle = self.algo_var.get() == "bres_circle"
        if is_circle:
            self.lbl_x1.config(text="Центр Xc:")
            self.lbl_y1.config(text="Центр Yc:")
            self.lbl_x2.config(text="Радиус R:")
            self.ent_y2.config(state=tk.DISABLED)
        else:
            self.lbl_x1.config(text="X1:")
            self.lbl_y1.config(text="Y1:")
            self.lbl_x2.config(text="X2:")
            self.ent_y2.config(state=tk.NORMAL)
        self.run_selected_algorithm()

    def _on_scale_slider(self, val):
        self.cell_size = int(float(val))
        self.lbl_scale_val.config(text=f"{self.cell_size} px")
        self.redraw_canvas()

    def _on_mouse_wheel(self, event):
        if event.num == 4 or event.delta > 0:
            new_size = min(80, self.cell_size + 4)
        else:
            new_size = max(10, self.cell_size - 4)
        self.scale_slider.set(new_size)

    def _on_pan_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_pan_move(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.offset_x += dx
        self.offset_y += dy
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.redraw_canvas()

    def _on_mouse_move(self, event):
        gx, gy = self.screen_to_grid(event.x, event.y)
        self.lbl_cursor.config(
            text=f"Курсор: ({gx}, {gy}) | ЛКМ — перемещение, колесико — масштаб"
        )

    def reset_view(self):
        self.offset_x = 0
        self.offset_y = 0
        self.scale_slider.set(28)
        self.redraw_canvas()

    def clear_canvas(self):
        self.current_pixels = []
        self.ideal_shape = None
        self.redraw_canvas()

    def get_origin_screen(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx = (w // 2) + self.offset_x
        cy = (h // 2) + self.offset_y
        return cx, cy

    def grid_to_screen_center(self, gx: float, gy: float):
        ox, oy = self.get_origin_screen()
        sx = ox + gx * self.cell_size
        sy = oy - gy * self.cell_size
        return sx, sy

    def grid_to_cell_rect(self, gx: int, gy: int):
        cx, cy = self.grid_to_screen_center(gx, gy)
        half = self.cell_size / 2.0
        return cx - half, cy - half, cx + half, cy + half

    def screen_to_grid(self, sx: int, sy: int):
        ox, oy = self.get_origin_screen()
        gx = round((sx - ox) / self.cell_size)
        gy = round((oy - sy) / self.cell_size)
        return gx, gy

    def run_selected_algorithm(self):
        try:
            x1 = int(self.ent_x1.get())
            y1 = int(self.ent_y1.get())
            x2 = int(self.ent_x2.get())
            y2 = int(self.ent_y2.get()) if self.algo_var.get() != "bres_circle" else 0
        except ValueError:
            messagebox.showerror("Ошибка", "Координаты должны быть целыми числами")
            return

        algo = self.algo_var.get()
        if algo == "bres_circle" and x2 < 0:
            messagebox.showerror("Ошибка", "Радиус должен быть неотрицательным")
            return

        if algo == "step":
            pts, _ = step_by_step_line(x1, y1, x2, y2)
        elif algo == "dda":
            pts, _ = dda_line(x1, y1, x2, y2)
        elif algo == "bres_line":
            pts, _ = bresenham_line(x1, y1, x2, y2)
        elif algo == "bres_circle":
            pts, _ = bresenham_circle(x1, y1, x2)
        elif algo == "castle":
            pts, _ = castle_pitteway_line(x1, y1, x2, y2)
        elif algo == "wu":
            pts, _ = wu_line(x1, y1, x2, y2)
        else:
            pts = []

        self.current_pixels = pts
        if algo == "bres_circle":
            self.ideal_shape = ("circle", x1, y1, x2)
        else:
            self.ideal_shape = ("line", x1, y1, x2, y2)

        self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 10 or h <= 10:
            return

        ox, oy = self.get_origin_screen()
        cs = self.cell_size
        half = cs / 2.0

        min_gx = int((-ox) // cs) - 2
        max_gx = int((w - ox) // cs) + 2
        min_gy = int((oy - h) // cs) - 2
        max_gy = int(oy // cs) + 2

        # Отрисовка пикселей
        for gx, gy, intensity in self.current_pixels:
            x1, y1, x2, y2 = self.grid_to_cell_rect(gx, gy)
            r = int(255 - (255 - 31) * intensity)
            g = int(255 - (255 - 97) * intensity)
            b = int(255 - (255 - 141) * intensity)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

            if cs >= 24 and intensity >= 0.4:
                cx, cy = self.grid_to_screen_center(gx, gy)
                self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill="#ffffff", outline="")

        # Сетка
        for gx in range(min_gx, max_gx + 1):
            sx = ox + gx * cs - half
            self.canvas.create_line(sx, 0, sx, h, fill="#e2e8f0", width=1)

        for gy in range(min_gy, max_gy + 1):
            sy = oy - gy * cs - half
            self.canvas.create_line(0, sy, w, sy, fill="#e2e8f0", width=1)

        # Оси координат
        self.canvas.create_line(0, oy, w, oy, fill="#2c3e50", width=2, arrow=tk.LAST)
        self.canvas.create_line(ox, h, ox, 0, fill="#2c3e50", width=2, arrow=tk.LAST)

        self.canvas.create_text(w - 20, oy - 16, text="X", font=("Segoe UI", 11, "bold"), fill="#2c3e50")
        self.canvas.create_text(ox + 18, 16, text="Y", font=("Segoe UI", 11, "bold"), fill="#2c3e50")

        # Разметка осей
        label_step = 1 if cs >= 22 else (2 if cs >= 14 else 5)
        for gx in range(min_gx, max_gx + 1):
            if gx % label_step == 0:
                cx, _ = self.grid_to_screen_center(gx, 0)
                self.canvas.create_line(cx, oy - 4, cx, oy + 4, fill="#2c3e50", width=1)
                if gx != 0:
                    self.canvas.create_text(
                        cx, oy + 14, text=str(gx), font=("Segoe UI", 8), fill="#34495e"
                    )

        for gy in range(min_gy, max_gy + 1):
            if gy % label_step == 0:
                _, cy = self.grid_to_screen_center(0, gy)
                self.canvas.create_line(ox - 4, cy, ox + 4, cy, fill="#2c3e50", width=1)
                if gy != 0:
                    self.canvas.create_text(
                        ox - 16, cy, text=str(gy), font=("Segoe UI", 8), fill="#34495e"
                    )

        self.canvas.create_text(ox - 10, oy + 12, text="0", font=("Segoe UI", 8, "bold"), fill="#2c3e50")

        # Идеальная фигура
        if self.show_ideal.get() and self.ideal_shape:
            if self.ideal_shape[0] == "line":
                _, x1, y1, x2, y2 = self.ideal_shape
                sx1, sy1 = self.grid_to_screen_center(x1, y1)
                sx2, sy2 = self.grid_to_screen_center(x2, y2)
                self.canvas.create_line(sx1, sy1, sx2, sy2, fill="#e74c3c", width=2, dash=(5, 3))
                self.canvas.create_oval(sx1 - 4, sy1 - 4, sx1 + 4, sy1 + 4, fill="#e74c3c", outline="#ffffff")
                self.canvas.create_oval(sx2 - 4, sy2 - 4, sx2 + 4, sy2 + 4, fill="#e74c3c", outline="#ffffff")
            elif self.ideal_shape[0] == "circle":
                _, xc, yc, r = self.ideal_shape
                c_sx, c_sy = self.grid_to_screen_center(xc, yc)
                r_px = r * cs
                self.canvas.create_oval(
                    c_sx - r_px, c_sy - r_px, c_sx + r_px, c_sy + r_px, outline="#e74c3c", width=2, dash=(5, 3)
                )
                self.canvas.create_oval(c_sx - 4, c_sy - 4, c_sx + 4, c_sy + 4, fill="#e74c3c", outline="#ffffff")