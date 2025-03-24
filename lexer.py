#lexer.py
from ply import lex

# --- Lexer ---

# List of token names. This is always required
tokens = (
    'TYPE', 'ID', 'INT_NUM', 'FLOAT_NUM', 'CHAR_LIT', 'DOUBLE_NUM', 'BOOL_LIT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMI', 'COMMA',
    'IF', 'ELSE', 'FOR', 'WHILE', 'RETURN',
    'AND', 'OR'
)

# Reserved keywords
keywords = {
    'int': 'TYPE',
    'float': 'TYPE',
    'double': 'TYPE',
    'char': 'TYPE',
    'bool': 'TYPE',
    'void': 'TYPE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'return': 'RETURN',
}

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMI = r';'
t_COMMA = r','
t_AND = r'&&'
t_OR = r'\|\|'

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    t.lexer.lineno += t.value.count('\n')

def t_BOOL_LIT(t):
    r'true|false'
    """Handles boolean literals."""
    t.value = t.value == 'true'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    """Handles identifiers and checks for keywords."""
    t.type = keywords.get(t.value, 'ID')
    return t

def t_FLOAT_NUM(t):
    r'(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?[fF]'
    """Handles floating-point numbers with 'f' or 'F' suffix."""
    try:
        t.value = float(t.value[:-1])
    except ValueError:
        print(f"Invalid float format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
    return t

def t_DOUBLE_NUM(t):
    r'(\d+\.\d*|\.\d+)([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    """Handles double-precision floating-point numbers."""
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Invalid double format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
    return t

def t_INT_NUM(t):
    r'\d+'
    """Handles integer numbers."""
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Invalid integer format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
    return t

def t_CHAR_LIT(t):
    r'\'(\\[^\']|.)\''
    """Handles character literals, including escape sequences."""
    value = t.value[1:-1]
    if value.startswith('\\'):
        esc = value[1]
        if esc == 'n':
            t.value = '\n'
        elif esc == 't':
            t.value = '\t'
        elif esc == 'r':
            t.value = '\r'
        elif esc == 'b':
            t.value = '\b'
        elif esc == '\\':
            t.value = '\\'
        elif esc == '\'':
            t.value = '\''
        elif esc == '"':
            t.value = '"'
        else:
            print(f"Invalid escape sequence '\\{esc}' at line {t.lexer.lineno}")
            t.lexer.skip(1)
            return None
    else:
        t.value = value
    if len(t.value) != 1:
        print(f"Invalid character literal '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
        return None
    return t

def t_newline(t):
    r'\n+'
    """Tracks line numbers."""
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error handling for illegal characters."""
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()