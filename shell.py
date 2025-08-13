import util
import subprocess
from datetime import datetime

class Shell:
    def __init__(self, config):
        self.config = config

    def set_gui(self, gui):
        self.gui = gui

    def preprocess(self, cmd):
        tokens = cmd.strip().split(" ")
        if tokens[0] in self.config["aliases"]:
            name = tokens[0]
            value = self.config["aliases"][name]
            cmd = cmd.replace(name, value, 1)
        for name, value in self.config["variables"].items():
            name = "$" + name
            if name in cmd:
                cmd = cmd.replace(name, value)
        return cmd

    def exec(self, cmd):
        cmd = self.preprocess(cmd)
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
        else:
            cmds = util.split(cmd, delimiter="|")
            results = []
            try:
                for i in range(0, len(cmds)):
                    args = util.split(cmds[i], strip_quotes=True)
                    if i == 0:
                        results.append(subprocess.run(args, capture_output=True, text=True, check=True))
                    else:
                        results.append(subprocess.run(args, input=results[i-1].stdout, capture_output=True, text=True, check=True))
                    if i == len(cmds)-1:
                        self.gui.append("\n" + results[i].stdout)
                        self.gui.append_prefix()
            except Exception as err:
                print(err)
                self.gui.append("\n")
                self.gui.append_prefix()
