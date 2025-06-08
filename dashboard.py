import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from db_config import get_connection
from mysql.connector import IntegrityError,InterfaceError,Error
import gc

class UserDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("User Dashboard")
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", lambda e: self.master.attributes("-fullscreen", False))
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        self.frame_cache = None
        self.type_cache = {}
        self.setup_ui()
    
    def close_app(self):
        self.master.destroy()
        gc.collect()

    def parse_float(self,value):
        try:
            return float(value) if value else 0
        except ValueError:
            return 0

    def setup_ui(self):
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        tk.Label(self.master, text="Welcome to Omkar Optics Userdashboard", font=("Arial", 18)).grid(row=0, column=0, pady=10)

        notebook = ttk.Notebook(self.master)
        notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.tab1 = tk.Frame(notebook)
        self.tab2 = tk.Frame(notebook)
        self.tab3 = tk.Frame(notebook)
        notebook.add(self.tab1, text="Customer Details")
        notebook.add(self.tab2, text="Update Details")
        #notebook.add(self.tab3, text="Details of Spectacles")
        self.build_customer_tab()
        self.update_customer_tab()
        #self.details_spec_tab()

        tk.Button(self.master, text="Logout", font=("Arial", 12), bg="#0085FF", fg="white", command=self.logout).grid(row=2, column=0, pady=10)

    def build_labeled_entry(self, parent, text, row, column, readonly=False):
        tk.Label(parent, text=text, font=("Arial", 12)).grid(row=row, column=column * 2, padx=10, pady=5, sticky="w")
        entry = tk.Entry(parent, font=("Arial", 12), width=30)
        if readonly:
            entry.insert(0, "")
            entry.config(state="readonly")
        entry.grid(row=row, column=column * 2 + 1, padx=10, pady=5)
        return entry
    
    def get_options(self,column,frame=None):
        if frame:
            if frame in self.type_cache:
                return self.type_cache[frame]
        elif self.frame_cache is not None:
            return self.frame_cache
        with get_connection() as conn:
            cursor=conn.cursor()
            if frame:
                cursor.execute("SELECT DISTINCT Type FROM stock_items WHERE Frame = %s ", (frame,))
                result = [row[0] for row in cursor.fetchall()]
                self.type_cache[frame] = result
            else:
                cursor.execute(f"SELECT DISTINCT {column} FROM stock_items")
                result = [row[0] for row in cursor.fetchall()]
                self.frame_cache = result
        return result
    
    def update_type_options(self, event=None):
        selected_frame = self.frame_combobox.get()
        if selected_frame == "Select Frame":
            self.type_combobox["values"] = []
            self.type_combobox.set("Select Type")
            self.unique_combobox["values"] = []
            self.unique_combobox.set("Select Type First")
            return
        types = self.get_options("Type", frame=selected_frame)
        self.type_combobox["values"] = types
        self.type_combobox.set("Select Type")
    # Clear Unique No combobox
        self.unique_combobox["values"] = []
        self.unique_combobox.set("Select Type First")

    # Bind selection of type to update unique numbers
        self.type_combobox.bind("<<ComboboxSelected>>", self.update_unique_options)

    def update_unique_options(self, event=None):
        selected_frame = self.frame_combobox.get()
        selected_type = self.type_combobox.get()
        if selected_frame == "Select Frame" or selected_type == "Select Type":
            self.unique_combobox["values"] = []
            self.unique_combobox.set("Select Type First")
            return

        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                query = """
                SELECT unique_no FROM stock_items 
                WHERE frame = %s AND type = %s AND customer_id IS NULL
            """
                cursor.execute(query, (selected_frame, selected_type))
                unique_numbers = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            unique_numbers = []
            print("Error fetching unique_no:", e)

        if unique_numbers:
            self.unique_combobox["values"] = unique_numbers
            self.unique_combobox.set(unique_numbers[0])  # Or set to 'Select Unique No'
        else:
            self.unique_combobox["values"] = []
            self.unique_combobox.set("No Unique No Available")

    def refresh_data(self):
        self.frame_cache=None
        self.type_cache.clear()
        self.frame_combobox["values"] = self.get_options("Frame")
        self.frame_combobox.set("Select Frame")
        self.type_combobox.set("Select Type")
        self.unique_combobox.set("Select Frame and Type")
        self.type_combobox["values"] = []
        self.unique_combobox["values"] = []

    def build_table(self, tab):
        table_frame = tk.Frame(tab, bg="white")
        table_frame.grid(row=8, column=1, columnspan=3, padx=10, pady=10)

        headers = ["", "R.E", "", "", "L.E", "", ""]
        for col, text in enumerate(headers):
            tk.Label(table_frame, text=text, font=("Arial", 12, "bold"), bg="white", borderwidth=1, relief="solid").grid(row=0, column=col, sticky="nsew")

        sub_headers = ["SPH", "CYL", "AXIS", "SPH", "CYL", "AXIS"]
        for col, text in enumerate([""] + sub_headers):
            tk.Label(table_frame, text=text, font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=10).grid(row=1, column=col)

        row_labels = ["Distance", "Reading"]
        self.entries = []
        for row, label in enumerate(row_labels, start=2):
            tk.Label(table_frame, text=label, font=("Arial", 12), bg="white", borderwidth=1, relief="solid", width=10).grid(row=row, column=0)
            row_entries = []
            for col in range(1, 7):
                entry = tk.Entry(table_frame, font=("Arial", 12), width=10, justify="center", relief="solid", borderwidth=1)
                entry.grid(row=row, column=col, padx=0, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)
    
    def build_billing_fields(self, tab):
        self.total_amt = self.build_labeled_entry(tab, "Total Amount", 9, 0)
        self.discount = self.build_labeled_entry(tab, "Discount", 10, 0)
        self.after_discount = self.build_labeled_entry(tab, "After Discount", 10, 1, readonly=True)
        self.advance_amt = self.build_labeled_entry(tab, "Advance", 11, 0)
        self.balance_amt = self.build_labeled_entry(tab, "Balance", 11, 1, readonly=True)

        for field in [self.total_amt, self.discount, self.advance_amt]:
            field.bind("<KeyRelease>", self.calculate_balance)
    
    def calculate_balance(self, *args):
        total = self.parse_float(self.total_amt.get())
        discount = self.parse_float(self.discount.get())
        advance = self.parse_float(self.advance_amt.get())
        discounted = total - discount
        balance = discounted - advance

        self.after_discount.config(state="normal")
        self.after_discount.delete(0, tk.END)
        self.after_discount.insert(0, f"{discounted:.2f}")
        self.after_discount.config(state="readonly")

        self.balance_amt.config(state="normal")
        self.balance_amt.delete(0, tk.END)
        self.balance_amt.insert(0, f"{balance:.2f}")
        self.balance_amt.config(state="readonly")
      
    def insert_data(self):
        try:
            conn=get_connection()
            cursor=conn.cursor()
            name = self.name_entry.get().strip()
            phone_no = self.phone_entry.get().strip()
            bill_no = self.transaction.get().strip()
            order_date = self.date_entry.get()
            dob = self.dob_entry.get()
            lens = self.lens_entry.get().strip()
            remark = self.remark.get().strip()

            unique_no = self.unique_combobox.get().strip()
            unique_no_lens = None if lens else (unique_no if unique_no else None)

            total_amount = self.parse_float(self.total_amt.get())
            discount_amount = self.parse_float(self.after_discount.get())
            advance_amount = self.parse_float(self.advance_amt.get())
            balance_amount = self.parse_float(self.balance_amt.get())

            lens_value = lens if lens else None
            remark_value = remark if remark else None 

            re_sph_dist = self.parse_float(self.entries[0][0].get())
            re_cyl_dist = self.parse_float(self.entries[0][1].get())
            re_axis_dist = self.parse_float(self.entries[0][2].get())
            le_sph_dist = self.parse_float(self.entries[0][3].get())
            le_cyl_dist = self.parse_float(self.entries[0][4].get())
            le_axis_dist = self.parse_float(self.entries[0][5].get())

            re_sph_read = self.parse_float(self.entries[1][0].get())
            re_cyl_read = self.parse_float(self.entries[1][1].get())
            re_axis_read = self.parse_float(self.entries[1][2].get())
            le_sph_read = self.parse_float(self.entries[1][3].get())
            le_cyl_read = self.parse_float(self.entries[1][4].get())
            le_axis_read = self.parse_float(self.entries[1][5].get())


            if not (name and phone_no and bill_no and order_date and dob and total_amount is not None and discount_amount is not None and advance_amount is not None and balance_amount is not None):
                messagebox.showerror("Error", "All fields must be filled!")
                return
            
            if not (phone_no.isdigit() and len(phone_no)==10):
                messagebox.showerror("Invalid Phone Number", "Please enter a valid 10-digit phone number!")
                return
            payable_amount = total_amount - discount_amount
            balance_amount = payable_amount - advance_amount
            if total_amount < 0 or discount_amount < 0 or advance_amount < 0:
                messagebox.showerror("Invalid Input", "Amounts cannot be negative.")
                return
            
            if discount_amount > total_amount:
                messagebox.showerror("Invalid Discount", "Discount cannot exceed total amount.")
                return

            if advance_amount > payable_amount:
                messagebox.showerror("Invalid Advance", "Advance exceeds payable amount.")
                return
            
            if unique_no_lens:
                cursor.execute("SELECT COUNT(*) FROM stock_items WHERE unique_no = %s", (unique_no_lens,))
                if cursor.fetchone()[0] == 0:
                    messagebox.showerror("Stock Error", f"Selected stock unique_no '{unique_no_lens}' does not exist.")
                    return

            cursor.execute('''INSERT INTO customers (name, phone_no, bill_no, order_date, dob, stock_unique_no,total_amount, after_discount, advance_amount, balance_amount, Lens, remark) 
                           VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)''', ( name, phone_no, bill_no, order_date, dob, unique_no_lens, total_amount, discount_amount, advance_amount, balance_amount, lens_value, remark_value))
            customer_id = cursor.lastrowid
            if unique_no_lens:
                cursor.execute('''UPDATE stock_items SET customer_id = %s WHERE unique_no = %s''', (customer_id, unique_no_lens))
            cursor.execute('''INSERT INTO eye_prescriptions (customer_id, eye_type, re_sph, re_cyl, re_axis, le_sph, le_cyl, le_axis)
            VALUES (%s, 'Distance', %s, %s, %s, %s, %s, %s)''', 
            (customer_id, re_sph_dist, re_cyl_dist, re_axis_dist, le_sph_dist, le_cyl_dist, le_axis_dist))

            cursor.execute('''INSERT INTO eye_prescriptions (customer_id, eye_type, re_sph, re_cyl, re_axis, le_sph, le_cyl, le_axis)
            VALUES (%s, 'Reading', %s, %s, %s, %s, %s, %s)''', 
            (customer_id, re_sph_read, re_cyl_read, re_axis_read, le_sph_read, le_cyl_read, le_axis_read))
            conn.commit()
            messagebox.showinfo("Success", "Customer data inserted successfully.")
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.transaction.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.dob_entry.delete(0, tk.END)
            self.lens_entry.delete(0, tk.END)
            self.total_amt.delete(0, tk.END)
            self.discount.delete(0, tk.END)
            self.advance_amt.delete(0, tk.END)
            self.balance_amt.delete(0, tk.END)
            self.frame_combobox.set('')
            self.type_combobox.set('')
            self.unique_combobox.set('')
            self.remark.delete(0,tk.END)
            for row in self.entries:
                for entry in row:
                    entry.delete(0, tk.END)
            self.refresh_data()
        except ValueError as ve:
            messagebox.showerror("Invalid Input",f"{ve}")
        except IntegrityError as ie:
            messagebox.showerror("Database Error", f"Duplicate or invalid entry: {ie}")
        except InterfaceError:
            messagebox.showerror("Connection Error", "Could not connect to the database. Please check your settings.")
        except Error as db_err:
            messagebox.showerror("Database Error", f"An error occurred while accessing the database:\n{db_err}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"Something went wrong:\n{e}")
        finally:
            try:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
            except:
                pass

    def build_customer_tab(self):
        tab = self.tab1
        self.transaction = self.build_labeled_entry(tab, "Bill no", 0, 0)
        self.date_entry = self.build_labeled_entry(tab, "Date of Order", 1, 0, readonly=True)
        self.date_entry.config(state="normal")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.config(state="readonly")

        self.phone_entry = self.build_labeled_entry(tab, "Phone No", 2, 0)
        self.name_entry = self.build_labeled_entry(tab, "Name", 3, 0)

        tk.Label(tab, text="DOB:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.dob_entry = DateEntry(tab, font=("Arial", 12), width=28, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)

        # Frame Combobox
        tk.Label(tab, text="Frame:", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.frame_combobox = ttk.Combobox(tab, values=self.get_options("Frame"), font=("Arial", 12), width=28)
        self.frame_combobox.grid(row=5, column=1, padx=10, pady=5)
        self.frame_combobox.set("Select Frame")
        self.frame_combobox.bind("<<ComboboxSelected>>", self.update_type_options)
        
        tk.Label(tab, text="Unique No:", font=("Arial", 12)).grid(row=5, column=2, padx=10, pady=5, sticky="w")
        self.unique_combobox = ttk.Combobox(tab, font=("Arial", 12), width=28)
        self.unique_combobox.grid(row=5, column=3, padx=10, pady=5)
        self.unique_combobox.set("Select Type First")

        tk.Button(tab, text="Refresh Data", font=("Arial", 12), bg="white", command=self.refresh_data).grid(row=5, column=4, padx=10, pady=5)

        tk.Label(tab, text="Type:", font=("Arial", 12)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.type_combobox = ttk.Combobox(tab, values=["Select a Frame First"], font=("Arial", 12), width=28)
        self.type_combobox.grid(row=6, column=1, padx=10, pady=5)
        self.type_combobox.set("Select Type")
        
        self.lens_entry = self.build_labeled_entry(tab, "Lens", 7, 0)

        self.build_table(tab)
        self.build_billing_fields(tab)
        self.remark= self.build_labeled_entry(tab, "Remark", 12, 0)
        tk.Button(tab, text="Insert Customer Data", font=("Arial", 12), bg="green", fg="white", command=self.insert_data).grid(row=13, column=0, columnspan=2, padx=10, pady=5)
    
    def update_balance(self):
        selected_bill = self.frame_up_combobox.get()
        if not selected_bill:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance_amount, advance_amount FROM customers WHERE bill_no = %s", (selected_bill,))
        result = cursor.fetchone()

        if result:
            new_advance_amount = result[0] + result[1]  # balance_amt + advance_amt
            cursor.execute("UPDATE customers SET advance_amount = %s, balance_amount = 0, payment='Paid' WHERE bill_no = %s", (new_advance_amount, selected_bill))
            messagebox.showinfo("Payment Update", f"Bill No {selected_bill} has been marked as Paid.")
            conn.commit()

        conn.close()
        self.frame_up_combobox.set("")
        self.balance_up_amt.config(state="normal")
        self.balance_up_amt.delete(0, tk.END)
        self.balance_up_amt.config(state="readonly")
        self.load_customers()
    
    def fetch_bill_numbers(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT bill_no FROM customers where balance_amount!=0")
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result
    
    def on_bill_selected(self, event=None):
        selected_bill = self.frame_up_combobox.get()
        if not selected_bill:
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance_amount FROM customers WHERE bill_no = %s", (selected_bill,))
        result = cursor.fetchone()
        conn.close()

        if result:
            balance_amt = result[0]
            self.balance_up_amt.config(state="normal")
            self.balance_up_amt.delete(0, tk.END)
            self.balance_up_amt.insert(0, str(balance_amt))
            self.balance_up_amt.config(state="readonly")
        else:
            print(f"No balance found for Bill No {selected_bill}")

    def update_customer_tab(self):
        tab2 = self.tab2
        tk.Label(tab2, text="Bill No:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        bill_numbers = self.fetch_bill_numbers()
        self.frame_up_combobox = ttk.Combobox(tab2,values=bill_numbers,font=("Arial", 12), width=28)
        self.frame_up_combobox.grid(row=0, column=1, padx=10, pady=5)
        self.frame_up_combobox.bind("<<ComboboxSelected>>", self.on_bill_selected)

        tk.Button(tab2, text="Update Billno", font=("Arial", 12), bg="green", fg="white",command=self.update_balance).grid(row=0, column=3, columnspan=2, padx=10, pady=5)
        tk.Button(tab2, text="Refresh Button for Billno", font=("Arial", 12), bg="blue", fg="white",command=self.refresh_combobox2).grid(row=0, column=5, columnspan=2, padx=10, pady=5)

        self.balance_up_amt = self.build_labeled_entry(tab2, "Balance Amount", 1, 0, readonly=True)

        tree_frame = tk.Frame(tab2)
        tree_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
        tab2.grid_rowconfigure(2, weight=1)
        tab2.grid_columnconfigure(1, weight=1)

        columns = ("billno", "name", "phone", "balance")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        for col in columns: 
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
    
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.load_customers()

    def logout(self):
        self.master.destroy()
        gc.collect()
        import login
        login.launch_login()


def open_user_dashboard():
    root = tk.Tk()
    UserDashboard(root)
    root.mainloop()