import gui
import shell
import settings

def main():
    app = gui.GUI(settings.Settings())
    app.set_shell(shell.Shell())
    app.mainloop()

if __name__ == "__main__":
    main()
