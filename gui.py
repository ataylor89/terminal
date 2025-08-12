import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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
        self.text_area.bind("<Return>", self.handle_return)
        self.text_area.bind("<BackSpace>", self.handle_backspace)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.append_prefix()

    def set_shell(self, shell):
        self.shell = shell

    def append(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def append_prefix(self):
        self.text_area.insert(tk.END, self.settings.prefix)
        self.text_area.see(tk.END)

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.append_prefix()

    def handle_return(self, event):
        line = self.text_area.index('end-1c').split('.')[0]
        userinput = self.text_area.get(f"{line}.2", f"{line}.end")
        self.shell.exec(userinput)
        return "break"

    def handle_backspace(self, event):
        index = self.text_area.index(tk.INSERT)
        line, pos = index.split(".")
        pos = int(pos)
        if pos <= 2:
            return "break"
