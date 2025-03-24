import ply.yacc as yacc
from lexer import lexer, tokens  # Import the lexer and the defined tokens
from syntax_tree import * # Import the AST node classes

# Global flags and lists for error handling
parsing_error = False  # Flag to indicate if a parsing error has occurred
syntax_errors = [] # List to store the messages of syntax errors found

tokens = tokens  # Re-declare tokens to be accessible within this module (though imported)

# Operator precedence (lowest to highest)
# This tuple defines the order in which operators are evaluated.
# Operators in the same tuple have the same precedence and are evaluated left to right (unless specified otherwise).
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'GT', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'ASSIGN'),  # Assignment operator is right-associative
)

# --- Grammar Rules with AST Construction ---

def p_program(p):
    '''program : translation_unit'''
    # Rule for the top-level program structure: it consists of a translation unit.
    # p[0] represents the result of this production (a Program node).
    # p[1] represents the result of the 'translation_unit' production.
    p[0] = Program(p[1])

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration'''
    # Rule for a translation unit: it can be a single external declaration or a sequence of them.
    # An external declaration can be a function definition or a global declaration.
    if len(p) == 2:
        # Single external declaration
        p[0] = [p[1]]
    else:
        # Multiple external declarations; append the new one to the existing list.
        p[0] = p[1] + [p[2]]

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration_statement SEMI'''
    # Rule for an external declaration: it can be either a function definition or a declaration statement followed by a semicolon.
    p[0] = p[1]

def p_function_definition(p):
    '''function_definition : TYPE ID LPAREN parameter_list_opt RPAREN block'''
    # Rule for defining a function: specifies the return type, name, parameters, and the function body (block).
    # p[1]: TYPE (e.g., 'int', 'void')
    # p[2]: ID (function name)
    # p[4]: parameter_list_opt (list of Parameter nodes)
    # p[6]: block (Block node representing the function body)
    p[0] = FunctionDefinition(p[1], p[2], p[4], p[6])

def p_parameter_list_opt(p):
    '''parameter_list_opt : parameter_list
                          | empty'''
    # Rule for an optional parameter list: it can be a parameter list or empty.
    p[0] = p[1] if p[1] is not None else []

def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter_list COMMA parameter'''
    # Rule for a parameter list: it can be a single parameter or a list of parameters separated by commas.
    if len(p) == 2:
        # Single parameter
        p[0] = [p[1]]
    else:
        # Multiple parameters; append the new parameter to the existing list.
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : TYPE ID'''
    # Rule for a single parameter: specifies the type and the identifier (name) of the parameter.
    # p[1]: TYPE
    # p[2]: ID
    p[0] = Parameter(p[1], p[2])

# --- Blocks ---

def p_block(p):
    '''block : LBRACE statement_list_opt RBRACE'''
    # Rule for a block of code enclosed in curly braces: contains an optional list of statements.
    # p[2]: statement_list_opt (list of Statement nodes)
    p[0] = Block(p[2])

def p_statement_list_opt(p):
    '''statement_list_opt : statement_list
                           | empty'''
    # Rule for an optional statement list: it can be a statement list or empty.
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    # Rule for a statement list: it can be a single statement or a sequence of statements.
    if len(p) == 2:
        # Single statement
        p[0] = [p[1]]
    else:
        # Multiple statements; append the new statement to the existing list.
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
    # Rule for a generic statement: it can be various types of statements.
    p[0] = p[1]

def p_empty_statement(p):
    '''empty_statement :'''
    # Rule for an empty statement (just a semicolon).
    p[0] = EmptyStatement()

# --- Declaration Statements ---

def p_declaration_statement(p):
    '''declaration_statement : TYPE ID
                             | TYPE ID ASSIGN initializer'''
    # Rule for a declaration statement: declares a variable with an optional initializer.
    # p[1]: TYPE
    # p[2]: ID (variable name)
    # p[4]: initializer (Expression node)
    if len(p) == 3:
        # Declaration without initializer
        p[0] = Declaration(p[1], p[2], None)
    else:
        # Declaration with initializer
        p[0] = Declaration(p[1], p[2], p[4])

def p_initializer(p):
    '''initializer : expression'''
    # Rule for an initializer: it's just an expression.
    # p[1]: expression (Expression node)
    p[0] = p[1]

# --- Assignment Statements ---
def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''
    # Rule for an assignment statement: assigns the value of an expression to a variable.
    # p[1]: ID (variable name)
    # p[3]: expression (Expression node)
    p[0] = Assignment(Identifier(p[1]), p[3])  # Create an Identifier node for the left-hand side.

# --- Return Statements ---

def p_return_statement(p):
    '''return_statement : RETURN expression_opt'''
    # Rule for a return statement: optionally returns an expression.
    # p[2]: expression_opt (Expression node or None)
    p[0] = ReturnStatement(p[2])

def p_expression_opt(p):
    '''expression_opt : expression
                      | empty'''
    # Rule for an optional expression: it can be an expression or empty.
    p[0] = p[1]

# --- Control Flow Statements ---

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                    | IF LPAREN expression RPAREN statement ELSE statement'''
    # Rule for an if statement: can have an optional else block.
    # p[3]: expression (condition)
    # p[5]: statement (then block)
    # p[7]: statement (else block, if present)
    if len(p) == 6:
        # If statement without else
        p[0] = IfStatement(p[3], p[5], None)
    else:
        # If statement with else
        p[0] = IfStatement(p[3], p[5], p[7])

def p_for_statement(p):
    '''for_statement : FOR LPAREN for_init_opt SEMI for_condition_opt SEMI for_increment_opt RPAREN statement'''
    # Rule for a for loop: specifies initialization, condition, increment, and the loop body.
    # p[3]: for_init_opt
    # p[5]: for_condition_opt
    # p[7]: for_increment_opt
    # p[9]: statement (loop body)
    p[0] = ForStatement(p[3], p[5], p[7], p[9])

def p_for_init_opt(p):
    '''for_init_opt : declaration_statement
                    | expression_statement
                    | empty'''
    # Rule for the optional initialization part of a for loop.
    p[0] = p[1]

def p_for_condition_opt(p):
    '''for_condition_opt : expression
                         | empty'''
    # Rule for the optional condition part of a for loop.
    p[0] = p[1]

def p_for_increment_opt(p):
    '''for_increment_opt : expression
                         | empty'''
    # Rule for the optional increment part of a for loop.
    p[0] = p[1]

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    # Rule for a while loop: specifies the condition and the loop body.
    # p[3]: expression (condition)
    # p[5]: statement (loop body)
    p[0] = WhileStatement(p[3], p[5])

# --- Expressions ---

def p_expression_statement(p):
    '''expression_statement : expression'''
    # Rule for an expression statement: an expression followed by a semicolon (handled in p_statement).
    p[0] = p[1]

def p_expression(p):
    '''expression : assignment_expression
                  | binary_expression
                  | primary_expression'''
    # Rule for a general expression: can be an assignment, a binary operation, or a primary expression.
    p[0] = p[1]

def p_assignment_expression(p):
    '''assignment_expression : ID ASSIGN expression'''
    # Rule for an assignment expression.
    p[0] = Assignment(p[1], p[3]) # Note: p[1] here is just the ID string, not wrapped in Identifier yet. It might be better to consistently use Identifier nodes.

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
    # Rule for binary expressions: defines operations between two expressions.
    # p[2]: operator (e.g., '+', '-', '*')
    # p[1]: left operand (Expression node)
    # p[3]: right operand (Expression node)
    p[0] = BinaryExpression(p[2], p[1], p[3])
    if p[0]:
        p[0].lineno = p.lineno(2) # Set the line number of the binary expression based on the operator's token.

def p_primary_expression(p):
    '''primary_expression : ID
                          | INT_NUM
                          | FLOAT_NUM
                          | DOUBLE_NUM
                          | CHAR_LIT
                          | BOOL_LIT
                          | LPAREN expression RPAREN
                          | ID LPAREN argument_list_opt RPAREN'''
    # Rule for primary expressions: the most basic building blocks of expressions.
    if len(p) == 2:
        # Identifier or Literal
        if p.slice[1].type == 'ID':
            p[0] = Identifier(p[1])
            if p[0]:
                p[0].lineno = p.lineno(1)  # Set line number for Identifier
                p[0].lexpos = p.lexpos(1)  # Set lexpos for Identifier
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
        # Parenthesized expression
        p[0] = p[2]
        if p[0]:
            p[0].lineno = p.lineno(1)
            p[0].lexpos = p.lexpos(1)
    elif len(p) == 5:
        # Function call
        p[0] = CallExpression(Identifier(p[1]), p[3])
        if p[0].callee: # Access the Identifier object within CallExpression
            p[0].callee.lineno = p.lineno(1)
            p[0].callee.lexpos = p.lexpos(1)

def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                          | empty'''
    # Rule for an optional argument list in a function call.
    p[0] = p[1] if p[1] is not None else []

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression'''
    # Rule for an argument list in a function call: can be a single expression or a list of expressions.
    if len(p) == 2:
        # Single argument
        p[0] = [p[1]]
    else:
        # Multiple arguments; append the new argument to the existing list.
        p[0] = p[1] + [p[3]]

# --- Empty Production ---

def p_empty(p):
    '''empty :'''
    # Rule for an empty production (matches nothing). Used for optional parts of the grammar.
    p[0] = None

# --- Error Handling ---

def p_error(p):
    '''Error handling function for syntax errors.'''
    global parsing_error, syntax_errors
    parsing_error = True
    if p:
        # If a token caused the error, extract its information.
        column = p.lexpos - lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
        error_message = f"Syntax error at line {p.lineno}, column {column}: Unexpected token '{p.value}' of type '{p.type}'"
        print(error_message) # Print the error message to the console.
        syntax_errors.append(error_message) # Store the error message in the list.
        parser.errok() # Attempt error recovery by skipping the problematic token.
    else:
        # If the error occurred at the end of the input (EOF).
        print("Syntax error at EOF") # Print the error message to the console.
        syntax_errors.append("Syntax error at EOF") # Store the error message in the list.

# --- Build the Parser ---
parser = yacc.yacc() # Create the parser object using the grammar rules defined above.