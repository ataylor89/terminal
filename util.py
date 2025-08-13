import re

def split(text, delimiter=" "):
    pattern = r'{0}(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)'.format(re.escape(delimiter))
    return [token.strip() for token in re.split(pattern, text)]

def search(text, delimiter):
    pattern = r'{0}(?=(?:[^"\']*["\'][^"\']*["\'])*[^"\']*$)'.format(re.escape(delimiter))
    return re.search(pattern, text)
