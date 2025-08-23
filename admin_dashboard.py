import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import Error, IntegrityError
from datetime import datetime
from db_config import get_connection
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
from matplotlib.dates import DateFormatter
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dateutil.relativedelta import relativedelta
import logging
logging.getLogger('mysql.connector').setLevel(logging.WARNING)

current_date = datetime.today().strftime('%Y-%m-%d')

class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Management")
        self.master.geometry("750x450")
        self.master.configure(bg='#f0f0f0')
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        self.create_styles()
        self.create_widgets()
        self.fetch_data()
        ttk.Button(self.master, text="Back to Login", command=self.back_to_login).pack(pady=10)

    def create_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TEntry", font=("Arial", 12))

    def close_app(self):
        self.master.destroy()

    def back_to_login(self):
        self.master.destroy()
        from login import launch_login
        launch_login()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(pady=10, fill='both', expand=True)

        # Add Stock Tab
        self.frame_add = ttk.Frame(notebook, padding=10)
        notebook.add(self.frame_add, text="Add Stock")

        self.entry_frame_add = self._create_labeled_entry(self.frame_add, "Frame:", 0)
        self.entry_type_add = self._create_labeled_entry(self.frame_add, "Type:", 1)
        self.entry_count_add = self._create_labeled_entry(self.frame_add, "Count:", 2)

        ttk.Button(self.frame_add, text="Add Stock", command=self.add_stock).grid(row=4, column=0, columnspan=2, pady=10)
        self.tree = self._create_treeview(self.frame_add, 5)

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

        fig, ax = plt.subplots(figsize=(10, 6))
        keys = sorted(daily_sales.keys())
        dates = [datetime.strptime(k, "%Y-%m-%d") for k in keys]
        values = [daily_sales[k] for k in keys]
        bars=ax.bar(dates, values)
        ax.set_title("Daily Sales")
        ax.set_ylabel("Amount")
        date_format = DateFormatter("%Y-%m-%d") 
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        fig.autofmt_xdate()
        ax.tick_params(axis='x', rotation=45)
        cursor = mplcursors.cursor(bars, hover=True)
        @cursor.connect("add")
        def on_add(sel):
            sel.annotation.set(text=f'Amount: {sel.target[1]:.2f}')
            sel.annotation.get_bbox_patch().set(alpha=0.9)
        self._show_chart(fig)
    
    def generate_monthly_sales(self):
        _, monthly_sales = self.fetch_sales_data()
        if not monthly_sales:
            messagebox.showinfo("Info", "No monthly sales data found.")
            return

        fig, ax = plt.subplots(figsize=(8, 4))
        keys = sorted(monthly_sales.keys())
        values = [monthly_sales[k] for k in keys]
        dates = [datetime.strptime(k, "%Y-%m") for k in keys]
        bars=ax.bar(dates, values, color='blue')
        ax.set_title("Monthly Sales")
        ax.set_ylabel("Amount")
        ax.tick_params(axis='x', rotation=45)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        fig.autofmt_xdate()
        cursor = mplcursors.cursor(bars, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            sel.annotation.set_text(f"Amount: {sel.target[1]:.2f}")
            sel.annotation.get_bbox_patch().set_alpha(0.9)
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
        top.protocol("WM_DELETE_WINDOW", on_close)

    def fetch_sales_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
            SELECT order_date, after_discount 
            FROM customers
            WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        """)
            data = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            return {}, {}
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn and conn.is_connected():
                conn.close()
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
                # Optional: Use logging instead of print for large projects
                pass
        return daily_sales, monthly_sales

    def _create_labeled_entry(self, parent, text, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky='w', padx=5, pady=5)
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def _create_treeview(self, parent, row, bind_select=False):
        columns = ("Frame", "Type", "Date", "Count")
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
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT frame, type, date, COUNT(*) AS count_per_date "
                "FROM stock_items WHERE customer_id IS NULL "
                "GROUP BY frame, type, date ORDER BY frame, type, date;"
            )
            rows = cursor.fetchall()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            return
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn and conn.is_connected():
                conn.close()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_stock(self):
        frame = self.entry_frame_add.get()
        type_ = self.entry_type_add.get()
        count = self.entry_count_add.get()
        if not (frame and type_ and count.isdigit()):
            messagebox.showerror("Input Error", "Please enter valid Frame, Type, and numeric Count.")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.callproc("add_stock_items", (frame, type_, int(count)))
            conn.commit()
            messagebox.showinfo("Success", "Stock added successfully.")
            self.fetch_data()
        except IntegrityError:
            messagebox.showerror("Duplicate Error", "Frame & Type combination already exists.")
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn and conn.is_connected():
                conn.close()

# Entry Point
def open_admin_dashboard():
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
