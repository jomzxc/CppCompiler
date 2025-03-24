#parser.py
import ply.yacc as yacc
from lexer import lexer, tokens
from syntax_tree import *

parsing_error = False

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
        elif p.slice[1].type == 'INT_NUM':
            p[0] = Literal('int', p[1])
        elif p.slice[1].type == 'FLOAT_NUM':
            p[0] = Literal('float', p[1])
        elif p.slice[1].type == 'DOUBLE_NUM':
            p[0] = Literal('double', p[1])
        elif p.slice[1].type == 'CHAR_LIT':
            p[0] = Literal('char', p[1])
        elif p.slice[1].type == 'BOOL_LIT':
            p[0] = Literal('bool', p[1])
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 5:
        p[0] = CallExpression(Identifier(p[1]), p[3])

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
    global parsing_error
    parsing_error = True
    if p:
        error_message = f"Syntax error at line {p.lineno}, column {p.lexpos}: Unexpected token '{p.value}' of type '{p.type}'"
        print(error_message)
        parser.errok()
    else:
        print("Syntax error at EOF")

# --- Build the Parser ---
parser = yacc.yacc()


# Sample 1: Simple function definition
sample_code_1 = """
int add(int a, int b) {
    return a + b;
}
"""

# Sample 2: Function with no parameters
sample_code_2 = """
int get_value() {
    return 100;
}
"""

# Sample 3: Variable declaration and assignment
sample_code_3 = """
int main() {
    int x;
    x = 5;
    int y = 10;
    return y;
}
"""

# Sample 4: Arithmetic expression
sample_code_4 = """
int calculate() {
    int result = (5 * 2) + (10 - 3);
    return result;
}
"""

# Sample 5: Comparison expression
sample_code_5 = """
bool compare(int a, int b) {
    return a > b;
}
"""

# Sample 6: If statement
sample_code_6 = """
void check(int num) {
    if (num > 0) {
        return;
    }
}
"""

# Sample 7: If-else statement
sample_code_7 = """
int get_parity(int num) {
    if (num % 2 == 0) {
        return 0;
    } else {
        return 1;
    }
}
"""

# Sample 8: For loop
sample_code_8 = """
int sum_up() {
    int sum = 0;
    for (int i = 0; i < 5; i = i + 1) {
        sum = sum + i;
    }
    return sum;
}
"""

# Sample 9: While loop
sample_code_9 = """
int decrement(int n) {
    while (n > 0) {
        n = n - 1;
    }
    return n;
}
"""

# Sample 10: Multiple declarations and statements in a block
sample_code_10 = """
int process() {
    int a = 5;
    int b;
    b = a * 2;
    int c = b + 1;
    return c;
}
"""

# Test case that was failing
test_code_identity_call = """
int main() {
    int x = identity(10);
    return 0;
}
"""

if __name__ == '__main__':
    # You can test each sample by assigning it to test_code
    test_code = test_code_identity_call  # Change this to test other samples

    lexer.input(test_code)
    tokens_generated = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_generated.append(tok)
    print("Tokens:", tokens_generated)

    parser.parse(test_code, lexer=lexer)
    if not parsing_error:
        print("\nParsing successful!")
        ast_result = parser.parse(test_code, lexer=lexer)
        print("\nAbstract Syntax Tree:", ast_result)
    else:
        print("\nParsing failed due to syntax errors.")