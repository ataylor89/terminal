import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import time
import subprocess
import os

class GUI(tk.Tk):
    def __init__(self, settings):
        self.settings = settings
        tk.Tk.__init__(self)
        self.title("Terminal")
        self.geometry(settings.geometry)
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.text_area = ScrolledText(self.frame, wrap="word", bg=settings.bg, fg=settings.fg, font=settings.font)
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<Return>", self.handle_enter)
        self.text_area.bind("<BackSpace>", self.handle_delete)
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        self.append_prefix()

    def set_shell(self, shell):
        self.shell = shell

    def append(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def append_prefix(self):
        self.text_area.insert(tk.END, self.settings.prefix)
        self.text_area.see(tk.END)

    def handle_enter(self, event):
        line = self.text_area.index('end-1c').split('.')[0]
        userinput = self.text_area.get(f"{line}.2", f"{line}.end")
        if userinput == "exit":
            self.handle_close()
        elif userinput == "clear":
            self.clear_text()
            return "break"
        elif userinput == "date":
            self.append(datetime.now().strftime("\n%A, %B %d, %Y\n"))
            self.append_prefix()
            return "break"
        elif userinput == "time":
            self.append(datetime.now().strftime("\n%-I:%M %p\n"))
            self.append_prefix()
            return "break"
        elif userinput in ("vi", "vim") or userinput.startswith(("vi ", "vim ")):
            if os.path.exists(self.settings.wp_path):
                tokens = userinput.split(" ")
                if len(tokens) == 2:
                    subprocess.Popen(["java", "-jar", self.settings.wp_path, tokens[1]])
                else:
                    subprocess.Popen(["java", "-jar", self.settings.wp_path])
                self.append("\n")
                self.append_prefix()
                return "break"
        else:
            self.shell.write(userinput)
            self.append("\n")
            time.sleep(0.1)
            stdout = self.shell.readall()
            self.append(stdout)
            self.append_prefix()
            return "break"

    def handle_delete(self, event):
        index = self.text_area.index(tk.INSERT)
        line, pos = index.split(".")
        pos = int(pos)
        if pos <= 2:
            return "break"

    def handle_close(self):
        self.destroy()

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.append_prefix()
