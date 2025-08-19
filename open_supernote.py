#!/usr/bin/env python
import supernotelib as sn
import os
import sys
import tempfile
import subprocess
import datetime
import tkinter as tk
from tkinter import ttk
import threading
import time

def open_with_default_application(file_path):
    print(f"Opening file with default application: {file_path}")
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.call(["open", file_path])
    else:
        subprocess.call(["xdg-open", file_path])

def convert(input_file_path, output_folder_path, status_callback=None):
    try:
        if status_callback:
            status_callback("Loading notebook...")

        original_file_name = os.path.basename(input_file_path)
        pdf_filename = original_file_name.replace('.note', '.pdf')
        output_file_path = os.path.join(output_folder_path, pdf_filename)

        if status_callback:
            status_callback(f"Saving to: {output_file_path}")

        os.makedirs(output_folder_path, exist_ok=True)
        notebook = sn.load_notebook(input_file_path)

        if status_callback:
            status_callback("Converting to PDF...")

        conv = sn.converter.PdfConverter(notebook)
        data = conv.convert(-1, vectorize=False, enable_link=True)

        if status_callback:
            status_callback("Writing PDF file...")

        with open(output_file_path, 'wb') as f:
            f.write(data)

        if status_callback:
            status_callback("Conversion complete!")

        return output_file_path
    except Exception as e:
        if status_callback:
            status_callback(f"Error: {str(e)}")
        raise e

def main():
    if len(sys.argv) != 2:
        print("Usage: supernote_converter.py <note_file>")
        sys.exit(1)

    note_file_path = sys.argv[1]

    if not note_file_path.endswith('.note'):
        print("Error: The input file must have a '.note' extension.")
        sys.exit(3)

    if not os.path.isfile(note_file_path):
        print(f"Error: File '{note_file_path}' not found.")
        sys.exit(2)

    # Create progress window
    root = tk.Tk()
    root.title("Supernote Converter")
    root.geometry("400x150")

    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    # Add some padding
    frame = ttk.Frame(root, padding="20 20 20 20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a label for the file being converted
    file_label = ttk.Label(frame, text=f"Converting: {os.path.basename(note_file_path)}")
    file_label.pack(anchor="w", pady=(0, 10))

    # Add status label
    status_var = tk.StringVar(value="Starting conversion...")
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.pack(anchor="w")

    # Add progress bar
    progress = ttk.Progressbar(frame, mode="indeterminate")
    progress.pack(fill=tk.X, pady=10)
    progress.start()

    def update_status(message):
        status_var.set(message)
        root.update_idletasks()

    def conversion_thread():
        try:
            temp_dir = tempfile.gettempdir()
            current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            temp_file_path = os.path.join(temp_dir, 'supernote-conversions', current_datetime)

            output_file_path = convert(note_file_path, temp_file_path, update_status)

            update_status("Opening PDF viewer...")

            # Launch the PDF viewer
            open_with_default_application(output_file_path)

            # Wait a moment to ensure the PDF viewer has started
            time.sleep(1.5)

            # Now close the window
            root.destroy()

        except Exception as e:
            update_status(f"Error: {str(e)}")
            # Keep window open on error, add a close button
            close_btn = ttk.Button(frame, text="Close", command=root.destroy)
            close_btn.pack(pady=10)
            progress.stop()

    # Start conversion in a separate thread
    threading.Thread(target=conversion_thread, daemon=True).start()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
