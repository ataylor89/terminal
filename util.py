import re

def split(text, delimiter=" ", strip_quotes=False):
    pattern = r'{0}(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)'.format(re.escape(delimiter))
    tokens = re.split(pattern, text)
    for i in range(0, len(tokens)):
        tokens[i] = tokens[i].strip()
        if strip_quotes and is_quoted(tokens[i]):
            tokens[i] = tokens[i][1:-1]
    return tokens

def search(text, delimiter):
    pattern = r'{0}(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)'.format(re.escape(delimiter))
    return re.search(pattern, text)

def is_quoted(text):
    if len(text) >= 2:
        if text[0] == "'" and text[-1] == "'":
            return True
        if text[0] == '"' and text[-1] == '"':
            return True
    return False
