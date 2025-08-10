import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import fcntl
import os
from datetime import datetime

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Terminal")
        self.geometry("900x600")
        self.prefix = "% "
        self.home = os.path.expanduser("~")
        self.paths = {"wordprocessor": self.home + "/Github/WordProcessor/target/WordProcessor.jar"}
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.text_area = ScrolledText(self.frame, wrap="word", bg="blue", fg="white", font=("SF Mono Regular", 16))
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
        self.text_area.insert(tk.END, self.prefix)
        self.text_area.see(tk.END)

    def handle_enter(self, event):
        line = self.text_area.index('end-1c').split('.')[0]
        userinput = self.text_area.get(f"{line}.2", f"{line}.end")
        if userinput == "exit":
            self.handle_close()
        elif userinput == "clear":
            self.clear_text()
            return "break"
        elif userinput == "time":
            self.append(datetime.now().astimezone().strftime("\nIt is %-I:%M %p on %A, %B %d, %Y\n"))
            self.append_prefix()
            return "break"
        elif userinput.startswith(("vi", "vim", "wp", "wordprocessor")):
            if os.path.exists(self.paths["wordprocessor"]):
                tokens = userinput.split(" ")
                if len(tokens) == 2:
                    subprocess.Popen(["java", "-jar", self.paths["wordprocessor"], tokens[1]])
                else:
                    subprocess.Popen(["java", "-jar", self.paths["wordprocessor"]])
                self.append("\n")
                self.append_prefix()
                return "break"
        else:
            self.shell.write(userinput)

    def handle_delete(self, event):
        index = self.text_area.index(tk.INSERT)
        line, pos = index.split(".")
        pos = int(pos)
        if pos <= 2:
            return "break"

    def handle_close(self):
        self.shell.stop_event.set()
        self.destroy()

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.append_prefix()

class Shell:
    def __init__(self, gui):
        self.gui = gui
        try:
            self.process = subprocess.Popen(
                ["/bin/bash", "-i"],
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True)
            fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(self.process.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            self.thread = threading.Thread(target=self.readloop)
            self.stop_event = threading.Event()
            self.thread.start()
        except Exception as err:
            print(err)

    def readloop(self):
        key_phrases = ["command not found", "No such file", ">", "rm"]
        while not self.stop_event.is_set():
            stdout = ""
            stderr = ""
            done = False
            while not done:
                try:
                    stdout += self.process.stdout.read()
                except:
                    done = True
            done = False
            while not done:
                try:
                    stderr += self.process.stderr.read()
                except:
                    done = True
            if stdout:
                self.gui.append(stdout)
                self.gui.append_prefix()
            elif any(phrase in stderr for phrase in key_phrases):
                self.gui.append_prefix()

    def write(self, userinput):
        self.process.stdin.write(userinput)
        self.process.stdin.write("\n")
        self.process.stdin.flush()

if __name__ == "__main__":
    gui = GUI()
    shell = Shell(gui)
    gui.set_shell(shell)
    gui.mainloop()
