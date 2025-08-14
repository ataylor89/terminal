import util
import subprocess
from datetime import datetime

class Shell:
    def __init__(self, config):
        self.config = config

    def set_gui(self, gui):
        self.gui = gui

    def preprocess(self, code):
        tokens = code.strip().split(" ")
        if tokens[0] in self.config["aliases"]:
            name = tokens[0]
            value = self.config["aliases"][name]
            code = code.replace(name, value, 1)
        for name, value in self.config["variables"].items():
            name = "$" + name
            if name in code:
                code = code.replace(name, value)
        return code

    def run(self, code):
        try:
            self._run(code)
        except Exception as err:
            print(err)
            self.gui.append("\n")
            self.gui.append_prefix()

    def _run(self, code):
        code = self.preprocess(code)
        statements = self.compile(code)
        for statement in statements:
            command = statement["command"] if "command" in statement else None
            commandname = command.split()[0] if command else None
            if "pipes" in statement:
                pipes = statement["pipes"]
                results = []
                for i in range(0, len(pipes)):
                    pipe = pipes[i]
                    command = pipe["command"]
                    commandname = command.split()[0]
                    if commandname == "date":
                        results.append(datetime.now().strftime("\n%A, %B %d, %Y\n"))
                    elif commandname == "time":
                        output = datetime.now().strftime("\n%-I:%M %p\n")
                    else:
                        args = util.split(command, strip_quotes=True)
                        if i == 0:
                            result = subprocess.run(args, capture_output=True, text=True, check=True)
                            results.append(result.stdout)
                        else:
                            result = subprocess.run(args, input=results[i-1], capture_output=True, text=True, check=True)
                            results.append(result.stdout)
                    if pipe["mode"] in ("write", "append"):
                        mode = "w" if pipe["mode"] == "write" else "a"
                        filename = pipe["output_file"]
                        with open(filename, mode) as file:
                            file.write(results[i])
                    if i == len(pipes)-1:
                        if pipe["mode"] == "stdout":
                            self.gui.flush(prefix=False)
                            self.gui.append(results[i])
            elif commandname == "exit":
                self.gui.destroy()
            elif commandname == "clear":
                self.gui.clear_text()
            elif commandname == "date":
                output = datetime.now().strftime("%A, %B %d, %Y")
                if statement["mode"] in ("write", "append"):
                    mode = "w" if statement["mode"] == "write" else "a"
                    filename = statement["output_file"]
                    with open(filename, mode) as file:
                        file.write(output)
                else:
                    self.gui.flush(prefix=False)
                    self.gui.append(output)
            elif commandname == "time":
                output = datetime.now().strftime("%-I:%M %p")
                if statement["mode"] in ("write", "append"):
                    mode = "w" if statement["mode"] == "write" else "a"
                    filename = statement["output_file"]
                    with open(filename, mode) as file:
                        file.write(output)
                else:
                    self.gui.flush(prefix=False)
                    self.gui.append(output)
            else:
                args = util.split(command, strip_quotes=True)
                result = subprocess.run(args, capture_output=True, text=True, check=True)
                if statement["mode"] in ("write", "append"):
                    mode = "w" if statement["mode"] == "write" else "a"
                    filename = statement["output_file"]
                    with open(filename, mode) as file:
                        file.write(result.stdout)
                else:
                    self.gui.flush(prefix=False)
                    self.gui.append(result.stdout)
        self.gui.flush(prefix=True)

    def compile(self, code):
        statements = []
        stmts = util.split(code, delimiter=";")
        for stmt in stmts:
            statement = {}
            statement["code"] = stmt
            if util.search(stmt, "|"):
                pipes = util.split(stmt, delimiter="|")
                statement["pipes"] = []
                for i in range(0, len(pipes)):
                    pipe = {}
                    if util.search(pipes[i], ">"):
                        parts = util.split(pipes[i], ">")
                        if len(parts) != 2:
                            raise SyntaxError("There was an error compiling the code.")
                        pipe["command"] = parts[0]
                        pipe["mode"] = "write"
                        pipe["output_file"] = parts[1]
                    elif util.search(pipes[i], ">>"):
                        parts = util.split(pipes[i], ">>")
                        if len(parts) != 2:
                            raise SyntaxError("There was an error compiling the code.")
                        pipe["command"] = parts[0]
                        pipe["mode"] = "append"
                        pipe["output_file"] = parts[1]
                    else:
                        pipe["command"] = pipes[i]
                        pipe["mode"] = "stdout"
                    statement["pipes"].append(pipe)
            elif util.search(stmt, ">"):
                parts = util.split(stmt, ">")
                if len(parts) != 2:
                    raise SyntaxError("There was an error compiling the code.")
                statement["command"] = parts[0]
                statement["mode"] = "write"
                statement["output_file"] = parts[1]
            elif util.search(stmt, ">>"):
                parts = util.split(stmt, ">>")
                if len(parts) != 2:
                    raise SyntaxError("There was an error compiling the code.")
                statement["command"] = parts[0]
                statement["mode"] = "append"
                statement["output_file"] = parts[1]
            else:
                statement["command"] = stmt
                statement["mode"] = "stdout"
            statements.append(statement)
        return statements
