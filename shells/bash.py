import subprocess
import fcntl
import os

class Bash:
    def __init__(self):
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

    def readall(self):
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
        return stdout

    def write(self, userinput):
        self.process.stdin.write(userinput)
        self.process.stdin.write("\n")
        self.process.stdin.flush()
