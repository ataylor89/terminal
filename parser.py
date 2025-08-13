import os

homedir = os.path.expanduser("~")
paths = [homedir + "/.terminal", "config/.terminal"]

def parse_config(filename=None):
    config = defaults()
    if not filename:
        for path in paths:
            if os.path.exists(path):
                filename = path
                break
    if not filename or not os.path.exists(filename):
        return config
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            line = line.strip()
            if not line:
                continue
            tokens = line.split(" ", 1)
            if tokens[0] == "export":
                name, value = tokens[1].split("=")
                config["variables"][name] = clean(value)
            elif tokens[0] == "alias":
                name, value = tokens[1].split("=")
                config["aliases"][name] = clean(value)
    return config

def clean(value):
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    elif len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    else:
        return value

def defaults():
    return {
        "variables": {
            "home": homedir,
            "geometry": "900x600",
            "bg": "blue",
            "fg": "white",
            "font": "SF Mono Regular",
            "fontsize": 16,
            "prefix": "% "
        },
        "aliases": {}
    }
