#semantic.py
from syntax_tree import Program, FunctionDefinition, Block, Declaration, Assignment, ReturnStatement, IfStatement, \
    ForStatement, WhileStatement, BinaryExpression, Identifier, Literal, EmptyStatement, CallExpression


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.undeclared_reported = set() # Add this line

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None

    def set(self, name, value):
        if name in self.symbols:
            raise SemanticError(f"'{name}' already declared in this scope")
        self.symbols[name] = value

    def update(self, name, value):
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            raise SemanticError(f"'{name}' not declared")

class SemanticError(Exception):
    pass

type_compatibility = {
    'int': {'int'},
    'float': {'int', 'float'},
    'double': {'int', 'float', 'double'},
    'char': {'char', 'int'},
    'bool': {'bool'}
}

def check_type_compatibility(var_type, value_type, lineno=0):
    if value_type in type_compatibility.get(var_type, set()):
        return True
    else:
        error_msg = f"Type error at line {lineno}: Cannot assign value of type '{value_type}' to variable of type '{var_type}'"
        raise SemanticError(error_msg)

def get_expression_type(expression, current_scope):
    if isinstance(expression, Literal):
        return expression.type
    elif isinstance(expression, Identifier):
        print(f"get_expression_type: Identifier '{expression.name}', scope symbols: {current_scope.symbols.keys()}, parent symbols: {current_scope.parent.symbols.keys() if current_scope.parent else None}")
        info = current_scope.get(expression.name)
        if info:
            return info['type']
        else:
            if expression.name not in current_scope.undeclared_reported:
                current_scope.undeclared_reported.add(expression.name)
                raise SemanticError(f"Semantic Error: '{expression.name}' not declared before use.")
            return None
    elif isinstance(expression, BinaryExpression):
        left_type = get_expression_type(expression.left, current_scope)
        right_type = get_expression_type(expression.right, current_scope)
        op = expression.op

        if left_type is None or right_type is None:
            return None # Error in operands already reported

        if op == '+':
            if (left_type == 'int' and right_type == 'bool') or \
               (left_type == 'bool' and right_type == 'int'):
                raise SemanticError(f"Type error at line {expression.lineno if hasattr(expression, 'lineno') else 0}: Invalid operation '+' between types '{left_type}' and '{right_type}'.")
            elif left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            else:
                return 'int'
        elif op in ['-', '*', '/']:
            if left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            else:
                return 'int'
        elif op in ['==', '!=', '<', '>', '<=', '>=', '&&', '||']:
            return 'bool'
        return None
    elif isinstance(expression, Assignment):
        expr_type = get_expression_type(expression.rvalue, current_scope)
        return None
    return None

def semantic_analyzer(ast):
    errors = []
    global_scope = SymbolTable()

    def visit(node, current_scope):
        nonlocal errors
        print(f"Visiting node (again): {type(node)}") # Added "again" for clarity

        if isinstance(node, Program):
            print(f"Program Node from: {node.__class__.__module__}") # Check module
            for declaration in node.declarations:
                visit(declaration, current_scope)
        elif isinstance(node, FunctionDefinition):
                print(f"FunctionDefinition: {node.name}, Return Type: {node.return_type}")
                current_scope.set(node.name, {'type': node.return_type, 'kind': 'function', 'params': node.params})
                function_scope = SymbolTable(current_scope)
                if node.name == 'main' and node.params:
                    errors.append(f"Semantic Error: Function 'main' should not have parameters.")

                for param in node.params:
                    function_scope.set(param.name, {'type': param.param_type, 'kind': 'variable'})
                    print(f"Parameter in function scope: {param.name}")

                has_return = False

                def check_return(n):
                    nonlocal has_return
                    print(f"check_return called with node: {n}")  # Added print
                    if isinstance(n, ReturnStatement) and n.value is not None:
                        has_return = True
                    elif isinstance(n, Block):
                        if n.statements is not None:  # Added check
                            for stmt in n.statements:
                                check_return(stmt)
                    elif isinstance(n, IfStatement):
                        check_return(n.then_block)
                        if n.else_block:
                            check_return(n.else_block)
                    elif isinstance(n, (ForStatement, WhileStatement)):
                        check_return(n.body)

                if node.return_type != 'void':
                    check_return(node.body)  # Moved the call inside the if block
                    if not has_return:
                        errors.append(f"Semantic Error: Non-void function '{node.name}' must return a value.")

                # Check for return statement with value in void main
                if node.name == 'main' and node.return_type == 'void':
                    def check_void_main_return(n):
                        nonlocal errors
                        if isinstance(n, ReturnStatement) and n.value is not None:
                            errors.append(f"Semantic Error: Function 'main' must have return type 'int'.")
                        elif isinstance(n, Block):
                            for stmt in n.statements:
                                check_void_main_return(stmt)
                        elif isinstance(n, IfStatement):
                            check_void_main_return(n.then_block)
                            if n.else_block:
                                check_void_main_return(n.else_block)
                        elif isinstance(n, (ForStatement, WhileStatement)):
                            check_void_main_return(n.body)

                    check_void_main_return(node.body)

                visit(node.body, function_scope)  # Still visit the body for other checks

        elif isinstance(node, Block):
            print(f"Block Node from: {node.__class__.__module__}") # Check module
            block_scope = SymbolTable(current_scope)
            if node.statements is not None:
                for statement in node.statements:
                    visit(statement, block_scope)
        elif isinstance(node, Declaration):
            print(f"Declaration Node from: {node.__class__.__module__}") # Check module
            if current_scope.get(node.name):
                errors.append(f"Semantic Error: '{node.name}' already declared.")
            else:
                current_scope.set(node.name, {'type': node.data_type, 'kind': 'variable'})
                if node.initializer:
                    initializer_type = get_expression_type(node.initializer, current_scope)
                    print(
                        f"Declaration: var_type='{node.data_type}', value_type='{initializer_type}'")
                    if initializer_type:
                        try:
                            check_type_compatibility(node.data_type, initializer_type)
                        except SemanticError as e:
                            print(f"Caught SemanticError: {e}")
                            errors.append(
                                f"Semantic Error: Type mismatch in declaration of '{node.name}'. Expected '{node.data_type}', got '{initializer_type}'.")
        elif isinstance(node, Assignment):
            print(f"Assignment Node from: {node.__class__.__module__}")  # Check module
            try:
                # Check if the left-hand side variable is declared
                get_expression_type(node.lvalue, current_scope)
                var_info = current_scope.get(node.lvalue.name)  # Get info again after checking
                if var_info:
                    expr_type = get_expression_type(node.rvalue, current_scope)
                    if expr_type:
                        try:
                            check_type_compatibility(var_info['type'], expr_type)
                        except SemanticError as e:
                            errors.append(
                                f"Semantic Error: Type mismatch in assignment to '{node.lvalue.name}'. Expected '{var_info['type']}', got '{expr_type}'.")
            except SemanticError as e:
                errors.append(str(e))
        elif isinstance(node, ReturnStatement):
            print(f"ReturnStatement Node from: {node.__class__.__module__}")  # Check module
            if node.value:
                try:
                    get_expression_type(node.value, current_scope)  # Perform type checking on the return value
                except SemanticError as e:
                    errors.append(str(e))
                    print(f"Error added from ReturnStatement: {e}")
        elif isinstance(node, IfStatement):
            print(f"IfStatement Node from: {node.__class__.__module__}") # Check module
            visit(node.condition, current_scope)
            condition_type = get_expression_type(node.condition, current_scope)
            if condition_type != 'bool' and condition_type is not None:
                errors.append(f"Semantic Error: If condition must be boolean, got '{condition_type}'.")
            visit(node.then_block, current_scope)
            if node.else_block:
                visit(node.else_block, current_scope)
        elif isinstance(node, ForStatement):
            print(f"ForStatement Node from: {node.__class__.__module__}") # Check module
            if node.init:
                visit(node.init, current_scope)
            if node.condition:
                visit(node.condition, current_scope)
                condition_type = get_expression_type(node.condition, current_scope)
                if condition_type != 'bool' and condition_type is not None:
                    errors.append(f"Semantic Error: For loop condition must be boolean, got '{condition_type}'.")
            if node.increment:
                visit(node.increment, current_scope)
            visit(node.body, current_scope)
        elif isinstance(node, WhileStatement):
            print(f"WhileStatement Node from: {node.__class__.__module__}") # Check module
            visit(node.condition, current_scope)
            condition_type = get_expression_type(node.condition, current_scope)
            if condition_type != 'bool' and condition_type is not None:
                errors.append(f"Semantic Error: While loop condition must be boolean, got '{condition_type}'.")
            visit(node.body, current_scope)
        elif isinstance(node, BinaryExpression):
            print(f"BinaryExpression Node from: {node.__class__.__module__}") # Check module
            get_expression_type(node, current_scope) # Type checking is done in get_expression_type
        elif isinstance(node, Identifier):
            print(f"Identifier Node from: {node.__class__.__module__}") # Check module
            pass # Removed the direct check for undeclared variables here
        elif isinstance(node, Literal):
            print(f"Literal Node from: {node.__class__.__module__}") # Check module
            pass
        elif isinstance(node, EmptyStatement):
            print(f"EmptyStatement Node from: {node.__class__.__module__}") # Check module
            pass
        elif isinstance(node, CallExpression):
            print(f"CallExpression Node from: {node.__class__.__module__}") # Check module
            function_name = node.callee.name
            info = current_scope.get(function_name)
            if not info or info['kind'] != 'function':
                errors.append(f"Semantic Error: Function '{function_name}' not declared.")
            for arg in node.arguments:
                get_expression_type(arg, current_scope) # Check types of arguments

    visit(ast, global_scope)
    print("Errors:", errors) # Print the final errors list
    return errors