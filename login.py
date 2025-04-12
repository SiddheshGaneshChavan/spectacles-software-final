import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import time
from db_config import get_connection
from utils import verify_password
from dashboard import open_user_dashboard
from admin_dashboard import open_admin_dashboard
from mysql.connector import Error

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Omkar Optics Login Page")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Load background
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "Bg1.png")
        img = Image.open(img_path).resize((500, 500), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.bg_img).grid(row=0, column=0)

        # Frame for login
        frame = tk.Frame(self.root, bg="#D9D9D9", height=350, width=300)
        frame.grid(row=0, column=1, padx=40)

        tk.Label(frame, text="Welcome Back!\nLogin to Account", fg="black", bg="#D9D9D9",
                 font=("", 18, "bold")).grid(row=0, column=0, sticky="nw", pady=30, padx=10)

        # Username
        tk.Label(frame, text="Username", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(row=1, column=0, sticky="w", padx=30)
        self.username_entry = tk.Entry(frame, fg="black", bg="white", font=("", 16, "bold"), width=20)
        self.username_entry.grid(row=2, column=0, sticky="nwe", padx=30)

        # Password
        tk.Label(frame, text="Password", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(row=3, column=0, sticky="w", padx=30, pady=(10, 0))
        self.password_entry = tk.Entry(frame, fg="black", bg="white", font=("", 16, "bold"), width=20, show="*")
        self.password_entry.grid(row=4, column=0, sticky="nwe", padx=30, pady=5)

        # Toggle password
        self.toggle_btn = tk.Button(frame, text='Show', command=self.toggle_password, bg="white", fg="black", font=("", 10))
        self.toggle_btn.grid(row=4, column=1, sticky='w', pady=5)

        # Login Button
        tk.Button(frame, text="Login", font=("", 16, "bold"), height=1, width=10, bg="#0085FF", fg="white",
                  cursor="hand2", command=self.login_user).grid(row=5, column=0, sticky="ne", pady=20, padx=35)

    def toggle_password(self):
        show = self.password_entry.cget('show') == ''
        self.password_entry.config(show='*' if show else '')
        self.toggle_btn.config(text='Show' if show else 'Hide')

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT password, type FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()

            if user and verify_password(password, user[0]):
                messagebox.showinfo("Success", "Login successful. Redirecting...")
                time.sleep(1)
                self.root.destroy()
                if user[1] == "admin":
                    open_admin_dashboard()
                else:
                    open_user_dashboard()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Error as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

def launch_login():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

# Splash screen with progress bar
def show_splash_and_launch_login():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_root.geometry("400x200+500+250")
    splash_root.configure(bg="white")

    tk.Label(splash_root, text="Loading Omkar Optics Software...", font=("Helvetica", 16, "bold"), bg="white").pack(pady=40)
    
    progress = ttk.Progressbar(splash_root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    def load():
        for i in range(0, 101, 5):
            progress['value'] = i
            splash_root.update_idletasks()
            time.sleep(0.05)
        splash_root.destroy()
        launch_login()

    splash_root.after(100, load)
    splash_root.mainloop()


# --- Main Execution ---
if __name__ == "__main__":
    show_splash_and_launch_login()
