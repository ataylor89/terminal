import shlex

def split(text, delimiter=None):
    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    lexer.quotes = ""
    if delimiter:
        lexer.whitespace = delimiter
    return [item.strip() for item in list(lexer)]
