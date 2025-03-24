# Global symbol table to track variables and their types during semantic analysis.
symbol_table = {}

# Add a function table to track return types and parameters
function_table = {}

# Stack of symbol tables for nested scopes
scope_stack = [{}]

# This dictionary defines type compatibility rules.
# For each variable type (key), the set of value types (values) that can be assigned to it.
# For example, a 'double' can accept values of type 'int', 'float', and 'double'.
type_compatibility = {
    'int': {'int'},
    'float': {'int', 'float'},
    'double': {'int', 'float', 'double'},
    'char': {'char'},
    'bool': {'bool'}
}

def reset_symbol_table():
    """
    Resets the symbol table to an empty dictionary.
    This is typically called at the start of analyzing a new program.
    """
    global symbol_table
    symbol_table = {}

def register_function(func_name, return_type, params):
    """Register function signature in the function table"""
    function_table[func_name] = {
        'return_type': return_type,
        'params': params  # List of (param_type, param_name) tuples
    }

def register_variable(var_name, var_type):
    """
    Registers a variable in the symbol table.
    
    Parameters:
        var_name (str): The name of the variable.
        var_type (str): The data type of the variable.
        
    Returns:
        str: The data type of the registered variable.
    """
    symbol_table[var_name] = var_type
    return var_type

def check_type_compatibility(var_type, value_type, lineno=0):
    """
    Checks if a value of a given type can be assigned to a variable of another type.
    
    Parameters:
        var_type (str): The data type of the variable.
        value_type (str): The data type of the value being assigned.
        lineno (int): Line number for error reporting (optional).
        
    Returns:
        bool: True if compatible, otherwise raises TypeError exception.
        
    Raises:
        TypeError: If the value type is not compatible with the variable type.
    """
    if value_type in type_compatibility.get(var_type, set()):
        return True
    else:
        error_msg = f"Type error at line {lineno}: Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
        raise TypeError(error_msg)

def check_return_statements(block_node, expected_type):
    """Check if all return statements in a block match the expected type"""
    # Recursive helper function to find return statements
    def find_returns(node):
        if node is None:
            return []
        
        if node[0] == 'return':
            return [node]
        
        if node[0] == 'block':
            returns = []
            for stmt in node[1]:
                returns.extend(find_returns(stmt))
            return returns
        
        if node[0] in ('for_loop', 'while_loop'):
            return find_returns(node[-1])  # Check the loop body
        
        return []
    
    returns = find_returns(block_node)
    
    # Check each return statement
    for ret_node in returns:
        expr = ret_node[1]
        if expr is None:
            # void return
            if expected_type != 'void':
                raise TypeError(f"Function with return type '{expected_type}' has empty return statement")
        else:
            ret_type = get_expression_type(expr)
            if not check_type_compatibility(expected_type, ret_type):
                raise TypeError(f"Return statement type '{ret_type}' doesn't match function return type '{expected_type}'")

def get_expression_type(expr):
    """
    Determines the data type of an expression.
    
    Parameters:
        expr (tuple): The AST node representing the expression.
        
    Returns:
        str: The data type of the expression, or None if it cannot be determined.
        
    Raises:
        NameError: If a variable is used before being defined.
        TypeError: If there are type compatibility issues in the expression.
    """
    if expr is None:
        return None
    
    expr_type = expr[0]  # The first element of the tuple is the node type
    
    # Literal values - return their corresponding data types
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
    
    # Variable identifier - look up its type in the symbol table
    elif expr_type == 'id':
        var_name = expr[1]
        if var_name in symbol_table:
            return symbol_table[var_name]
        else:
            raise NameError(f"Undefined variable: '{var_name}'")

    # Binary operations - determine type based on operand types and operation
    elif expr_type == 'binop':
        op = expr[1]  # The operation (e.g., '+', '-', '*', '/')
        left_type = get_expression_type(expr[2])  # Type of left operand
        right_type = get_expression_type(expr[3])  # Type of right operand
        
        # Arithmetic operations - result type depends on operand types
        if op in ['+', '-', '*', '/']:
            # Type promotion: double > float > int
            if left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            else:
                return 'int'
        # Comparison operations - always return boolean
        elif op in ['==', '!=', '<', '>', '<=', '>=']:
            return 'bool'
    
    # Function call - currently assumes all functions return int
    # This is a simplification and would need to be extended for a full implementation
    elif expr_type == 'call':
        return 'int'
    
    # Assignment - get the type of the variable being assigned to
    elif expr_type == 'assign':
        var_name = expr[1]  # Variable name
        value_expr = expr[2]  # Expression being assigned
        if var_name in symbol_table:
            value_type = get_expression_type(value_expr)  # Type of the value expression
            var_type = symbol_table[var_name]  # Type of the variable
            check_type_compatibility(var_type, value_type)  # Check if types are compatible
            return var_type
        else:
            raise NameError(f"Undefined variable: '{var_name}'")
    
    # Default return if the expression type isn't recognized
    return None

def get_promoted_type(type1, type2):
    """Determine the resulting type from an operation on two types"""
    numeric_types = ['int', 'float', 'double']
    
    # If both types are numeric, choose the more precise type
    if type1 in numeric_types and type2 in numeric_types:
        if 'double' in (type1, type2):
            return 'double'
        elif 'float' in (type1, type2):
            return 'float'
        else:
            return 'int'
    
    # If types are the same, return that type
    if type1 == type2:
        return type1

    return type1

def s_node(node):
    """
    Dispatches a node to the appropriate semantic analysis function based on its type.
    This is the main dispatcher for semantic analysis.
    
    Parameters:
        node (tuple): The AST node to analyze.
    """
    if node is None:
        return
        
    node_type = node[0]
    
    # Dispatch to the appropriate function based on node type
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
    """
    Performs semantic analysis on a program node.
    
    Parameters:
        node (tuple): The program node in the AST.
    """
    function_list = node[1]
    
    reset_symbol_table()
    
    # Analyze each function in the program
    for function in function_list:
        s_node(function)

def s_declaration(node):
    """
    Analyzes a variable declaration node.
    
    Parameters:
        node (tuple): The declaration node in the AST.
        
    Raises:
        TypeError: If there's a type mismatch in the initialization.
    """
    var_type = node[1]
    var_name = node[2]
    init_expr = node[3]
    
    # Register the variable in the symbol table
    register_variable(var_name, var_type)
    
    # If the variable is initialized, check type compatibility
    if init_expr:
        expr_type = get_expression_type(init_expr)
        if not check_type_compatibility(var_type, expr_type):
            raise TypeError(f"Cannot assign value of type '{expr_type}' to variable of type '{var_type}'")

def s_assignment(node):
    """
    Analyzes an assignment node.
    
    Parameters:
        node (tuple): The assignment node in the AST.
        
    Raises:
        NameError: If the variable is not defined.
        TypeError: If the assigned type is not compatible with the variable type.
    """
    var_name = node[1]
    expr = node[2]

    if var_name not in symbol_table:
        raise NameError(f"Undefined variable '{var_name}'")

    var_type = symbol_table[var_name]
    expr_type = get_expression_type(expr)
    
    if not check_type_compatibility(var_type, expr_type):
        pass  # This just raises a TypeError in check_type_compatibility

def s_function(node):
    """
    Analyzes a function definition node.
    
    Parameters:
        node (tuple): The function node in the AST.
    """
    global symbol_table
    
    return_type = node[1]
    func_name = node[2]
    params = node[3]
    block = node[4]
  
    # Register function in function table
    param_info = [(param[1], param[2]) for param in params]  # Extract type and name
    register_function(func_name, return_type, param_info)
    
    # Create a new scope for the function body
    old_symbol_table = symbol_table.copy()
    reset_symbol_table()
    
    # Register parameters in the function scope
    for param in params:
        param_type = param[1]
        param_name = param[2]
        register_variable(param_name, param_type)

    # Analyze the function body
    s_node(block)

    # Verify return statements match function return type
    # Restore the outer scope
    symbol_table = old_symbol_table

def s_block(node):
    """
    Analyzes a block of statements.
    
    Parameters:
        node (tuple): The block node in the AST.
    """
    statement_list = node[1]

    # Analyze each statement in the block
    for statement in statement_list:
        s_node(statement)

def s_for_loop(node):
    """
    Analyzes a for loop node.
    
    Parameters:
        node (tuple): The for_loop node in the AST.
        
    Raises:
        TypeError: If the loop condition is not a boolean expression.
    """
    init = node[1]
    condition = node[2]
    increment = node[3]
    block = node[4]
    
    # Analyze the initialization expression if present
    if init:
        s_node(init)
    
    # Check that the condition is a boolean expression if present
    if condition:
        condition_type = get_expression_type(condition)
        if condition_type != 'bool' and condition_type is not None:
            raise TypeError(f"   {condition_type}")
    
    # Analyze the increment expression if present
    if increment:
        s_node(increment)
    
    s_node(block)

def s_while_loop(node):
    """
    Analyzes a while loop node.
    
    Parameters:
        node (tuple): The while_loop node in the AST.
        
    Raises:
        TypeError: If the loop condition is not a boolean expression.
    """
    condition = node[1]
    block = node[2]
    
    # Check that the condition is a boolean expression
    condition_type = get_expression_type(condition)
    if condition_type != 'bool' and condition_type is not None:
        raise TypeError(f"While loop condition must be boolean, but found {condition_type}")
    
    s_node(block)

def s_return(node):
    """
    Analyzes a return statement node.
    
    Parameters:
        node (tuple): The return node in the AST.
    """
    expr = node[1]
    
    # Determine the type of the return expression if present
    if expr:
        get_expression_type(expr)

def s_call(node):
    """
    Analyzes a function call node.
    
    Parameters:
        node (tuple): The call node in the AST.
    """
    func_name = node[1]
    args = node[2]

    # Check if function exists
    if func_name not in function_table:
        raise NameError(f"Undefined function: '{func_name}'")
    
    func_info = function_table[func_name]
    expected_params = func_info['params']
    
    # Check argument count
    if len(args) != len(expected_params):
        raise TypeError(f"Function '{func_name}' expects {len(expected_params)} arguments, but found {len(args)}")
    
    # Check argument types
    for i, (arg, expected) in enumerate(zip(args, expected_params)):
        arg_type = get_expression_type(arg)
        expected_type = expected[0]
        if not check_type_compatibility(expected_type, arg_type):
            raise TypeError(f"Argument {i+1} of function '{func_name}' expects {expected_type}, but found {arg_type}")
    
    # Return the function's return type
    return func_info['return_type']

def s_expression(node):
    """Handles expression nodes generically"""
    return get_expression_type(node)

def s_group(node):
    """Handle parenthesized expressions"""
    # just need to analyze the inner expression
    return get_expression_type(node)

def s_binop(node):
    """
    Analyzes a binary operation node.
    
    Parameters:
        node (tuple): The binop node in the AST.
        
    Raises:
        TypeError: If the operands are not compatible with the operation.
    """
    op = node[1]
    left = node[2]
    right = node[3]
    
    # Get the types of both operands
    left_type = get_expression_type(left)
    right_type = get_expression_type(right)
    
    # Check type constraints based on operation type
    # Arithmetic operations require numeric operands
    if op in ['+', '-', '*', '/']:
        if left_type not in ['int', 'float', 'double'] or right_type not in ['int', 'float', 'double']:
            raise TypeError(f"Operator '{op}' requires numeric operands, but found {left_type} and {right_type}")
    
    # Equality operations require comparable types
    elif op in ['==', '!=']:
        # Types must be exactly the same or both numeric
        if left_type != right_type and not (left_type in ['int', 'float', 'double'] and right_type in ['int', 'float', 'double']):
            raise TypeError(f"Cannot compare {left_type} and {right_type} with operator '{op}'")
    
    # Relational operations require numeric operands
    elif op in ['<', '>', '<=', '>=']:
        if left_type not in ['int', 'float', 'double'] or right_type not in ['int', 'float', 'double']:
            raise TypeError(f"Operator '{op}' requires numeric operands, but found {left_type} and {right_type}")

def enter_scope():
    """Enter a new scope"""
    scope_stack.append({})

def exit_scope():
    """Exit the current scope"""
    if len(scope_stack) > 1:
        scope_stack.pop()

def register_variable_in_current_scope(var_name, var_type):
    """Register variable in the current scope"""
    scope_stack[-1][var_name] = var_type
    return var_type

def lookup_variable(var_name):
    """Look up a variable starting from the innermost scope"""
    for scope in reversed(scope_stack):
        if var_name in scope:
            return scope[var_name]
    return None

def s_ast(ast):
    """
    Main entry point for semantic analysis.
    
    Parameters:
        ast (tuple): The AST representing the entire program.
        
    Returns:
        bool: True if semantic analysis completes without errors.
    """
    reset_symbol_table()
    s_node(ast)
    return True