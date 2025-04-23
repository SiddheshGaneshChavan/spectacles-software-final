import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import IntegrityError, Error
from datetime import datetime
from db_config import get_connection
import gc
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dateutil.relativedelta import relativedelta

current_date = datetime.today().strftime('%Y-%m-%d')

class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Management")
        self.master.geometry("750x450")
        self.master.configure(bg='#f0f0f0')
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TEntry", font=("Arial", 12))

        self.create_widgets()
        self.fetch_data()
        ttk.Button(self.master, text="Back to Login", command=self.back_to_login).pack(pady=10)

    def close_app(self):
        self.master.destroy()
        gc.collect()

    def back_to_login(self):
        self.master.destroy()
        gc.collect()
        import login 
        login.launch_login()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(pady=10, fill='both', expand=True)

        # Add Stock Tab
        self.frame_add = ttk.Frame(notebook, padding=10)
        notebook.add(self.frame_add, text="Add Stock")

        self.entry_frame_add = self._create_labeled_entry(self.frame_add, "Frame:", 0)
        self.entry_type_add = self._create_labeled_entry(self.frame_add, "Type:", 1)
        self.entry_count_add = self._create_labeled_entry(self.frame_add, "Count:", 2)

        ttk.Label(self.frame_add, text="Date:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.entry_date_add = ttk.Entry(self.frame_add, width=30)
        self.entry_date_add.insert(0, current_date)
        self.entry_date_add.config(state="readonly")
        self.entry_date_add.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.frame_add, text="Add Stock", command=self.add_stock).grid(row=4, column=0, columnspan=2, pady=10)
        self.tree = self._create_treeview(self.frame_add, 5)

        # Update Stock Tab
        self.frame_update = ttk.Frame(notebook, padding=10)
        notebook.add(self.frame_update, text="Update Stock")

        self.entry_frame_update = self._create_labeled_entry(self.frame_update, "Frame:", 0)
        self.entry_type_update = self._create_labeled_entry(self.frame_update, "Type:", 1)
        self.entry_count_update = self._create_labeled_entry(self.frame_update, "Count:", 2)

        ttk.Label(self.frame_update, text="Date:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.entry_date_update = ttk.Entry(self.frame_update, width=30)
        self.entry_date_update.insert(0, current_date)
        self.entry_date_update.config(state="readonly")
        self.entry_date_update.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.frame_update, text="Update Stock", command=self.update_stock).grid(row=4, column=0, columnspan=2, pady=10)
        self.tree2 = self._create_treeview(self.frame_update, 5, bind_select=True)

        # Daily Sales Tab
        self.frame_daily_sales = ttk.Frame(notebook, padding=10)
        notebook.add(self.frame_daily_sales, text="Daily Sales")

        ttk.Label(self.frame_daily_sales, text="Generate Daily Sales Report", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.frame_daily_sales, text="Generate Report", command=self.generate_daily_sales).pack(pady=10)

        # Monthly Sales Tab
        self.frame_monthly_sales = ttk.Frame(notebook, padding=10)
        notebook.add(self.frame_monthly_sales, text="Monthly Sales")

        ttk.Label(self.frame_monthly_sales, text="Generate Monthly Sales Report", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.frame_monthly_sales, text="Generate Report", command=self.generate_monthly_sales).pack(pady=10)

    def generate_daily_sales(self):
        daily_sales, _ = self.fetch_sales_data()
        if not daily_sales:
            messagebox.showinfo("Info", "No daily sales data found.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        keys = sorted(daily_sales.keys())
        values = [daily_sales[k] for k in keys]
        ax.bar(keys, values)
        ax.set_title("Daily Sales")
        ax.set_ylabel("Amount")
        ax.tick_params(axis='x', rotation=45)

        self._show_chart(fig)

    def generate_monthly_sales(self):
        _, monthly_sales = self.fetch_sales_data()
        if not monthly_sales:
            messagebox.showinfo("Info", "No monthly sales data found.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        keys = sorted(monthly_sales.keys())
        values = [monthly_sales[k] for k in keys]
        ax.bar(keys, values, color='green')
        ax.set_title("Monthly Sales")
        ax.set_ylabel("Amount")
        ax.tick_params(axis='x', rotation=45)

        self._show_chart(fig)

    def _show_chart(self, fig):
        top = tk.Toplevel(self.master)
        top.title("Sales Chart")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        def on_close():
            plt.close(fig)
            top.destroy()
            gc.collect()

        top.protocol("WM_DELETE_WINDOW", on_close)

    def fetch_sales_data(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT order_date, total_amount FROM customers")
            data = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            return {}, {}
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

        del conn,cursor

        daily_sales = defaultdict(int)
        monthly_sales = defaultdict(int)

        today = datetime.today().date()
        seven_months_ago = (datetime.today() - relativedelta(months=7)).date()

        for date_obj, amount in data:
            try:
                if isinstance(date_obj, str):
                    date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
                elif isinstance(date_obj, datetime):
                    date_obj = date_obj.date()
                if seven_months_ago <= date_obj <= today:
                    daily_sales[date_obj.strftime("%Y-%m-%d")] += amount
                    monthly_sales[date_obj.strftime("%Y-%m")] += amount
            except Exception as e:
                print(f"Date format error: {e} for value {date_obj}")

        return daily_sales, monthly_sales

    def _create_labeled_entry(self, parent, text, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky='w', padx=5, pady=5)
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def _create_treeview(self, parent, row, bind_select=False):
        columns = ("No", "Frame", "Type", "Count", "Date")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.grid(row=row, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=row, column=2, sticky="ns")

        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(row, weight=1)

        if bind_select:
            tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        return tree

    def fetch_data(self):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stocks")
            rows = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

        for trv in [self.tree, self.tree2]:
            trv.delete(*trv.get_children())
            for row in rows:
                trv.insert("", "end", values=row)
        del conn,cursor

    def add_stock(self):
        frame = self.entry_frame_add.get()
        type_ = self.entry_type_add.get()
        count = self.entry_count_add.get()
        date = self.entry_date_add.get()

        if not (frame and type_ and count.isdigit()):
            messagebox.showerror("Input Error", "Please enter valid Frame, Type, and numeric Count.")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Stocks (Frame, Type, Count, Date) VALUES (%s, %s, %s, %s)",
                           (frame, type_, int(count), date))
            conn.commit()
            messagebox.showinfo("Success", "Stock added successfully.")
            self.fetch_data()
        except IntegrityError:
            messagebox.showerror("Duplicate Error", "Frame & Type combination already exists.")
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        del cursor,conn

    def update_stock(self):
        selected_item = self.tree2.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a record to update.")
            return

        frame = self.entry_frame_update.get()
        type_ = self.entry_type_update.get()
        count = self.entry_count_update.get()
        date = self.entry_date_update.get()

        if not (frame and type_ and count.isdigit()):
            messagebox.showerror("Input Error", "Please enter valid Frame, Type, and numeric Count.")
            return

        item_values = self.tree2.item(selected_item)["values"]
        stock_id = item_values[0]

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Stocks SET Frame=%s, Type=%s, Count=%s, Date=%s WHERE No=%s",
                           (frame, type_, int(count), date, stock_id))
            conn.commit()
            messagebox.showinfo("Success", "Stock updated successfully.")
            self.fetch_data()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        del conn,cursor

    def on_row_selected(self, event):
        selected_item = self.tree2.selection()
        if not selected_item:
            return

        item_values = self.tree2.item(selected_item)["values"]
        self.entry_frame_update.delete(0, tk.END)
        self.entry_frame_update.insert(0, item_values[1])
        self.entry_type_update.delete(0, tk.END)
        self.entry_type_update.insert(0, item_values[2])
        self.entry_count_update.delete(0, tk.END)
        self.entry_count_update.insert(0, item_values[3])


# Entry Point
def open_admin_dashboard():
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
