# Stores variable types
symbol_table = {}

type_compatibility = {
    'int': {'int'},
    'float': {'int', 'float'},
    'double': {'int', 'float', 'double'},
    'char': {'char'},
    'bool': {'bool'}
}

def reset_symbol_table():
    global symbol_table
    symbol_table = {}

def register_variable(var_name, var_type):
    symbol_table[var_name] = var_type
    return var_type

def check_type_compatibility(var_type, value_type, lineno=0):
    if value_type in type_compatibility.get(var_type, set()):
        return True
    else:
        error_msg = f"Type error at line {lineno}: Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
        raise TypeError(error_msg)

def get_expression_type(expr):
    if expr is None:
        return None
    
    expr_type = expr[0]
    

    if expr_type == 'int_literal':
        return 'int'
    elif expr_type == 'float_literal':
        return 'float'
    elif expr_type == 'double_literal':
        return 'double'
    elif expr_type == 'char_literal':
        return 'char'
    elif expr_type == 'bool_literal':
        return 'bool'
    
    elif expr_type == 'id':
        var_name = expr[1]
        if var_name in symbol_table:
            return symbol_table[var_name]
        else:
            raise NameError(f"Undefined variable: '{var_name}'")

    elif expr_type == 'binop':
        op = expr[1]
        left_type = get_expression_type(expr[2])
        right_type = get_expression_type(expr[3])
        
        if op in ['+', '-', '*', '/']:
            if left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            else:
                return 'int'
        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            return 'bool'
        
    elif expr_type == 'call':
        return 'int'
    
    # Handle assignments
    elif expr_type == 'assign':
        var_name = expr[1]
        value_expr = expr[2]
        if var_name in symbol_table:
            value_type = get_expression_type(value_expr)
            var_type = symbol_table[var_name]
            check_type_compatibility(var_type, value_type)
            return var_type
        else:
            raise NameError(f"Undefined variable: '{var_name}'")
    
    return None

def s_node(node):
    if node is None:
        return
        
    node_type = node[0]
    
    if node_type == 'program':
        s_program(node)
    elif node_type == 'declare':
        s_declaration(node)
    elif node_type == 'assign':
        s_assignment(node)
    elif node_type == 'function':
        s_function(node)
    elif node_type == 'block':
        s_block(node)
    elif node_type == 'for_loop':
        s_for_loop(node)
    elif node_type == 'while_loop':
        s_while_loop(node)
    elif node_type == 'return':
        s_return(node)
    elif node_type == 'call':
        s_call(node)
    elif node_type == 'binop':
        s_binop(node)
    
def s_program(node):
    function_list = node[1]
    
    reset_symbol_table()
    
    for function in function_list:
        s_node(function)

def s_declaration(node):
    var_type = node[1]
    var_name = node[2]
    init_expr = node[3]
    
    register_variable(var_name, var_type)
    
    if init_expr:
        expr_type = get_expression_type(init_expr)
        if not check_type_compatibility(var_type, expr_type):
            raise TypeError(f"Cannot assign value of type '{expr_type}' to variable of type '{var_type}'")

def s_assignment(node):
    var_name = node[1]
    expr = node[2]

    if var_name not in symbol_table:
        raise NameError(f"Undefined variable '{var_name}'")

    var_type = symbol_table[var_name]
    expr_type = get_expression_type(expr)
    
    if not check_type_compatibility(var_type, expr_type):
        pass

def s_function(node):
    return_type = node[1]
    func_name = node[2]
    params = node[3]
    block = node[4]
  
    s_node(block)

def s_block(node):
    statement_list = node[1]

    for statement in statement_list:
        s_node(statement)

def s_for_loop(node):
    init = node[1]
    condition = node[2]
    increment = node[3]
    block = node[4]
    
    if init:
        s_node(init)
    
    if condition:
        condition_type = get_expression_type(condition)
        if condition_type != 'bool' and condition_type is not None:
            raise TypeError(f"For loop condition must be boolean, got {condition_type}")
    
    if increment:
        s_node(increment)
    
    s_node(block)

def s_while_loop(node):
    condition = node[1]
    block = node[2]
    
    condition_type = get_expression_type(condition)
    if condition_type != 'bool' and condition_type is not None:
        raise TypeError(f"While loop condition must be boolean, got {condition_type}")
    
    s_node(block)

def s_return(node):
    expr = node[1]
    
    if expr:
        get_expression_type(expr)

def s_call(node):
    func_name = node[1]
    args = node[2]

    for arg in args:
        get_expression_type(arg)

def s_binop(node):
    op = node[1]
    left = node[2]
    right = node[3]
    
    left_type = get_expression_type(left)
    right_type = get_expression_type(right)
    
    if op in ['+', '-', '*', '/']:
        if left_type not in ['int', 'float', 'double'] or right_type not in ['int', 'float', 'double']:
            raise TypeError(f"Operator '{op}' requires numeric operands, got {left_type} and {right_type}")
    elif op in ['==', '!=']:
        if left_type != right_type and not (left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']):
            raise TypeError(f"Cannot compare {left_type} and {right_type} with operator '{op}'")
    elif op in ['<', '>', '<=', '>=']:
        if left_type not in ['int', 'float', 'double'] or right_type not in ['int', 'float', 'double']:
            raise TypeError(f"Operator '{op}' requires numeric operands, got {left_type} and {right_type}")

def s_ast(ast):
    """Main entry point for semantic analysis"""
    reset_symbol_table()
    s_node(ast)
    return True