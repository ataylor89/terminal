def parse_config(filename):
    variables = {}
    aliases = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            tokens = line.split(" ", 1)
            if tokens[0] == "export":
                name, value = tokens[1].split("=")
                variables["$" + name] = clean(value)
            elif tokens[0] == "alias":
                name, value = tokens[1].split("=")
                aliases[name] = clean(value)
    return dict(variables=variables, aliases=aliases)

def clean(value):
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    elif len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    else:
        return value
