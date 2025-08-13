import parser
import subprocess
import os
from datetime import datetime

class Shell:
    def __init__(self, settings):
        self.settings = settings
        self.load_config()

    def set_gui(self, gui):
        self.gui = gui

    def load_config(self):
        if os.path.exists(self.settings.homedir + "/.terminal"):
            self.config = parser.parse_config(self.settings.homedir + "/.terminal")
        elif os.path.exists("config/.terminal"):
            self.config = parser.parse_config("config/.terminal")
        else:
            self.config = {}
        self.config["variables"]["$HOME"] = os.path.expanduser("~")

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
        elif cmd in ("vi", "vim", "wp", "wordprocessor") or cmd.startswith(("vi ", "vim ", "wp ", "wordprocessor ")):
            if os.path.exists(self.settings.wp_path):
                tokens = cmd.split(" ")
                if len(tokens) == 2:
                    subprocess.Popen(["java", "-jar", self.settings.wp_path, tokens[1]])
                else:
                    subprocess.Popen(["java", "-jar", self.settings.wp_path])
                self.gui.append("\n")
                self.gui.append_prefix()
            else:
                self.gui.append("\nThe WordProcessor application is not installed.\n")
                self.gui.append_prefix()
        elif cmd == "paint":
            if os.path.exists(self.settings.paint_path):
                subprocess.Popen(["java", "-jar", self.settings.paint_path])
                self.gui.append("\n")
                self.gui.append_prefix()
            else:
                self.gui.append("\nThe Paint application is not installed.\n")
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
