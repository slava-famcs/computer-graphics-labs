import tkinter as tk
from ui import RasterizerApp


def main():
    root = tk.Tk()
    app = RasterizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()