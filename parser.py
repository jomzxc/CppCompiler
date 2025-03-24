import ply.yacc as yacc
from lexer import lexer, tokens
from syntax_tree import *

parsing_error = False
syntax_errors = []

tokens = tokens

# Operator precedence (lowest to highest)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN'),
)

# --- Grammar Rules with AST Construction ---

def p_program(p):
    '''program : translation_unit'''
    p[0] = Program(p[1])

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration_statement SEMI'''
    p[0] = p[1]

def p_function_definition(p):
    '''function_definition : TYPE ID LPAREN parameter_list_opt RPAREN block'''
    p[0] = FunctionDefinition(p[1], p[2], p[4], p[6])

def p_parameter_list_opt(p):
    '''parameter_list_opt : parameter_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter_list COMMA parameter'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : TYPE ID'''
    p[0] = Parameter(p[1], p[2])

# --- Blocks ---

def p_block(p):
    '''block : LBRACE statement_list_opt RBRACE'''
    p[0] = Block(p[2])

def p_statement_list_opt(p):
    '''statement_list_opt : statement_list
                           | empty'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# --- Statements ---

def p_statement(p):
    '''statement : declaration_statement SEMI
                 | assignment_statement SEMI
                 | return_statement SEMI
                 | if_statement
                 | for_statement
                 | while_statement
                 | block
                 | expression_statement SEMI
                 | empty_statement SEMI'''
    p[0] = p[1]

def p_empty_statement(p):
    '''empty_statement :'''
    p[0] = EmptyStatement()

# --- Declaration Statements ---

def p_declaration_statement(p):
    '''declaration_statement : TYPE ID
                             | TYPE ID ASSIGN initializer'''
    if len(p) == 3:
        p[0] = Declaration(p[1], p[2], None)
    else:
        p[0] = Declaration(p[1], p[2], p[4])

def p_initializer(p):
    '''initializer : expression'''
    p[0] = p[1]

# --- Assignment Statements ---

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''
    p[0] = Assignment(p[1], p[3])

# --- Return Statements ---

def p_return_statement(p):
    '''return_statement : RETURN expression_opt'''
    p[0] = ReturnStatement(p[2])

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    p[0] = p[1]

# --- Control Flow Statements ---

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = IfStatement(p[3], p[5], None)
    else:
        p[0] = IfStatement(p[3], p[5], p[7])

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_init_opt SEMI for_condition_opt SEMI for_increment_opt RPAREN statement'''
    p[0] = ForStatement(p[3], p[5], p[7], p[9])

def p_for_init_opt(p):
    '''for_init_opt : declaration_statement
                    | expression_statement
                    | empty'''
    p[0] = p[1]

def p_for_condition_opt(p):
    '''for_condition_opt : expression
                         | empty'''
    p[0] = p[1]

def p_for_increment_opt(p):
    '''for_increment_opt : expression
                         | empty'''
    p[0] = p[1]

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = WhileStatement(p[3], p[5])

# --- Expressions ---

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = p[1]

def p_expression(p):
    '''expression : assignment_expression
                  | binary_expression
                  | primary_expression'''
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : ID ASSIGN expression'''
    p[0] = Assignment(p[1], p[3])

def p_binary_expression(p):
    '''binary_expression : expression PLUS expression
                         | expression MINUS expression
                         | expression TIMES expression
                         | expression DIVIDE expression
                         | expression EQ expression
                         | expression NEQ expression
                         | expression LT expression
                         | expression GT expression
                         | expression LEQ expression
                         | expression GEQ expression
                         | expression AND expression
                         | expression OR expression'''
    p[0] = BinaryExpression(p[2], p[1], p[3])

def p_primary_expression(p):
    '''primary_expression : ID
                          | INT_NUM
                          | FLOAT_NUM
                          | DOUBLE_NUM
                          | CHAR_LIT
                          | BOOL_LIT
                          | LPAREN expression RPAREN
                          | ID LPAREN argument_list_opt RPAREN'''
    if len(p) == 2:
        if p.slice[1].type == 'ID':
            p[0] = Identifier(p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)  # Set lineno as an attribute after creation
                p[0].lexpos = p.lexpos(1)  # Set lexpos as an attribute after creation
        elif p.slice[1].type == 'INT_NUM':
            p[0] = Literal('int', p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)
                p[0].lexpos = p.lexpos(1)
        elif p.slice[1].type == 'FLOAT_NUM':
            p[0] = Literal('float', p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)
                p[0].lexpos = p.lexpos(1)
        elif p.slice[1].type == 'DOUBLE_NUM':
            p[0] = Literal('double', p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)
                p[0].lexpos = p.lexpos(1)
        elif p.slice[1].type == 'CHAR_LIT':
            p[0] = Literal('char', p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)
                p[0].lexpos = p.lexpos(1)
        elif p.slice[1].type == 'BOOL_LIT':
            p[0] = Literal('bool', p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)
                p[0].lexpos = p.lexpos(1)
    elif len(p) == 4:
        p[0] = p[2]
        if p[0]:
            p[0].lineno = p.lineno(1)
            p[0].lexpos = p.lexpos(1)
    elif len(p) == 5:
        p[0] = CallExpression(Identifier(p[1]), p[3])
        if p[0].callee: # Access the Identifier object within CallExpression
            p[0].callee.lineno = p.lineno(1)
            p[0].callee.lexpos = p.lexpos(1)

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                          | empty'''
    p[0] = p[1] if p[1] is not None else []

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# --- Empty Production ---

def p_empty(p):
    '''empty :'''
    p[0] = None

# --- Error Handling ---

def p_error(p):
    global parsing_error, syntax_errors
    parsing_error = True
    if p:
        column = p.lexpos - lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        error_message = f"Syntax error at line {p.lineno}, column {column}: Unexpected token '{p.value}' of type '{p.type}'"
        print(error_message) # Keep printing for console output if needed
        syntax_errors.append(error_message) # Store the error
        parser.errok()
    else:
        print("Syntax error at EOF") # Keep printing for console output if needed
        syntax_errors.append("Syntax error at EOF") # Store the error

# --- Build the Parser ---
parser = yacc.yacc()