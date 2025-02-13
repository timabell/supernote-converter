![supernote converter logo](https://i.ibb.co/60bcgxc/icon-small.png)
# Supernote-converter
Convert Supernote's `.note` files into `.pdf` files without using the "export" function on a real device.

This program is simply a GUI (graphical user interface) wrapper of [supernote-tool](https://github.com/jya-dev/supernote-tool), and is designed for those unfamiliar with `python` and command-line applications.

At the moment, only Windows is supported.

## Features
There is not much to say... the only "feature" at the moment is that the program remembers the last input and output paths used, so that they do not have to be entered again the next time you want to convert a note. These paths are stored in two text files `last_input_path.txt` and `last_output_path.txt` in the same folder where the main executable is contained.

## Download
Simply go to the [releases](https://github.com/francescoboc/supernote-converter/releases) page and follow the instructions.

## Set up file association

In the file browser set the default application to this, with your equivalent paths. Nemo doesn't like symlinks so you have to find the actual path

`/home/tim/.asdf/installs/python/3.11.3/bin/python3.11 /home/tim/repo/supernote-converter/open_supernote.py`

Finding the actual python path when using asdf:

```
$ which python
/home/tim/.asdf/shims/python

$ asdf which python
/home/tim/.asdf/installs/python/3.11.3/bin/python

$ ll /home/tim/.asdf/installs/python/3.11.3/bin/python
lrwxrwxrwx 1 tim tim 10 May 24  2023 /home/tim/.asdf/installs/python/3.11.3/bin/python -> python3.11

$ file  /home/tim/.asdf/installs/python/3.11.3/bin/python3.11
/home/tim/.asdf/installs/python/3.11.3/bin/python3.11: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b75a53fe87924cb38f2713997562c6c29fecd04c, for GNU/Linux 3.2.0, with debug_info, not stripped
```
