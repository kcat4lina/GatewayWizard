import os
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
import time
import zipfile
import stat

class DataDeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gateway Wizard .69 © Jojo")
        self.set_dark_theme()

        # Initialize UI components
        self.label_src = tk.Label(root, text="Enter the source path to monitor:")
        self.label_src.pack(pady=10)

        self.path_entry_src = tk.Entry(root, width=50, bg="#1e1e1e", fg="#ffffff", insertbackground='white')
        self.path_entry_src.pack(pady=5)

        self.label_dest = tk.Label(root, text="Enter the destination path:")
        self.label_dest.pack(pady=10)

        self.path_entry_dest = tk.Entry(root, width=50, bg="#1e1e1e", fg="#ffffff", insertbackground='white')
        self.path_entry_dest.pack(pady=5)

        # Checkboxes for actions
        self.copy_var = tk.BooleanVar(value=False)
        self.delete_var = tk.BooleanVar(value=False)
        self.backup_var = tk.BooleanVar(value=False)  # Backup checkbox

        self.copy_check = tk.Checkbutton(root, text="Copy files", variable=self.copy_var, bg="#2e2e2e", fg="#ffffff", selectcolor="#3a3a3a", activebackground="#3a3a3a", font=("Arial", 12))
        self.copy_check.pack(pady=5)

        self.delete_check = tk.Checkbutton(root, text="Delete files", variable=self.delete_var, bg="#2e2e2e", fg="#ffffff", selectcolor="#3a3a3a", activebackground="#3a3a3a", font=("Arial", 12))
        self.delete_check.pack(pady=5)

        self.backup_check = tk.Checkbutton(root, text="Create Backup", variable=self.backup_var, bg="#2e2e2e", fg="#ffffff", selectcolor="#3a3a3a", activebackground="#3a3a3a", font=("Arial", 12))
        self.backup_check.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring, bg="#4CAF50", fg="#ffffff", relief=tk.RAISED, height=2, width=20, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED, bg="#F44336", fg="#ffffff", relief=tk.RAISED, height=2, width=20, font=("Arial", 12))
        self.stop_button.pack(pady=10)

        self.backup_button = tk.Button(root, text="Open Backup Folder", command=self.open_backup_folder, state=tk.DISABLED, bg="#2196F3", fg="#ffffff", relief=tk.RAISED, height=2, width=20, font=("Arial", 12))
        self.backup_button.pack(pady=10)

        self.status_label = tk.Label(root, text="Items processed: 0", bg="#2e2e2e", fg="#ffffff", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.output_text = tk.Text(root, height=10, width=60, bg="#1e1e1e", fg="#ffffff", insertbackground='white', wrap=tk.WORD, font=("Arial", 12))
        self.output_text.pack(pady=10)

        self.monitoring = False
        self.path_src = ""
        self.path_dest = ""
        self.backup_created = False  # Flag to ensure only one backup is created per start

    def set_dark_theme(self):
        self.root.configure(bg="#2e2e2e")
        self.root.option_add("*Font", "Arial 12")
        self.root.option_add("*Button.BorderWidth", 2)
        self.root.option_add("*Button.relief", "raised")
        self.root.option_add("*Checkbutton.Background", "#2e2e2e")
        self.root.option_add("*Checkbutton.Foreground", "#ffffff")
        self.root.option_add("*Checkbutton.SelectColor", "#3a3a3a")
        self.root.option_add("*Checkbutton.ActiveBackground", "#3a3a3a")
        self.root.option_add("*Text.Background", "#1e1e1e")
        self.root.option_add("*Text.Foreground", "#ffffff")

    def start_monitoring(self):
        if self.monitoring:
            return

        self.path_src = self.path_entry_src.get()
        self.path_dest = self.path_entry_dest.get()

        if not self.path_src:
            messagebox.showwarning("Input Error", "Please enter the source path.")
            return

        if not os.path.exists(self.path_src):
            messagebox.showwarning("Invalid Source Path", "The specified source path does not exist.")
            return

        if self.copy_var.get() and not self.path_dest:
            messagebox.showwarning("Input Error", "Please enter the destination path for copying data.")
            return

        self.disable_checkboxes(True)
        self.monitoring = True
        self.backup_created = False  # Reset the backup flag
        self.thread = Thread(target=self.monitor_path)
        self.thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.backup_button.config(state=tk.NORMAL)  # Enable the backup button

    def stop_monitoring(self):
        self.monitoring = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.disable_checkboxes(False)
        self.backup_button.config(state=tk.DISABLED)  # Disable the backup button
        if hasattr(self, 'thread'):
            self.thread.join()

    def disable_checkboxes(self, disable):
        state = tk.DISABLED if disable else tk.NORMAL
        self.copy_check.config(state=state)
        self.delete_check.config(state=state)
        self.backup_check.config(state=state)  # Disable the backup checkbox

    def monitor_path(self):
        while self.monitoring:
            if os.path.exists(self.path_src):
                if self.backup_var.get() and not self.backup_created:
                    self.create_backup()  # Create a backup if the checkbox is selected and it hasn't been created
                    self.backup_created = True

                copied_items = []
                if self.copy_var.get():
                    copied_items = self.copy_data(self.path_src, self.path_dest)

                deleted_items = []
                if self.delete_var.get():
                    count, deleted_items = self.delete_data_in_path(self.path_src)
                else:
                    count = 0

                self.update_status(count)
                self.log_processed_items(deleted_items, copied_items)
            time.sleep(5)  # Check every 5 seconds

    def create_backup(self):
        if not self.path_dest:
            return

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.zip"
        backup_path = os.path.join(self.path_dest, backup_filename)

        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for root, dirs, files in os.walk(self.path_src):
                for file_ in files:
                    file_path = os.path.join(root, file_)
                    backup_zip.write(file_path, os.path.relpath(file_path, self.path_src))
        print(f"Backup created: {backup_filename}")

    def copy_data(self, src, dest):
        copied_items = []
        try:
            if os.path.isdir(src):
                for root, dirs, files in os.walk(src):
                    for file_ in files:
                        src_file = os.path.join(root, file_)
                        dest_file = os.path.join(dest, os.path.relpath(src_file, src))
                        os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                        shutil.copy2(src_file, dest_file)
                        copied_items.append(src_file)
        except Exception as e:
            print(f"Failed to copy files from {src} to {dest}: {e}")
        return copied_items

    def delete_data_in_path(self, path):
        count = 0
        deleted_items = []
        try:
            for root, dirs, files in os.walk(path):
                for file_ in files:
                    file_path = os.path.join(root, file_)
                    os.remove(file_path)
                    count += 1
                    deleted_items.append(file_path)
                for dir_ in dirs:
                    dir_path = os.path.join(root, dir_)
                    shutil.rmtree(dir_path)
                    count += 1
                    deleted_items.append(dir_path)
        except PermissionError as e:
            print(f"Permission error: {e}. Attempting to change permissions.")
            if self.change_permissions(path):
                for root, dirs, files in os.walk(path):
                    for file_ in files:
                        file_path = os.path.join(root, file_)
                        os.remove(file_path)
                        count += 1
                        deleted_items.append(file_path)
                    for dir_ in dirs:
                        dir_path = os.path.join(root, dir_)
                        shutil.rmtree(dir_path)
                        count += 1
                        deleted_items.append(dir_path)
            else:
                print(f"Failed to delete {path} even after changing permissions.")
        return count, deleted_items

    def change_permissions(self, path):
        try:
            os.chmod(path, stat.S_IWRITE)
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for dir_ in dirs:
                        os.chmod(os.path.join(root, dir_), stat.S_IWRITE)
                    for file_ in files:
                        os.chmod(os.path.join(root, file_), stat.S_IWRITE)
            return True
        except Exception as e:
            print(f"Failed to change permissions for {path}: {e}")
            return False

    def update_status(self, count):
        self.status_label.config(text=f"Items processed: {count}")

    def log_processed_items(self, deleted_items, copied_items):
        self.output_text.delete(1.0, tk.END)
        if deleted_items:
            self.output_text.insert(tk.END, "Deleted items:\n")
            for item in deleted_items:
                self.output_text.insert(tk.END, f"{item}\n")
        if copied_items:
            self.output_text.insert(tk.END, "Copied items:\n")
            for item in copied_items:
                self.output_text.insert(tk.END, f"{item}\n")

    def open_backup_folder(self):
        if self.path_dest:
            os.startfile(self.path_dest)
        else:
            messagebox.showwarning("No Destination Path", "Please enter a destination path before trying to open the backup folder.")

# Create and run the application
root = tk.Tk()
app = DataDeleterApp(root)
root.mainloop()
