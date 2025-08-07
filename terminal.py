import threading
import subprocess
import time
import logging
logger = logging.getLogger(__name__)

def readuserinput(process):
    userinput = ""
    while userinput != "exit":
        userinput = input("% ")
        process.stdin.write(userinput)
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(0.1)
    process.terminate()
    logger.info("Exiting the readuserinput thread...")

def readprocessoutput(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line, end="")
    logger.info("Exiting the readprocessoutput thread...")

def main():
    logging.basicConfig(filename="terminal.log", level=logging.INFO)
    logger.info("Started terminal.py")
    try:
        process = subprocess.Popen(
            ["/bin/bash", "-i"], 
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text=True)
        t1 = threading.Thread(target=readuserinput, args=(process,))
        t2 = threading.Thread(target=readprocessoutput, args=(process,))
        t1.start()
        t2.start()
    except Exception as err:
        logger.error(err)

if __name__ == "__main__":
    main()
