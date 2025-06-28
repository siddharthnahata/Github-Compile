import pandas as pd
import numpy as np
import os
from datetime import datetime
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry

class LedgerAgeingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ledger Standalsone Ledger.")
        master.geometry("800x600")
        master.resizable(False, False)

        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'{width}x{height}+{x}+{y}')

        self.main_frame = ttk.Frame(master)
        self.master.iconbitmap("favicon.ico")

        self.show_login_page()
        
    def show_login_page(self):
        self.login_window = tk.Toplevel(self.master)
        self.login_window.title("Login")
        self.login_window.geometry("300x200")
        self.login_window.transient(self.master)
        self.login_window.grab_set()

        self.login_window.update_idletasks()
        lw_width = self.login_window.winfo_width()
        lw_height = self.login_window.winfo_height()
        lw_x = self.master.winfo_x() + (self.master.winfo_width() // 2) - (lw_width // 2)
        lw_y = self.master.winfo_y() + (self.master.winfo_height() // 2) - (lw_height // 2)
        self.login_window.geometry(f'{lw_width}x{lw_height}+{lw_x}+{lw_y}')

        ttk.Label(self.login_window, text="Please Login to Continue", font=("Arial", 10, "bold")).pack(pady=10)

        ttk.Label(self.login_window, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_window, width=30)
        self.username_entry.pack(pady=5)
        self.username_entry.focus_set()

        ttk.Label(self.login_window, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_window, show="*", width=30)
        self.password_entry.pack(pady=5)

        ttk.Button(self.login_window, text="Login", command=self.attempt_login, width=15).pack(pady=1)
         
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self.attempt_login())

        self.login_window.protocol("WM_DELETE_WINDOW", self.on_login_close)
        self.login_window.iconbitmap("favicon.ico")

    def on_login_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.login_window.destroy()
            self.master.destroy()    

    def attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "admin" and password == "03011974":
            messagebox.showinfo("Login Successful", "Welcome to the Ledger Standalone Ledger!")
            self.login_window.destroy()
            self.show_main_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus_set()
    
    def show_main_page(self):
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.welcome_label = ttk.Label(self.main_frame, text="Ledger Standalone Ledger", font=("Arial", 16, "bold"))
        self.welcome_label.pack(pady=10)

        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=5, fill='x')

        ttk.Label(self.input_frame, text="Input Excel File Path (e.g., C:\\data\\ledger.xlsx):", wraplength=450).pack(anchor='w')
        self.input_file_entry = ttk.Entry(self.input_frame, width=60)
        self.input_file_entry.pack(side='left', fill='x', expand=True)
        self.browse_input_btn = ttk.Button(self.input_frame, text="Browse", command=self.browse_input_file)
        self.browse_input_btn.pack(side='right', padx=(5,0))

        self.output_folder_frame = ttk.Frame(self.main_frame)
        self.output_folder_frame.pack(pady=5, fill='x')

        ttk.Label(self.output_folder_frame, text="Output Folder Path (e.g., C:\\reports):", wraplength=450).pack(anchor='w')
        self.output_folder_entry = ttk.Entry(self.output_folder_frame, width=60)
        self.output_folder_entry.pack(side='left', fill='x', expand=True)
        self.browse_output_btn = ttk.Button(self.output_folder_frame, text="Browse", command=self.browse_output_folder)
        self.browse_output_btn.pack(side='right', padx=(5,0))

        self.output_file_frame = ttk.Frame(self.main_frame)
        self.output_file_frame.pack(pady=5, fill='x')

        ttk.Label(self.output_file_frame, text="Output Report File Name (without extension, e.g., Ageing_Report):", wraplength=450).pack(anchor='w')
        self.output_file_entry = ttk.Entry(self.output_file_frame, width=60)
        self.output_file_entry.pack(fill='x', expand=True)

        self.your_date_frame = ttk.Frame(self.main_frame)
        self.your_date_frame.pack(pady=5, fill='x')

        ttk.Label(self.your_date_frame, text="Select Date:").pack(pady=5)
        self.your_date_entry = DateEntry(self.your_date_frame, width=20, background='darkblue',
                        foreground='white', date_pattern='dd-mm-yyyy')
        self.your_date_entry.pack(pady=5)

        self.process_button = ttk.Button(self.main_frame, text="Generate Report", command=self.generate_report)
        self.process_button.pack(pady=20)

        self.status_label = ttk.Label(self.main_frame, text="", foreground="blue")
        self.status_label.pack(pady=5)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, file_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Save Report")
        if folder_path:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_path)

    
    def update_status(self, message, color="blue"):
        self.status_label.config(text=message, foreground=color)
        self.master.update_idletasks()


    def generate_report(self):
        self.update_status("Starting report generation...", "blue")

        input_file_path = self.input_file_entry.get().strip()
        output_folder_path = self.output_folder_entry.get().strip()
        output_file_name = self.output_file_entry.get().strip()

        # --- Validation ---
        if not input_file_path:
            self.update_status("Error: Input file path missing.", "red")
            return
        if not input_file_path.lower().endswith('.xlsx'): # Use .lower() for case-insensitivity
            self.update_status("Error: Invalid input file extension.", "red")
            return
        if not output_folder_path:
            self.update_status("Error: Output folder path missing.", "red")
            return
        if not os.path.isdir(output_folder_path):
            self.update_status("Error: Output folder invalid.", "red")
            return
        if not output_file_name:
            self.update_status("Error: Output file name missing.", "red")
            return
        
        df = pd.DataFrame()
        try:
            self.update_status("Loading Excel file...", "blue")
            df = pd.read_excel(input_file_path)
            self.update_status("File loaded successfully.", "green")
        except FileNotFoundError:
            self.update_status("Error: File not found.", "red")
            return
        except Exception as e:
            self.update_status("Error: Failed to load file.", "red")
            return
        
        df.columns = df.columns.str.strip()
        expected_columns = ['Date', 'Particulars', 'Vch Type', 'Vch No.', 'Debit', 'Credit']

        missing_columns = [col for col in expected_columns if col not in df.columns]

        if missing_columns:
            self.update_status(f"❌ Missing columns: {missing_columns}", "red")
            return
        else:
            self.update_status("✅ All required columns are present!")

        
        self.update_status("Performing Data Ageing Report Generation... This may take a moment.", "blue")
        
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception as e:
            self.update_status("Error: Date column format.", "red")
            return
        
        
        today_str = self.your_date_entry.get()
        today = pd.to_datetime(today_str, format='%d-%m-%Y')
        print(today)
        matched_rows = []

        purchase_df = df[df['Vch Type'] == 'Purchase'].copy()
        payments_df = df[df['Debit'] > 0].copy()
        
        purchase_df['Remaining'] = purchase_df['Credit']
        payments_df['Remaining'] = payments_df['Debit']

        for pi, prow in purchase_df.iterrows():
            purchase_date = prow['Date']
            remaining_amount = prow['Credit']

            for bi,brow in payments_df.iterrows():
                payment_date = brow['Date']
                remaining_balance = payments_df.at[bi, 'Remaining']

                if remaining_balance <= 0:
                    continue

                used_amount = min(remaining_amount, remaining_balance)
                match_type = 'Advance' if payment_date < purchase_date else 'Post Purchase'

                matched_rows.append({
                    'Puchase Date': purchase_date, 
                    'Payment Date': payment_date,
                    'Vch No.': prow['Vch No.'],
                    'Days Taken': abs((payment_date - purchase_date).days),
                    'Payment Vch Type': brow['Vch Type'],
                    'Amount': used_amount,
                    'Type': match_type
                })

                remaining_amount -= used_amount
                payments_df.at[bi, 'Remaining'] -= used_amount

                if remaining_amount <= 0:
                    break
            
            if remaining_amount > 0:
                matched_rows.append({
                    'Puchase Date': purchase_date, 
                    'Payment Date': "NA",
                    'Vch No.': prow['Vch No.'],
                    'Days Taken': abs((today - purchase_date).days),
                    'Payment Vch Type': "NA",
                    'Amount': remaining_amount,
                    'Type': 'Unpaid'
                })

            
        def ageing_category(days):
            if pd.isna(days): 
                return 'N/A'
            days = int(days) 
            if days <= 45:
                return '0-45 Days'
            elif days <= 180:
                return '46-180 Days'
            else:
                return '180+ Days'
            
        ageing_df = pd.DataFrame(matched_rows)
        
        ageing_df['Days Taken'] = pd.to_numeric(ageing_df['Days Taken'], errors='coerce')
        ageing_df['Ageing Category'] = ageing_df['Days Taken'].apply(ageing_category)

        ageing_df['Puchase Date'] = pd.to_datetime(ageing_df['Puchase Date']).dt.strftime('%d-%m-%Y')
        ageing_df['Payment Date'] = pd.to_datetime(ageing_df['Payment Date'], errors='coerce').dt.strftime('%d-%m-%Y')

        advance_pay = ageing_df[ageing_df['Type'] == 'Advance']
        post_pay = ageing_df[ageing_df['Type'] == 'Post Purchase']
        unpaid = ageing_df[ageing_df['Type'] == 'Unpaid']

        advance_pay.drop(columns=['Ageing Category'], inplace=True, errors='ignore')

        self.update_status("Matching complete. Preparing the ageing report...", "blue")

        save_path = os.path.join(output_folder_path, f"{output_file_name}.xlsx")

        try:
            with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
                advance_pay.to_excel(writer, sheet_name='Adavance Payments', index=False)
                post_pay.to_excel(writer, sheet_name='Post Payments', index=False)
                unpaid.to_excel(writer, sheet_name='Unpaid', index=False)
            messagebox.showinfo("Success", f"Ageing report saved successfully at:\n{save_path}")
            self.update_status("Report generated and saved successfully!", "green")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving report: {e}\nPlease check the path and file name, and ensure the file is not open.")
            self.update_status("Error: Failed to save report.", "red")

if __name__ == "__main__":
    root = tk.Tk()
    app = LedgerAgeingGUI(root)
    root.mainloop()