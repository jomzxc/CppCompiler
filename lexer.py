# lexer.py
from ply import lex  # Import the lex module from the PLY library

# --- Lexer ---

# List of token names. This is always required for PLY's lexer.
# These names are used by the parser to refer to the token types.
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
# This dictionary maps keyword strings to their token types.
# Keywords will be recognized as TYPE tokens (for data types) or their specific keyword tokens.
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
# These are defined as global variables starting with 't_'.
# The value of each variable is the regular expression string that matches the corresponding token.
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
# The lexer will skip these characters without producing a token.
t_ignore = ' \t'

def t_COMMENT(t):
    r'(//.*)|(/\*(.|\n)*?\*/)'
    """Handles single-line (// ...) and multi-line (/* ... */) comments.
    It updates the line number counter for multi-line comments."""
    t.lexer.lineno += t.value.count('\n')
    # No return value means this token is discarded and not passed to the parser.

def t_BOOL_LIT(t):
    r'true|false'
    """Handles boolean literals ('true' or 'false').
    It converts the matched string to a Python boolean value."""
    t.value = t.value == 'true'
    return t  # Returning the token makes it available to the parser.

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    """Handles identifiers (variable and function names).
    It checks if the matched string is a reserved keyword and sets the token type accordingly."""
    t.type = keywords.get(t.value, 'ID')  # Check if the identifier is a keyword. If so, use the keyword's token type.
    return t

def t_FLOAT_NUM(t):
    r'(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?[fF]'
    """Handles floating-point numbers with an optional exponent and mandatory 'f' or 'F' suffix.
    It converts the matched string (excluding the suffix) to a Python float."""
    try:
        t.value = float(t.value[:-1])  # Convert to float, excluding the 'f' or 'F' suffix.
    except ValueError:
        print(f"Invalid float format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)  # Skip the problematic character and continue lexing.
    return t

def t_DOUBLE_NUM(t):
    r'(\d+\.\d*|\.\d+)([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
    """Handles double-precision floating-point numbers with an optional exponent.
    It converts the matched string to a Python float."""
    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Invalid double format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
    return t

def t_INT_NUM(t):
    r'[+-]?\d+'
    """Handles integer numbers (sequences of digits).
    It converts the matched string to a Python integer."""
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Invalid integer format: '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
    return t

def t_CHAR_LIT(t):
    r'\'(\\[^\']|.)\''
    """Handles character literals enclosed in single quotes.
    It supports escape sequences (e.g., '\\n', '\\t')."""
    value = t.value[1:-1]  # Remove the surrounding single quotes.
    if value.startswith('\\'):
        # Handle escape sequences
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
            return None  # Don't return a token for an invalid escape sequence.
    else:
        t.value = value
    if len(t.value) != 1:
        print(f"Invalid character literal '{t.value}' at line {t.lexer.lineno}")
        t.lexer.skip(1)
        return None  # Don't return a token for multi-character literals.
    return t

def t_newline(t):
    r'\n+'
    """Tracks line numbers by counting newline characters."""
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error handling for illegal characters that don't match any rule.
    It prints an error message and skips the illegal character."""
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
# This creates the lexer object that can be used to tokenize input text.
lexer = lex.lex()