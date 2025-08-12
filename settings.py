import os

class Settings:
    def __init__(self):
        self.geometry = "900x600"
        self.bg = "blue"
        self.fg = "white"
        self.font = ("SF Mono Regular", 16)
        self.prefix = "% "
        self.homedir = os.path.expanduser("~")
        self.wp_path = self.homedir + "/Github/WordProcessor/target/WordProcessor.jar"
        self.paint_path = self.homedir + "/Github/Paint/target/Paint.jar"
