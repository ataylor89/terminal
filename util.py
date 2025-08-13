import shlex

def split(text, delimiter=None, quotes="'\""):
    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    if delimiter:
        lexer.whitespace = delimiter
    lexer.quotes = quotes
    return [item.strip() for item in list(lexer)]
