import subprocess
import os
from datetime import datetime

class Shell:
    def __init__(self, settings, gui):
        self.settings = settings
        self.gui = gui

    def exec(self, cmd):
        if cmd == "exit":
            self.gui.destroy()
        elif cmd == "clear":
            self.gui.clear_text()
        elif cmd == "date":
            self.gui.append(datetime.now().strftime("\n%A, %B %d, %Y\n"))
            self.gui.append_prefix()
        elif cmd == "time":
            self.gui.append(datetime.now().strftime("\n%-I:%M %p\n"))
            self.gui.append_prefix()
        elif cmd in ("vi", "vim") or cmd.startswith(("vi ", "vim ")):
            if os.path.exists(self.settings.wp_path):
                tokens = cmd.split(" ")
                if len(tokens) == 2:
                    subprocess.run(["java", "-jar", self.settings.wp_path, tokens[1]])
                else:
                    subprocess.run(["java", "-jar", self.settings.wp_path])
                self.gui.append("\n")
                self.gui.append_prefix()
            else:
                self.gui.append("\nThe WordProcessor application is not installed.\n")
                self.gui.append_prefix()
        else:
            try:
                result = subprocess.run(cmd.split(" "), capture_output=True, text=True, check=True)
                self.gui.append("\n" + result.stdout)
                self.gui.append_prefix()
            except Exception as err:
                print(err)
                self.gui.append("\n")
                self.gui.append_prefix()
