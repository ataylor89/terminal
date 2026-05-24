import tkinter as tk
import os
import pty
import threading

class Terminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Terminal')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f'{width}x{height}+0+0')
        self.text = tk.Text(self, background='blue', foreground='white', font=('SF Mono Regular', 16))
        self.text.pack(expand=True, fill='both')
        self.pid, self.parent_fd = pty.fork()
        if self.pid == 0:
            os.execlp('bash', 'bash')
        else:
            self.text.bind('<Key>', self.write_to_pty)
            threading.Thread(target=self.read_from_pty, daemon=True).start()

    def write_to_pty(self, event):
        char = event.char
        if event.keysym == 'Return':
            char = '\n'
        os.write(self.parent_fd, char.encode())
        return 'break'

    def read_from_pty(self):
        while True:
            try:
                data = os.read(self.parent_fd, 1024).decode(errors='ignore')
                if data:
                    self.text.insert('end', data)
                    self.text.see('end')
            except OSError:
                break

if __name__ == '__main__':
    gui = Terminal()
    gui.mainloop()
