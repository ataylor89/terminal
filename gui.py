import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class GUI(tk.Tk):
    def __init__(self, config):
        self.config = config
        vars = config["variables"]
        self.prefix = vars["prefix"]
        tk.Tk.__init__(self)
        self.title("Terminal")
        self.geometry(vars["geometry"])
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.text_area = ScrolledText(self.frame, 
            wrap="word", 
            bg=vars["bg"],
            fg=vars["fg"],
            font=(vars["font"], vars["fontsize"]))
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<Key>", self.handle_key_press)
        self.text_area.bind("<Return>", self.handle_return)
        self.text_area.bind("<BackSpace>", self.handle_delete)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.append_prefix()

    def set_shell(self, shell):
        self.shell = shell

    def append(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def append_prefix(self):
        self.text_area.insert(tk.END, self.prefix)
        self.text_area.see(tk.END)

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.append_prefix()

    def handle_key_press(self, event):
        index = self.text_area.index(tk.INSERT)
        line, pos = index.split(".")
        if int(line) < self.line_count():
            return "break"

    def handle_return(self, event):
        line = self.text_area.index('end-1c').split('.')[0]
        code = self.text_area.get(f"{line}.2", f"{line}.end")
        self.shell.run(code)
        return "break"

    def handle_delete(self, event):
        index = self.text_area.index(tk.INSERT)
        line, pos = index.split(".")
        if int(pos) <= 2 or int(line) < self.line_count():
            return "break"

    def line_count(self):
        index = self.text_area.index(tk.END)
        numlines = int(index.split(".")[0]) - 1
        return numlines
