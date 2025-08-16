import gui
from shells import shell, bash
import parser

def main():
    config = parser.parse_config()
    sh = bash.Shell(config)
    Gui = gui.GUI(config)
    sh.set_gui(Gui)
    Gui.set_shell(sh)
    Gui.mainloop()

if __name__ == "__main__":
    main()
