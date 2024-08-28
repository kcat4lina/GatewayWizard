import os
import shutil
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
import stat

class DataDeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gateway Wizard .69 © Jojo")

        # Apply dark theme
        self.root.configure(bg='#2E2E2E')
        self.root.option_add('*foreground', 'white')
        self.root.option_add('*background', '#2E2E2E')
        self.root.option_add('*Button.background', '#4A4A4A')
        self.root.option_add('*Button.foreground', 'white')
        self.root.option_add('*Entry.background', '#4A4A4A')
        self.root.option_add('*Entry.foreground', 'white')
        self.root.option_add('*Label.background', '#2E2E2E')
        self.root.option_add('*Label.foreground', 'white')
        self.root.option_add('*Text.background', '#4A4A4A')
        self.root.option_add('*Text.foreground', 'white')

        # Initialize UI components
        self.label_src = tk.Label(root, text="Enter the source path to monitor:")
        self.label_src.pack(pady=10)

        self.path_entry_src = tk.Entry(root, width=50)
        self.path_entry_src.pack(pady=5)

        self.label_dest = tk.Label(root, text="Enter the destination path to copy data to:")
        self.label_dest.pack(pady=10)

        self.path_entry_dest = tk.Entry(root, width=50)
        self.path_entry_dest.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=20)

        self.status_label = tk.Label(root, text="Items copied and deleted: 0")
        self.status_label.pack(pady=10)

        self.output_text = tk.Text(root, height=10, width=60)
        self.output_text.pack(pady=10)

        self.monitoring = False
        self.path_src = ""
        self.path_dest = ""

    def start_monitoring(self):
        if self.monitoring:
            return

        self.path_src = self.path_entry_src.get()
        self.path_dest = self.path_entry_dest.get()

        if not self.path_src or not self.path_dest:
            messagebox.showwarning("Input Error", "Please enter both the source and destination paths.")
            return

        if not os.path.exists(self.path_src):
            messagebox.showwarning("Invalid Source Path", "The specified source path does not exist.")
            return

        if not os.path.exists(self.path_dest):
            messagebox.showwarning("Invalid Destination Path", "The specified destination path does not exist.")
            return

        self.monitoring = True
        self.thread = Thread(target=self.monitor_path)
        self.thread.start()

    def monitor_path(self):
        while self.monitoring:
            if os.path.exists(self.path_src):
                copied_items = self.copy_data(self.path_src, self.path_dest)
                count, deleted_items = self.delete_data_at_path(self.path_src)
                self.update_status(count)
                self.log_deleted_items(deleted_items, copied_items)
            time.sleep(5)  # Check every 5 seconds

    def copy_data(self, src, dest):
        """
        Copies files and directories from the source to the destination path.
        Returns a list of copied items.
        """
        copied_items = []
        try:
            for item in os.listdir(src):
                s_item = os.path.join(src, item)
                d_item = os.path.join(dest, item)
                if os.path.isdir(s_item):
                    shutil.copytree(s_item, d_item, dirs_exist_ok=True)
                    copied_items.append(s_item)
                else:
                    shutil.copy2(s_item, d_item)
                    copied_items.append(s_item)
        except Exception as e:
            print(f"Failed to copy from {src} to {dest}: {e}")
        return copied_items

    def change_permissions(self, path):
        """
        Change the permissions of the file or directory to allow deletion.
        """
        try:
            os.chmod(path, stat.S_IWRITE)  # Grant write permission
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

    def delete_data_at_path(self, path):
        """
        Deletes files and subdirectories within the given path but preserves the path directory itself.
        """
        count = 0
        deleted_items = []
        try:
            for item in os.listdir(path):
                full_item_path = os.path.join(path, item)
                if os.path.isfile(full_item_path):
                    os.remove(full_item_path)
                    count += 1
                    deleted_items.append(full_item_path)
                elif os.path.isdir(full_item_path):
                    shutil.rmtree(full_item_path)
                    count += 1
                    deleted_items.append(full_item_path)
        except PermissionError as e:
            print(f"Permission error: {e}. Attempting to change permissions.")
            if self.change_permissions(path):
                for item in os.listdir(path):
                    full_item_path = os.path.join(path, item)
                    if os.path.isfile(full_item_path):
                        os.remove(full_item_path)
                        count += 1
                        deleted_items.append(full_item_path)
                    elif os.path.isdir(full_item_path):
                        shutil.rmtree(full_item_path)
                        count += 1
                        deleted_items.append(full_item_path)
            else:
                print(f"Failed to delete contents of {path} even after changing permissions.")
        return count, deleted_items

    def update_status(self, count):
        """
        Update the status label with the number of items copied and deleted.
        """
        current_text = self.status_label.cget("text")
        if "Items copied and deleted:" in current_text:
            new_count = int(current_text.split(":")[1].strip()) + count
        else:
            new_count = count
        self.status_label.config(text=f"Items copied and deleted: {new_count}")

    def log_deleted_items(self, deleted_items, copied_items):
        """
        Log the names of the copied and deleted items to the output text box.
        """
        if copied_items:
            for item in copied_items:
                self.output_text.insert(tk.END, f"Copied: {item}\n")
        if deleted_items:
            for item in deleted_items:
                self.output_text.insert(tk.END, f"Deleted: {item}\n")
        self.output_text.see(tk.END)  # Scroll to the end of the text box

    def stop_monitoring(self):
        """
        Stop monitoring for changes.
        """
        self.monitoring = False
        if hasattr(self, 'thread'):
            self.thread.join()

# Create and run the main window
root = tk.Tk()
app = DataDeleterApp(root)
root.protocol("WM_DELETE_WINDOW", app.stop_monitoring)  # Handle window close event
root.mainloop()
