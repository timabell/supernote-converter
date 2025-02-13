#!/usr/bin/env python
import supernotelib as sn
import tkinter as tk
from tkinter import filedialog, messagebox
import os, shutil

#def load_file(file_name: str) -> str:
#        return os.path.join(os.path.dirname(__file__), file_name)

def save_last_input_path(path):
    with open('last_input_path.txt', 'w') as f:
        f.write(path)

def load_last_input_path():
    try:
        with open('last_input_path.txt', 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        return ''

def save_last_output_path(path):
    with open('last_output_path.txt', 'w') as f:
        f.write(path)

def load_last_output_path():
    try:
        with open('last_output_path.txt', 'r') as f:
            return f.readline().strip()
    except FileNotFoundError:
        return ''

def select_file():
    filetypes = (
        ('Note file', '*.note'),
    )

    last_input_path = load_last_input_path()

    fullpath = filedialog.askopenfilename(
        title='Select note file',
        initialdir=last_input_path,
        filetypes=filetypes)

    if fullpath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, fullpath)
        save_last_input_path(os.path.dirname(fullpath))

def select_output_folder():
    last_output_path = load_last_output_path()
    output_folder_path = filedialog.askdirectory(
        title='Select output folder',
        initialdir=last_output_path,
            )
    if output_folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder_path)
        save_last_output_path(output_folder_path)

def convert():
    input_file_path = file_path_entry.get()
    output_folder_path = output_folder_entry.get()

    if not input_file_path or not output_folder_path:
        messagebox.showerror('Error', 'Please select input file and output folder')
        return

    try:
        note_filename = input_file_path.replace(load_last_input_path(),'')
        pdf_filename = note_filename.replace('.note', '.pdf')

        output_file_path = f'{output_folder_path}/{pdf_filename}'

        notebook = sn.load_notebook(input_file_path)
        conv = sn.converter.PdfConverter(notebook)
        data = conv.convert(-1, vectorize=False, enable_link=True)

        with open(output_file_path, 'wb') as f:
            f.write(data)

        messagebox.showinfo('Success', 'Note converted successfully')

    except Exception as e:
        messagebox.showerror('Error', str(e))

# Create the main window and set properties
root = tk.Tk()
root.title('Supernote to pdf converter')
#root.minsize(400, 270)
root.resizable(False, False)

# Set window icon
#icon = tk.PhotoImage(file=load_file('icon.png'))
icon = tk.PhotoImage(file='img/icon.png')
icon = icon.subsample(2)
root.iconphoto(False, icon)

# Create a label for the header image
image_label = tk.Label(root, image=icon)
image_label.grid(row=0, column=1, padx=0, pady=10, sticky=tk.N)

# Create labels for entry fields
file_label = tk.Label(root, text='Note file:')
file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
output_label = tk.Label(root, text='Output folder:')
output_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

# Create entry fields
file_path_entry = tk.Entry(root, width=40)
file_path_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
output_folder_entry = tk.Entry(root, width=40)
output_folder_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

# Load last output path and insert it into the output folder entry field
last_output_path = load_last_output_path()
output_folder_entry.insert(0, last_output_path)

# Create buttons
file_button = tk.Button(root, text='Browse', command=select_file)
file_button.grid(row=1, column=2, padx=5, pady=5)
output_button = tk.Button(root, text='Browse', command=select_output_folder)
output_button.grid(row=2, column=2, padx=5, pady=5)
convert_button = tk.Button(root, text='Convert to pdf', command=convert)
convert_button.grid(row=3, columnspan=3, padx=5, pady=5)  # Span across 3 columns

# Configure columns to resize with window width
root.columnconfigure(1, weight=1)

# Run the main event loop
root.mainloop()
