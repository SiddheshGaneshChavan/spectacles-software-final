import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import IntegrityError, Error  # 🔧 Added general `Error` import
import datetime
from collections import defaultdict
from db_config import get_connection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

current_date = datetime.datetime.today().strftime('%Y-%m-%d')


class AdminDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Management")
        self.master.geometry("750x450")
        self.master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TEntry", font=("Arial", 12))

        self.create_widgets()
        self.fetch_data()
        ttk.Button(self.master, text="Back to Login", command=self.back_to_login).pack(pady=10)
  
  
    def back_to_login(self):
        self.master.destroy()
        import login 
        login.launch_login()

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(pady=10, fill='both', expand=True)

        # --- Add Stock Tab ---
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

        # --- Update Stock Tab ---
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
                # --- Monthly ---
        self.monthly = ttk.Frame(notebook, padding=10)
        notebook.add(self.monthly, text="Monthly Sales")

        self.daily = ttk.Frame(notebook, padding=10)
        notebook.add(self.daily, text="Daily Sales")
        self.load_sales_charts()

    def fetch_sales_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT order_date, total_amount FROM customers")
        data = cursor.fetchall()
        conn.close()

        daily_sales = defaultdict(int)
        monthly_sales = defaultdict(int)

        for date_obj, amount in data:
            try: 
                daily_key = date_obj.strftime("%Y-%m-%d")
                monthly_key = date_obj.strftime("%Y-%m")
                daily_sales[daily_key] += amount
                monthly_sales[monthly_key] += amount
            except Exception as e:
                print(f"Date format error: {e} for value {date_obj}")
        
        return daily_sales, monthly_sales
    

    def load_sales_charts(self):
        daily_sales, monthly_sales = self.fetch_sales_data()
        daily_fig, ax1 = plt.subplots(figsize=(9, 4))
        daily_dates = list(daily_sales.keys())
        daily_totals = list(daily_sales.values())
        ax1.plot(daily_dates, daily_totals, marker='o', linestyle='-', color='green')
        ax1.set_title('Daily Sales')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Total Sales (₹)')
        ax1.tick_params(axis='x', rotation=45)

        daily_canvas = FigureCanvasTkAgg(daily_fig, master=self.daily)
        daily_canvas.draw()
        daily_canvas.get_tk_widget().pack(fill='both', expand=True)

        # --- Monthly Sales Chart ---
        monthly_fig, ax2 = plt.subplots(figsize=(9, 4))
        monthly_labels = list(monthly_sales.keys())
        monthly_totals = list(monthly_sales.values())
        ax2.bar(monthly_labels, monthly_totals, color='skyblue')
        ax2.set_title('Monthly Sales')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Total Sales (₹)')
        ax2.tick_params(axis='x', rotation=45)

        monthly_canvas = FigureCanvasTkAgg(monthly_fig, master=self.monthly)
        monthly_canvas.draw()
        monthly_canvas.get_tk_widget().pack(fill='both', expand=True)


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
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Stocks")
            rows = cursor.fetchall()
        except Error as e:  # 🔧 Gracefully handle DB errors
            messagebox.showerror("Database Error", str(e))
            return
        finally:
            if conn and conn.is_connected():
                conn.close()

        for trv in [self.tree, self.tree2]:
            trv.delete(*trv.get_children())
            for row in rows:
                trv.insert("", "end", values=row)

    def add_stock(self):
        frame = self.entry_frame_add.get()
        type_ = self.entry_type_add.get()
        count = self.entry_count_add.get()
        date = self.entry_date_add.get()

        if not (frame and type_ and count.isdigit()):
            messagebox.showerror("Input Error", "Please enter valid Frame, Type, and numeric Count.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Stocks (Frame, Type, Count, Date) VALUES (%s, %s, %s, %s)",
                           (frame, type_, int(count), date))
            conn.commit()
            if cursor.rowcount>0:
                messagebox.showinfo("Success","Stock added successfully.")
            else:
                messagebox.showwarning("Warning","No stock was added.")
            self.fetch_data()
        except IntegrityError:
            messagebox.showerror("Duplicate Error", "Frame & Type combination already exists.")
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()
            self.fetch_data()

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

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Stocks SET Frame=%s, Type=%s, Count=%s, Date=%s WHERE No=%s",
                           (frame, type_, int(count), date, stock_id))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Stock updated successfully.")
            else:
                messagebox.showwarning("Warning", "No changes were made.")
            self.fetch_data()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn and conn.is_connected():
                conn.close()
            self.fetch_data()

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
