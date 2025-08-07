# Please note, this is still a work in progress
# It's not done... there is still a lot of work to do

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import time
import fcntl
import os
import logging

logger = logging.getLogger(__name__)

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Terminal")
        self.geometry("900x600")
        self.prefix = "% "
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.text_area = ScrolledText(self.frame, wrap="word")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.bind("<Return>", self.handle_enter)
        self.append_prefix()
        self.protocol("WM_DELETE_WINDOW", self.handle_close)

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
        logger.info("User input = %s" %userinput)
        self.shell.write(userinput)

    def handle_close(self):
        self.shell.stop_event.set()
        self.destroy()

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
            logger.info("Started bash process")
            self.thread = threading.Thread(target=self.readloop)
            self.stop_event = threading.Event()
            self.thread.start()
        except Exception as err:
            logger.error(err)

    def readloop(self):
        logger.info("Starting readloop thread...")
        while not self.stop_event.is_set():
            buffer = ""
            done = False
            while not done:
                try:
                    buffer += self.process.stdout.read()
                except:
                    done = True
            if buffer:
                self.gui.append(buffer)
                self.gui.append_prefix()
        logger.info("Stopping readloop thread...")

    def write(self, userinput):
        self.process.stdin.write(userinput)
        self.process.stdin.write("\n")
        self.process.stdin.flush()

if __name__ == "__main__":
    logging.basicConfig(
        filename="terminal.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger.info("Starting up...")
    gui = GUI()
    shell = Shell(gui)
    gui.set_shell(shell)
    gui.mainloop()
