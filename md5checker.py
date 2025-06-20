import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import hashlib
import os

def compute_md5(file_path):
    """Compute the MD5 hash of a file specified by file_path."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        # Return None if any error occurs (e.g., file cannot be read)
        return None

def read_md5_file(md5_path):
    """
    Read the md5.txt file and return a dictionary mapping filenames to expected MD5 hashes.
    Format expected in md5.txt: <md5sum> <filename>
    """
    hashes = {}
    try:
        with open(md5_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split()
                if len(parts) >= 2:
                    md5_hash = parts[0]
                    filename = ' '.join(parts[1:])  # Handles spaces in filenames
                    hashes[filename] = md5_hash
        return hashes
    except Exception as e:
        messagebox.showerror("Error", f"Could not read md5.txt:\n{e}")
        return {}

def check_hashes(directory, md5_dict):
    """
    For each file in the md5_dict, compute its MD5 hash and compare to expected.
    Returns a list of tuples: (filename, status, computed_hash)
    Status can be: NOT FOUND, ERROR, MATCH, MISMATCH
    """
    results = []
    for filename, expected_hash in md5_dict.items():
        full_path = os.path.join(directory, filename)
        if not os.path.exists(full_path):
            results.append((filename, "NOT FOUND", "N/A"))
            continue
        computed_hash = compute_md5(full_path)
        if computed_hash is None:
            results.append((filename, "ERROR", "N/A"))
        else:
            status = "MATCH" if computed_hash == expected_hash else "MISMATCH"
            results.append((filename, status, computed_hash))
    return results

class MD5CheckerApp:
    """Tkinter GUI application for checking MD5 hashes of files in a selected directory."""
    def __init__(self, root):
        self.root = root
        self.root.title("MD5 Hash Checker")

        # Frame for the main button
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Button to select directory and start check
        self.select_dir_button = tk.Button(self.frame, text="Select Directory", command=self.run_check)
        self.select_dir_button.pack()

        # Scrolled text widget to display output
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.output_text.pack(padx=10, pady=10)

    def run_check(self):
        """Open directory selection, read md5.txt, and compare hashes."""
        directory = filedialog.askdirectory(title="Select folder containing files")
        if not directory:
            return

        md5_path = os.path.join(directory, "md5.txt")
        if not os.path.isfile(md5_path):
            messagebox.showwarning("Missing File", "md5.txt not found in selected directory.")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Reading md5.txt...\n")
        md5_dict = read_md5_file(md5_path)

        self.output_text.insert(tk.END, "Checking files...\n\n")
        results = check_hashes(directory, md5_dict)

        for filename, status, computed_hash in results:
            self.output_text.insert(tk.END, f"{filename}: {status}\n")
            if status == "MISMATCH":
                self.output_text.insert(tk.END, f"  Computed: {computed_hash}\n")
                self.output_text.insert(tk.END, f"  Expected: {md5_dict[filename]}\n")
            self.output_text.insert(tk.END, "\n")

        self.output_text.insert(tk.END, "Done.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MD5CheckerApp(root)
    root.mainloop()
