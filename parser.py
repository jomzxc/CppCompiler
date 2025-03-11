from ply import yacc
from lexer import tokens

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


def p_program(p):
    """program : function_list
               | empty"""
    p[0] = ('program', p[1])


def p_function_list(p):
    """function_list : function
                     | function_list function
                     | empty"""
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_function(p):
    """function : TYPE ID LPAREN param_list RPAREN block
                | TYPE ID LPAREN RPAREN block"""
    if len(p) == 7:
        p[0] = ('function', p[1], p[2], p[4], p[6])
    else:
        p[0] = ('function', p[1], p[2], [], p[5])


def p_param_list(p):
    """param_list : param
                  | param_list COMMA param
                  | empty"""
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []


def p_param(p):
    """param : TYPE ID"""
    p[0] = ('param', p[1], p[2])


def p_block(p):
    """block : LBRACE statement_list RBRACE"""
    p[0] = ('block', p[2])


def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement
                      | empty"""
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


def p_statement(p):
    """statement : loop_statement
                 | declaration_statement
                 | expression SEMI
                 | return_statement SEMI
                 | block
                 | declaration_statement_no_semi SEMI"""
    p[0] = p[1]


def p_loop_statement(p):
    """loop_statement : FOR LPAREN for_init SEMI expression_opt SEMI expression_opt RPAREN block
                      | WHILE LPAREN expression RPAREN block"""
    if p[1] == 'for':
        p[0] = ('for_loop', p[3], p[5], p[7], p[9])
    elif p[1] == 'while':
        p[0] = ('while_loop', p[3], p[5])


def p_for_init(p):
    """for_init : declaration_statement_no_semi
                | expression
                | empty"""
    if len(p) > 1 and p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = None


def p_declaration_statement_no_semi(p):
    """declaration_statement_no_semi : TYPE ID
                                     | TYPE ID ASSIGN expression"""
    if len(p) == 3:
        p[0] = ('declare', p[1], p[2], None)
    else:
        p[0] = ('declare', p[1], p[2], p[4])


def p_declaration_statement(p):
    """declaration_statement : declaration_statement_no_semi"""
    p[0] = p[1]


def p_return_statement(p):
    """return_statement : RETURN expression_opt"""
    p[0] = ('return', p[2])


def p_expression_opt(p):
    """expression_opt : expression
                      | empty"""
    if len(p) > 1 and p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = None


def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression LEQ expression
                  | expression GEQ expression"""
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])


def p_expression_assign(p):
    """expression : ID ASSIGN expression"""
    p[0] = ('assign', p[1], p[3])


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_call(p):
    """expression : ID LPAREN arg_list RPAREN"""
    p[0] = ('call', p[1], p[3])


def p_expression_id(p):
    """expression : ID"""
    p[0] = ('id', p[1])


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = ('number', p[1])


def p_arg_list(p):
    """arg_list : expression
                | arg_list COMMA expression
                | empty"""
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}, token {p.type} ({p.value})")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

# --- Test ---
# if __name__ == "__main__":
#     sample_code = """
#     int main() {
#             int x = 5;
#             x = x + 3;
#             for (int i=0; i<10; i=i+1) {
#                 x = x * i;
#             }
#             return x;
#         }
#     """
#     parsed = parser.parse(sample_code)
#     print(parsed)
#     # now lets show some errors.
#     sample_code_error_1 = """
#     int main() {
#         int x = 5;
#         x = x + 3;
#         while (x < 10) {
#             x = x * 2
#         }
#         return x;
#     """
#     print("---Error test 1---")
#     parsed = parser.parse(sample_code_error_1)
#
#     sample_code_error_2 = """
#     int main(int a, ) {
#         return 0;
#     }
#     """
#     print("---Error test 2---")
#     parsed = parser.parse(sample_code_error_2)
#
#     sample_code_error_3 = """
#     int main() {
#         x = 5 +;
#     }
#     """
#     print("---Error test 3---")
#     parsed = parser.parse(sample_code_error_3)
