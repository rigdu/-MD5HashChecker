# MD5 Hash Checker

A simple Tkinter GUI application to verify file integrity using MD5 hashes listed in an `md5.txt` file.

## Features

- Select a folder containing files and an `md5.txt` file.
- Displays which files match, mismatch, or are missing.
- Shows computed and expected hashes for mismatched files.

## Usage

1. Place an `md5.txt` file in the folder you want to check.
    - Each line should be:  
      `<md5_hash> <filename>`
2. Run the application:
    ```bash
    python md5_checker_app.py
    ```
3. Click **"Select Directory"** and choose your folder.

## Requirements

- Python 3.7 or higher
- No external libraries needed (uses standard library and Tkinter)

---
