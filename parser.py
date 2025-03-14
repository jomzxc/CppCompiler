#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2025-03-11

@author: Jomzxc
"""

from ply import yacc
from lexer import tokens
import semantic

# Define operator precedence. This is used to resolve parsing ambiguities.
# Operators lower in the list have higher precedence.
precedence = (
    ('right', 'ASSIGN'),  # Assignment operator has the lowest precedence and is right-associative
    ('left', 'EQ', 'NEQ'),  # Equality and inequality operators
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),  # Less than, greater than, less or equal, greater or equal
    ('left', 'PLUS', 'MINUS'),  # Addition and subtraction
    ('left', 'TIMES', 'DIVIDE'),  # Multiplication and division have the highest precedence
)

# Grammar rules start here. Each function named `p_rulename` defines a rule in the grammar.
# The docstring within each function is the grammar rule itself, in yacc format.
# The function body defines the action to be taken when this rule is recognized (i.e., how to build the AST node).


def p_program(p):
    """program : function_list
               | empty"""
    # A program is either a list of functions or empty.
    # p[0] is the parsed structure for 'program'.
    # It's a tuple: ('program', function_list) or ('program', None) if empty.
    p[0] = ('program', p[1])


def p_function_list(p):
    """function_list : function
                     | function_list function
                     | empty"""
    # A function_list can be:
    # 1. A single function.
    # 2. A function_list followed by another function (recursive rule for lists).
    # 3. Empty (no functions).
    if len(p) == 2:  # Case 1 or 3: single function or empty
        if p[1] is None:  # Case 3: empty
            p[0] = []  # Empty list of functions
        else:  # Case 1: single function
            p[0] = [p[1]]  # List containing the single parsed function
    elif len(p) == 3:  # Case 2: function_list function
        p[0] = p[1] + [p[2]]  # Append the new function to the existing list of functions
    else:  # Should not reach here in normal parsing, but for 'empty' production of function_list
        p[0] = []  # Empty list


def p_function(p):
    """function : TYPE ID LPAREN param_list RPAREN block
                | TYPE ID LPAREN RPAREN block"""
    # A function definition can be:
    # 1. With parameters: TYPE ID ( param_list ) block
    # 2. Without parameters: TYPE ID ( ) block
    if len(p) == 7:  # Case 1: with parameters
        # p[0] is ('function', return_type, function_name, parameter_list, function_block)
        p[0] = ('function', p[1], p[2], p[4], p[6])
    else:  # Case 2: without parameters
        # p[0] is ('function', return_type, function_name, [], function_block) - empty list for parameters
        p[0] = ('function', p[1], p[2], [], p[5])


def p_param_list(p):
    """param_list : param
                  | param_list COMMA param
                  | empty"""
    # A param_list can be:
    # 1. A single parameter.
    # 2. A param_list followed by a comma and another parameter (recursive list).
    # 3. Empty (no parameters).
    if len(p) == 2:  # Case 1 or 3: single parameter or empty
        if p[1] is None:  # Case 3: empty
            p[0] = []  # Empty list of parameters
        else:  # Case 1: single parameter
            p[0] = [p[1]]  # List with the single parsed parameter
    elif len(p) == 4:  # Case 2: param_list COMMA param
        p[0] = p[1] + [p[3]]  # Append the new parameter to the existing list
    else:  # Should not reach here in normal parsing, but for 'empty' production of param_list
        p[0] = []  # Empty list


def p_param(p):
    """param : TYPE ID"""
    # A parameter is defined as: TYPE ID (e.g., 'int x', 'void foo').
    # p[0] is ('param', parameter_type, parameter_name)
    p[0] = ('param', p[1], p[2])


def p_block(p):
    """block : LBRACE statement_list RBRACE"""
    # A block is defined as: { statement_list }.
    # p[0] is ('block', statement_list) - a block contains a list of statements.
    p[0] = ('block', p[2])


def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement
                      | empty"""
    # A statement_list can be:
    # 1. A single statement.
    # 2. A statement_list followed by another statement (recursive list).
    # 3. Empty (no statements).
    if len(p) == 2:  # Case 1 or 3: single statement or empty
        if p[1] is None:  # Case 3: empty
            p[0] = []  # Empty list of statements
        else:  # Case 1: single statement
            p[0] = [p[1]]  # List with the single parsed statement
    elif len(p) == 3:  # Case 2: statement_list statement
        p[0] = p[1] + [p[2]]  # Append the new statement to the existing list
    else:  # Should not reach here in normal parsing, but for 'empty' production of statement_list
        p[0] = []  # Empty list


def p_statement(p):
    """statement : loop_statement
                 | declaration_statement
                 | expression SEMI
                 | return_statement SEMI
                 | block
                 | declaration_statement_no_semi SEMI"""  # Corrected rule - declaration_statement_no_semi needs SEMI in statement
    # A statement can be one of the following:
    # 1. A loop statement (for, while).
    # 2. A declaration statement (with or without initialization, followed by SEMI in statement context).
    # 3. An expression followed by a semicolon (e.g., assignment, function call).
    # 4. A return statement followed by a semicolon.
    # 5. A block statement (nested block).
    p[0] = p[1]  # A statement is simply the parsed structure of its specific type.


def p_loop_statement(p):
    """loop_statement : FOR LPAREN for_init SEMI expression_opt SEMI expression_opt RPAREN block
                      | WHILE LPAREN expression RPAREN block"""
    # A loop_statement can be:
    # 1. A for loop: FOR ( for_init ; condition ; increment ) block
    # 2. A while loop: WHILE ( condition ) block
    if p[1] == 'for':  # Case 1: for loop
        # p[0] is ('for_loop', initialization, condition, increment, loop_body)
        p[0] = ('for_loop', p[3], p[5], p[7], p[9])
    elif p[1] == 'while':  # Case 2: while loop
        # p[0] is ('while_loop', condition, loop_body)
        p[0] = ('while_loop', p[3], p[5])


def p_for_init(p):
    """for_init : declaration_statement_no_semi
                | expression
                | empty"""
    # for_init can be:
    # 1. A declaration statement without a semicolon (e.g., 'int i = 0').
    # 2. An expression (e.g., 'i = 0').
    # 3. Empty (no initialization).
    if len(p) > 1 and p[1] is not None:  # Case 1 or 2: declaration or expression
        p[0] = p[1]  # Use the parsed structure of declaration or expression
    else:  # Case 3: empty
        p[0] = None  # No initialization


def p_declaration_statement_no_semi(p):
    """declaration_statement_no_semi : TYPE ID
                                     | TYPE ID ASSIGN expression"""
    # declaration_statement_no_semi can be:
    # 1. TYPE ID (e.g., 'int x' - declaration without initialization).
    # 2. TYPE ID ASSIGN expression (e.g., 'int x = 5' - declaration with initialization).
    if len(p) == 3:  # Case 1: declaration without initialization
        # p[0] is ('declare', data_type, variable_name, initial_value=None)
        p[0] = ('declare', p[1], p[2], None)
    else:  # Case 2: declaration with initialization
        # p[0] is ('declare', data_type, variable_name, initial_value=expression)
        p[0] = ('declare', p[1], p[2], p[4])


def p_declaration_statement(p):
    """declaration_statement : declaration_statement_no_semi SEMI"""  # Corrected rule - declaration_statement needs SEMI
    # A declaration_statement is a declaration_statement_no_semi followed by a semicolon.
    p[0] = p[1]  # Re-use the structure from declaration_statement_no_semi


def p_return_statement(p):
    """return_statement : RETURN expression_opt"""
    # A return statement is: RETURN [expression_opt].
    # expression_opt is optional expression to return.
    # p[0] is ('return', return_expression) - return_expression can be None if 'empty' production is used for expression_opt.
    p[0] = ('return', p[2])


def p_expression_opt(p):
    """expression_opt : expression
                      | empty"""
    # expression_opt can be:
    # 1. An expression.
    # 2. Empty (no expression).
    if len(p) > 1 and p[1] is not None:  # Case 1: expression
        p[0] = p[1]  # Use the parsed expression structure
    else:  # Case 2: empty
        p[0] = None  # No expression


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
    # Expression can be a binary operation:
    # expression OPERATOR expression, where OPERATOR is one of: +, -, *, /, ==, !=, <, >, <=, >=
    if len(p) == 4:  # For all binary operations defined above
        # p[0] is ('binop', operator, left_operand, right_operand)
        p[0] = ('binop', p[2], p[1], p[3])


def p_expression_assign(p):
    """expression : ID ASSIGN expression"""
    # Assignment expression: ID = expression.
    # p[0] is ('assign', variable_name, assigned_expression)
    p[0] = ('assign', p[1], p[3])


def p_expression_group(p):
    """expression : LPAREN expression RPAREN"""
    # Grouped expression: ( expression ).  Used to override precedence.
    # p[0] is simply the expression inside the parentheses.
    p[0] = p[2]


def p_expression_call(p):
    """expression : ID LPAREN arg_list RPAREN"""
    # Function call expression: ID ( arg_list ).
    # p[0] is ('call', function_name, argument_list)
    p[0] = ('call', p[1], p[3])


def p_expression_id(p):
    """expression : ID"""
    # Identifier (variable name) in an expression.
    # p[0] is ('id', identifier_name)
    p[0] = ('id', p[1])


def p_expression_number(p):
    """expression : INT_NUM
                 | FLOAT_NUM
                 | DOUBLE_NUM
                 | CHAR_LIT
                 | BOOL_LIT"""
    # Create different AST nodes based on the type
    if p.slice[1].type == 'INT_NUM':
        p[0] = ('int_literal', p[1])
    elif p.slice[1].type == 'FLOAT_NUM':
        p[0] = ('float_literal', p[1])
    elif p.slice[1].type == 'DOUBLE_NUM':
        p[0] = ('double_literal', p[1])
    elif p.slice[1].type == 'CHAR_LIT':
        p[0] = ('char_literal', p[1])
    elif p.slice[1].type == 'BOOL_LIT':
        p[0] = ('bool_literal', p[1])


def p_arg_list(p):
    """arg_list : expression
                | arg_list COMMA expression
                | empty"""
    # arg_list can be:
    # 1. A single expression (argument).
    # 2. An arg_list followed by a comma and another expression (recursive list).
    # 3. Empty (no arguments).
    if len(p) == 2:  # Case 1 or 3: single argument or empty
        if p[1] is None:  # Case 3: empty
            p[0] = []  # Empty list of arguments
        else:  # Case 1: single argument
            p[0] = [p[1]]  # List with the single parsed argument
    elif len(p) == 4:  # Case 2: arg_list COMMA expression
        p[0] = p[1] + [p[3]]  # Append the new argument to the existing list
    else:  # Should not reach here in normal parsing, but for 'empty' production of arg_list
        p[0] = []  # Empty list


def p_empty(p):
    """empty :"""
    # Empty production rule.  Means "nothing is here".
    p[0] = None  # Represented as None in the parsed structure.


def p_error(p):
    """error : syntax error handling function"""
    # Error handling function called by yacc when a syntax error is encountered during parsing.
    # 'p' is the token where the error occurred. If p is None, it's an error at EOF.
    if p:
        # Extract useful information from the token 'p' where error occurred
        token_type = p.type  # Type of the token (e.g., 'ID', 'NUMBER', 'SEMI', '}')
        token_value = p.value  # Actual text of the token that caused the error
        line_no = p.lineno  # Line number where the error occurred
        column = p.lexpos  # Character position in the line (lexpos)

        error_message = f"Syntax error at line {line_no}, column {column}: "  # Start building the error message

        # Provide more specific error messages based on the token type, to give user better hints
        if token_type == 'SEMI':
            error_message += f"Unexpected semicolon ';'. Semicolons are statement terminators. "
        elif token_type == 'RBRACE':
            error_message += f"Unexpected closing brace '}}'. Check for mismatched braces or incorrect block structure. "
        elif token_type == 'error':  # 'error' token type might be assigned by lexer for invalid tokens
            error_message += f"Invalid token '{token_value}'. This token is not recognized in the language. "
        elif token_type == 'ID':
            error_message += f"Unexpected identifier '{token_value}'. Check if it's used in the correct context. "
        elif token_type in (
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ', 'ASSIGN', 'COMMA', 'LPAREN',
        'RPAREN'):
            error_message += f"Unexpected operator or symbol '{token_value}'. Check operator usage or expression structure. "
        else:  # General error message for other unexpected tokens
            error_message += f"Unexpected token '{token_value}' of type '{token_type}'. "

        raise SyntaxError(error_message)  # Raise a Python SyntaxError exception with the detailed error message
    else:  # Error at End of File (EOF)
        raise SyntaxError(
            "Syntax error at EOF: Unexpected end of file. Program might be incomplete.")  # Error message for EOF errors


# Build the parser using ply.yacc.
parser = yacc.yacc()

# --- Test ---
# Example code to test the parser (can be uncommented to run parser directly from this file)
# if __name__ == "__main__":
    # sample_code = """
    # int main() {
    #         int x = 5;
    #         x = x + 3;
    #         for (int i=0; i<10; i=i+1) {
    #             x = x * i;
    #         }
    #         return x;
    #     }
    # """
    # parsed = parser.parse(sample_code)
    # print(parsed)
    # # Example of code with syntax errors for testing error reporting
    # sample_code_error_1 = """
    # int main() {
    #     int x = 5;
    #     x = x + 3;
    #     while (x < 10) {
    #         x = x * 2
    #     }
    #     return x;
    # """
    # print("---Error test 1---")
    # parsed = parser.parse(sample_code_error_1)
    #
    # sample_code_error_2 = """
    # int main(int a, ) {
    #     return 0;
    # }
    # """
    # print("---Error test 2---")
    # parsed = parser.parse(sample_code_error_2)
    #
    # sample_code_error_3 = """
    # int main() {
    #     x = 5 +;
    # }
    # """
    # print("---Error test 3---")
    # parsed = parser.parse(sample_code_error_3)

    # # sample int error
    # sample_code_error_int = """
    # int main() {
    #     int x = 3;
    #     return 0;
    # }
    # """
    # print("---Testing Invalid Integer---")
    # parsed = parser.parse(sample_code_error_int)
    # semantic.analyze_ast(parsed)

    # # sample float error
    # sample_code_error_float = """
    # int main() {
    #     float x = 'a';
    # }
    # """
    # print("---Testing Invalid Float---")
    # parsed = parser.parse(sample_code_error_float)
    # semantic.analyze_ast(parsed)

    # # sample double error
    # sample_code_error_double = """
    # int main() {
    #     double x = 2.5;
    #     return 0;
    # }
    # """
    # print("---Testing Invalid Double---")
    # parsed = parser.parse(sample_code_error_double)

    # # sample char error
    # sample_code_error_char = """
    # int main() {
    #     char c = 'AB';
    #     return 0;
    # }
    # """
    # print("---Testing Invalid Char---")
    # parsed = parser.parse(sample_code_error_char)

    # # sample bool error
    # sample_code_error_bool = """
    # int main() {
    #     bool flag = TRUE;
    #     return 0;
    # }
    # """
    # print("---Testing Invalid Boolean---")
    # parsed = parser.parse(sample_code_error_bool)
    # semantic.analyze_ast(parsed)