#!/usr/bin/env python
import supernotelib as sn
import os
import sys
import tempfile
import subprocess
import datetime

def open_with_default_application(file_path):
    print(f"Opening file with default application: {file_path}")
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.call(["open", file_path])
    else:
        subprocess.call(["xdg-open", file_path])

def convert(input_file_path, output_folder_path):
    original_file_name = os.path.basename(input_file_path)
    pdf_filename = original_file_name.replace('.note', '.pdf')
    output_file_path = os.path.join(output_folder_path, pdf_filename)
    print(f"Saving converted content to temporary file: {output_file_path}")
    os.makedirs(output_folder_path, exist_ok=True)
    notebook = sn.load_notebook(input_file_path)
    conv = sn.converter.PdfConverter(notebook)
    data = conv.convert(-1, vectorize=False, enable_link=True)
    with open(output_file_path, 'wb') as f:
        f.write(data)
    return output_file_path

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

    print(f"Converting note file: {note_file_path}")
    temp_dir = tempfile.gettempdir()
    original_file_name = os.path.basename(note_file_path)
    current_datetime = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    temp_file_path = os.path.join(temp_dir, 'supernote-conversions', current_datetime)
    output_file_path = convert(note_file_path, temp_file_path)
    open_with_default_application(output_file_path)

if __name__ == "__main__":
    main()
