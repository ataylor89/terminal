import shlex

def split(text, delimiter=None, remove_quotes=True):
    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    if delimiter:
        lexer.whitespace = delimiter
    lexer.quotes = "'\"" if remove_quotes else ""
    return [item.strip() for item in list(lexer)]
