import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import sys
import ctypes
import logging
from db_config import get_connection 
from utils import verify_password,set_window_icon,resource_path
from dashboard import open_user_dashboard
from admin_dashboard import open_admin_dashboard
from mysql.connector import Error

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def try_load_libmysql():
    if os.name != "nt":
        return
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    dll_path = os.path.join(base, "libmysql.dll")
    if os.path.isfile(dll_path):
        try:
            ctypes.WinDLL(dll_path)
            log.info("Loaded libmysql.dll from %s", dll_path)
        except Exception as e:
            log.warning("Failed to load libmysql.dll: %s", e)

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Omkar Optics Login Page")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        set_window_icon(self.root)
        self.username_entry = None
        self.password_entry = None
        self.toggle_btn = None
        self.bg_img = None

        try_load_libmysql()
        self.setup_ui()

    def setup_ui(self):
        try:
            img_path = resource_path("Bg1.png")
            img = Image.open(img_path).resize((500, 500), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.bg_img, bg="white").grid(row=0, column=0)
        except Exception as e:
            log.warning("Background image not loaded: %s", e)
            tk.Label(self.root, text="Background image not found", bg="white", fg="red").grid(row=0, column=0)

        # Frame for login
        frame = tk.Frame(self.root, bg="#D9D9D9", height=350, width=320)
        frame.grid(row=0, column=1, padx=40)

        tk.Label(frame, text="Welcome Back!\nLogin to Account", fg="black", bg="#D9D9D9",
                 font=("", 18, "bold")).grid(row=0, column=0, sticky="nw", pady=30, padx=10)

        # Username
        tk.Label(frame, text="Username", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(row=1, column=0, sticky="w", padx=30)
        self.username_entry = tk.Entry(frame, fg="black", bg="white", font=("", 16, "bold"), width=20)
        self.username_entry.grid(row=2, column=0, sticky="nwe", padx=30)
        self.username_entry.focus()  # Auto-focus

        # Password Label
        tk.Label(frame, text="Password", fg="black", bg="#D9D9D9", font=("", 12, "bold")).grid(
            row=3, column=0, sticky="w", padx=30, pady=(10, 0)
        )

        # Password Entry + Toggle Button inside one frame
        password_frame = tk.Frame(frame, bg="#D9D9D9")
        password_frame.grid(row=4, column=0, sticky="w", padx=30, pady=5)

        self.password_entry = tk.Entry(password_frame, fg="black", bg="white", font=("", 16, "bold"),
                                       width=15, show="*")
        self.password_entry.pack(side="left", fill="x", expand=True)

        self.toggle_btn = tk.Button(password_frame, text='Show', command=self.toggle_password,
                                    bg="white", fg="black", font=("", 10), relief="flat")
        self.toggle_btn.pack(side="left", padx=(5, 0))

        tk.Button(frame, text="Login", font=("", 16, "bold"), height=1, width=10, bg="#0085FF", fg="white",
                  cursor="hand2", command=self.login_user).grid(row=5, column=0, sticky="ne", pady=20, padx=35)

    def toggle_password(self):
        # If currently hidden (show == '*'), then show plaintext; else hide.
        current = self.password_entry.cget('show')
        if current == '':
            # currently visible -> hide
            self.password_entry.config(show='*')
            self.toggle_btn.config(text='Show')
        else:
            # currently hidden -> show
            self.password_entry.config(show='')
            self.toggle_btn.config(text='Hide')

    def login_user(self):
        username = (self.username_entry.get() or "").strip()
        password = (self.password_entry.get() or "").strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            # mysql.connector cursors typically don't support "with", so manage explicitly
            cursor = conn.cursor(buffered=True)
            cursor.execute("SELECT password, type, failed_attempts, last_failed_login FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if not user:
                messagebox.showerror("Error", "Invalid username or password")
                return

            stored_password, user_type, failed_attempts, last_failed_login = user
            failed_attempts = failed_attempts or 0

            if failed_attempts >= 5:
                messagebox.showerror("Account Locked", "Too many failed login attempts. Please contact admin.")
                return

            # Use stored_password variable (not user[0]) for clarity
            if verify_password(password, stored_password):
                cursor.execute("UPDATE users SET failed_attempts = 0, last_failed_login = NULL WHERE username = %s", (username,))
                conn.commit()
                messagebox.showinfo("Success", "Login successful. Redirecting...")
                # Close the window and open dashboard
                try:
                    self.root.destroy()
                except Exception:
                    pass

                if user_type == "admin":
                    open_admin_dashboard()
                else:
                    open_user_dashboard()
            else:
                # increment failed attempts and set last_failed_login to current time
                cursor.execute("""
                    UPDATE users 
                    SET failed_attempts = failed_attempts + 1, last_failed_login = NOW() 
                    WHERE username = %s
                """, (username,))
                conn.commit()
                remaining = max(0, 5 - (failed_attempts + 1))
                messagebox.showerror("Error", f"Invalid credentials. {remaining} attempt(s) left.")
        except Error as e:
            log.exception("Database error during login:")
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        except Exception as ex:
            log.exception("Unexpected error during login:")
            messagebox.showerror("Error", f"Unexpected error: {ex}")
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass
            try:
                if conn is not None and getattr(conn, "is_connected", lambda: False)():
                    conn.close()
            except Exception:
                pass

def launch_login():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

def show_splash_and_launch_login():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)

    width, height = 400, 200
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    splash_root.geometry(f"{width}x{height}+{x}+{y}")
    splash_root.configure(bg="white")

    tk.Label(splash_root, text="Loading Omkar Optics Software...", font=("Helvetica", 16, "bold"), bg="white").pack(pady=40)

    progress = ttk.Progressbar(splash_root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    def load_progress(value=0):
        if value <= 100:
            progress['value'] = value
            splash_root.after(50, load_progress, value + 5)
        else:
            splash_root.destroy()
            try:
                launch_login()
            except Exception as e:
                messagebox.showerror("Startup Error", f"Failed to launch application: {e}")

    splash_root.after(100, load_progress)
    splash_root.mainloop()

if __name__ == "__main__":
    show_splash_and_launch_login()
