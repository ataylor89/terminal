import gui
import shell
import settings

def main():
    sets = settings.Settings()
    sh = shell.Shell(sets)
    Gui = gui.GUI(sets)
    sh.set_gui(Gui)
    Gui.set_shell(sh)
    Gui.mainloop()

if __name__ == "__main__":
    main()
