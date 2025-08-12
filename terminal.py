import gui
import shell
import settings

def main():
    config = settings.Settings()
    app = gui.GUI(config)
    sh = shell.Shell(config, app)
    app.set_shell(sh)
    app.mainloop()

if __name__ == "__main__":
    main()
