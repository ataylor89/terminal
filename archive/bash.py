# This file is actually a work in progress
# The file shell.py is more fully functional
# We are using polymorphism because we can substitute a Shell instance from this file or from bash.py
# We can even create a third file called zsh.py
# I'm still working on this file
# It's a work in progress

import subprocess
import time
import fcntl
import os
from datetime import datetime

class Shell:
    def __init__(self, config):
        self.config = config
        try:
            self.process = subprocess.Popen(
                ["/bin/bash", "-i"],
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True)
            fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(self.process.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        except Exception as err:
            print(err)

    def set_gui(self, gui):
        self.gui = gui

    def run(self, cmd):
        cmdname = cmd.split()[0] if cmd else None
        if cmdname == "exit":
            self.process.terminate()
            self.gui.destroy()
        elif cmdname == "clear":
            self.gui.clear_text()
            self.gui.flush(prefix=True)
        elif cmdname == "date":
            self.gui.flush(prefix=False)
            self.gui.append(datetime.now().strftime("%A, %B %d, %Y"))
            self.gui.flush(prefix=True)
        elif cmdname == "time":
            self.gui.flush(prefix=False)
            self.gui.append(datetime.now().strftime("%-I:%M %p"))
            self.gui.flush(prefix=True)
        else:
            self.process.stdin.write(cmd)
            self.process.stdin.write("\n")
            self.process.stdin.flush()
            time.sleep(0.01)
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
            self.gui.flush(prefix=False)
            self.gui.append(stdout)
            self.gui.flush(prefix=True)
