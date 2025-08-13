import shlex

def split(text, delimiter=None):
    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    if delimiter:
        lexer.whitespace += delimiter
        lexer.wordchars = lexer.wordchars.replace(delimiter, "")
    return list(lexer)
