import tkinter as tk
from tkinter import ttk

def apply_treeview_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=28,
                    fieldbackground="white",
                    font=("Calibri", 12))

    style.configure("Treeview.Heading",
                    background="#2b5797",
                    foreground="white",
                    font=("Calibri", 13, "bold"))

    style.map("Treeview",
              background=[("selected", "#4a90e2")],
              foreground=[("selected", "white")])

def apply_common_styles():
    style = ttk.Style()

    style.configure("TLabel", font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12), padding=5)
    style.configure("TEntry", font=("Arial", 12))