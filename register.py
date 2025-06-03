import tkinter as tk
from tkinter import messagebox, ttk
import bcrypt
from mysql.connector import connect, Error

# MySQL credentials — **EDIT THESE**
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'omkaroptics',
'port': 3360
}

def get_connection():
    return connect(**DB_CONFIG)

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

class RegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Register New User")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Register New Account", font=("", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(frame, text="Username:", bg="white", font=("", 12)).grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(frame, font=("", 12))
        self.username_entry.grid(row=1, column=1, pady=5)
        self.username_entry.focus()

        tk.Label(frame, text="Password:", bg="white", font=("", 12)).grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(frame, font=("", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Confirm Password:", bg="white", font=("", 12)).grid(row=3, column=0, sticky="e", pady=5)
        self.confirm_password_entry = tk.Entry(frame, font=("", 12), show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Account Type:", bg="white", font=("", 12)).grid(row=4, column=0, sticky="e", pady=5)
        self.type_combo = ttk.Combobox(frame, values=["user", "admin"], state="readonly", font=("", 12))
        self.type_combo.current(0)  # default to user
        self.type_combo.grid(row=4, column=1, pady=5)

        tk.Button(frame, text="Register", font=("", 14, "bold"), bg="#0085FF", fg="white",
                  command=self.register_user).grid(row=5, column=0, columnspan=2, pady=20)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        user_type = self.type_combo.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters.")
            return

        hashed_password = hash_password(password)

        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, password, type) VALUES (%s, %s, %s)",
                               (username, hashed_password, user_type))
            conn.commit()
            messagebox.showinfo("Success", f"User registered successfully as {user_type}! You can now log in.")
            self.root.destroy()
        except Error as e:
            if e.errno == 1062:  # Duplicate username error code
                messagebox.showerror("Error", "Username already exists. Please choose another.")
            else:
                messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

def launch_register():
    root = tk.Tk()
    app = RegisterApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_register()
