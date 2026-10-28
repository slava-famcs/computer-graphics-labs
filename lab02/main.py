import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from histogram_ops import (
    calculate_histogram,
    linear_contrast,
    equalize_histogram_rgb,
    equalize_histogram_hsv
)
from lowpass_filters import box_blur, gaussian_blur


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x800')
        self.root.minsize(900, 650)

        self.original_image = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        btn_load = ttk.Button(control_frame, text='Загрузить изображение', command=self.load_image)
        btn_load.pack(side=tk.LEFT, padx=5)

        btn_reset = ttk.Button(control_frame, text='Сбросить', command=self.reset_image)
        btn_reset.pack(side=tk.LEFT, padx=5)

        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        contrast_frame = ttk.LabelFrame(control_frame, text='Гистограмма и контраст', padding=5)
        contrast_frame.pack(side=tk.LEFT, padx=5)

        ttk.Button(contrast_frame, text='Линейное контрастирование', command=self.apply_linear_contrast).pack(side=tk.LEFT, padx=3)
        ttk.Button(contrast_frame, text='Эквализация RGB', command=self.apply_equalize_rgb).pack(side=tk.LEFT, padx=3)
        ttk.Button(contrast_frame, text='Эквализация HSV (V)', command=self.apply_equalize_hsv).pack(side=tk.LEFT, padx=3)

        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        filter_frame = ttk.LabelFrame(control_frame, text='Низкочастотные фильтры', padding=5)
        filter_frame.pack(side=tk.LEFT, padx=5)

        ttk.Label(filter_frame, text='Ядро:').pack(side=tk.LEFT, padx=2)
        self.kernel_size_var = tk.IntVar(value=3)
        kernel_combo = ttk.Combobox(filter_frame, textvariable=self.kernel_size_var, values=[3, 5, 7, 9], width=3, state='readonly')
        kernel_combo.pack(side=tk.LEFT, padx=2)

        ttk.Label(filter_frame, text='Sigma:').pack(side=tk.LEFT, padx=2)
        self.sigma_var = tk.DoubleVar(value=1.0)
        sigma_entry = ttk.Entry(filter_frame, textvariable=self.sigma_var, width=5)
        sigma_entry.pack(side=tk.LEFT, padx=2)

        ttk.Button(filter_frame, text='Усредняющий фильтр', command=self.apply_box_blur).pack(side=tk.LEFT, padx=3)
        ttk.Button(filter_frame, text='Фильтр Гаусса', command=self.apply_gaussian_blur).pack(side=tk.LEFT, padx=3)

        content_pane = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        content_pane.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        images_frame = ttk.Frame(content_pane)
        content_pane.add(images_frame, weight=3)

        self.orig_canvas_frame = ttk.LabelFrame(images_frame, text='Исходное изображение')
        self.orig_canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.orig_label = ttk.Label(self.orig_canvas_frame)
        self.orig_label.pack(fill=tk.BOTH, expand=True)

        self.proc_canvas_frame = ttk.LabelFrame(images_frame, text='Обработанное изображение')
        self.proc_canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.proc_label = ttk.Label(self.proc_canvas_frame)
        self.proc_label.pack(fill=tk.BOTH, expand=True)

        hist_frame = ttk.LabelFrame(content_pane, text='Гистограммы')
        content_pane.add(hist_frame, weight=2)

        self.fig = Figure(figsize=(8, 2.5), dpi=100)
        self.ax_orig = self.fig.add_subplot(121)
        self.ax_proc = self.fig.add_subplot(122)
        self.fig.tight_layout(pad=2.0)

        self.canvas_hist = FigureCanvasTkAgg(self.fig, master=hist_frame)
        self.canvas_hist.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Изображения', '*.png;*.jpg;*.jpeg;*.bmp;*.tiff'), ('Все файлы', '*.*')]
        )
        if not file_path:
            return

        img = Image.open(file_path).convert('RGB')
        self.original_image = np.array(img, dtype=np.uint8)
        self.processed_image = self.original_image.copy()

        self.update_display()

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.update_display()

    def apply_linear_contrast(self):
        if self.original_image is None:
            return
        self.processed_image = linear_contrast(self.original_image)
        self.update_display()

    def apply_equalize_rgb(self):
        if self.original_image is None:
            return
        self.processed_image = equalize_histogram_rgb(self.original_image)
        self.update_display()

    def apply_equalize_hsv(self):
        if self.original_image is None:
            return
        self.processed_image = equalize_histogram_hsv(self.original_image)
        self.update_display()

    def apply_box_blur(self):
        if self.original_image is None:
            return
        size = self.kernel_size_var.get()
        self.processed_image = box_blur(self.original_image, size=size)
        self.update_display()

    def apply_gaussian_blur(self):
        if self.original_image is None:
            return
        size = self.kernel_size_var.get()
        try:
            sigma = float(self.sigma_var.get())
        except ValueError:
            sigma = 1.0
        self.processed_image = gaussian_blur(self.original_image, size=size, sigma=sigma)
        self.update_display()

    def update_display(self):
        if self.original_image is None:
            return

        self.display_image_on_label(self.original_image, self.orig_label, self.orig_canvas_frame)
        self.display_image_on_label(self.processed_image, self.proc_label, self.proc_canvas_frame)
        self.update_histograms()

    def display_image_on_label(self, img_array, label, parent_frame):
        max_w = parent_frame.winfo_width()
        max_h = parent_frame.winfo_height()

        if max_w <= 10 or max_h <= 10:
            max_w, max_h = 400, 300

        img = Image.fromarray(img_array)
        img.thumbnail((max_w - 20, max_h - 20))
        photo = ImageTk.PhotoImage(img)

        label.configure(image=photo)
        label.image = photo

    def update_histograms(self):
        self.ax_orig.clear()
        self.ax_proc.clear()

        colors = ('r', 'g', 'b')

        for i, col in enumerate(colors):
            hist_orig = calculate_histogram(self.original_image[:, :, i])
            self.ax_orig.plot(hist_orig, color=col, alpha=0.8)

            hist_proc = calculate_histogram(self.processed_image[:, :, i])
            self.ax_proc.plot(hist_proc, color=col, alpha=0.8)

        self.ax_orig.set_title('Исходная гистограмма (RGB)')
        self.ax_orig.set_xlim([0, 256])

        self.ax_proc.set_title('Обработанная гистограмма (RGB)')
        self.ax_proc.set_xlim([0, 256])

        self.fig.tight_layout(pad=1.5)
        self.canvas_hist.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
