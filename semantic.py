from syntax_tree import Program, FunctionDefinition, Block, Declaration, Assignment, ReturnStatement, IfStatement, \
    ForStatement, WhileStatement, BinaryExpression, Identifier, Literal, EmptyStatement, CallExpression


class SymbolTable:
    """
    Manages symbols (variables, functions) within different scopes of the program.
    Supports nested scopes through a parent table.
    """
    def __init__(self, parent=None):
        """
        Initializes the symbol table.

        Args:
            parent (SymbolTable, optional): The parent scope's symbol table. Defaults to None.
        """
        self.symbols = {}  # Dictionary to store symbols (name: info) in the current scope.
        self.parent = parent  # Reference to the parent scope's symbol table.
        self.undeclared_reported = set()  # Keeps track of undeclared variables to avoid repeated errors.

    def get(self, name):
        """
        Retrieves the information associated with a symbol name.

        Args:
            name (str): The name of the symbol.

        Returns:
            dict or None: The symbol's information (e.g., {'type': 'int', 'kind': 'variable'}),
                           or None if the symbol is not found in the current or parent scopes.
        """
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        """
        Adds a new symbol to the current scope.

        Args:
            name (str): The name of the symbol.
            value (dict): The information associated with the symbol.

        Raises:
            SemanticError: If the symbol is already declared in the current scope.
        """
        if name in self.symbols:
            raise SemanticError(f"'{name}' already declared in this scope")
        self.symbols[name] = value

    def update(self, name, value):
        """
        Updates the information of an existing symbol. Searches in the current and parent scopes.

        Args:
            name (str): The name of the symbol to update.
            value (dict): The new information for the symbol.

        Raises:
            SemanticError: If the symbol is not declared in any scope.
        """
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            raise SemanticError(f"'{name}' not declared")


class SemanticError(Exception):
    """
    Custom exception class for semantic analysis errors.
    """
    pass


# Define type compatibility rules for assignments and operations.
type_compatibility = {
    'int': {'int', 'bool', 'char'},
    'float': {'int', 'float', 'char'},
    'double': {'int', 'float', 'double', 'char'},
    'char': {'char', 'int'},
    'bool': {'bool', 'int'}
}


def check_type_compatibility(var_type, value_type, lineno=0):
    """
    Checks if a value type is compatible with a variable type based on predefined rules.

    Args:
        var_type (str): The declared type of the variable.
        value_type (str): The type of the value being assigned or used.
        lineno (int, optional): The line number where the type incompatibility occurs. Defaults to 0.

    Raises:
        SemanticError: If the value type is not compatible with the variable type.

    Returns:
        bool: True if the types are compatible.
    """
    if value_type in type_compatibility.get(var_type, set()):
        return True
    raise SemanticError(f"Type error at line {lineno}: Cannot assign value of type '{value_type}' to variable of type '{var_type}'")


def get_expression_type(expression, current_scope):
    """
    Determines the type of an expression.

    Args:
        expression: The expression node from the syntax tree.
        current_scope (SymbolTable): The current scope in which the expression is evaluated.

    Returns:
        str or None: The type of the expression (e.g., 'int', 'bool'), or None if an error occurred
                     (e.g., undeclared identifier and error reported).

    Raises:
        SemanticError: If an undeclared identifier is encountered for the first time, or if there's
                       an invalid operation between types in a binary expression.
    """
    if isinstance(expression, Literal):
        return expression.type
    elif isinstance(expression, Identifier):
        info = current_scope.get(expression.name)
        if info:
            return info['type']
        elif expression.name not in current_scope.undeclared_reported:
            current_scope.undeclared_reported.add(expression.name)
            raise SemanticError(f"Semantic Error: '{expression.name}' not declared before use.")
        return None
    elif isinstance(expression, BinaryExpression):
        left_type = get_expression_type(expression.left, current_scope)
        right_type = get_expression_type(expression.right, current_scope)
        op = expression.op

        if left_type is None or right_type is None:
            return None  # Error in operands already reported

        if op == '+':
            if (left_type == 'int' and right_type == 'bool') or \
               (left_type == 'bool' and right_type == 'int'):
                raise SemanticError(f"Type error at line {expression.lineno if hasattr(expression, 'lineno') else 0}: Invalid operation '+' between types '{left_type}' and '{right_type}'.")
            elif left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            return 'int'
        elif op in ['-', '*', '/']:
            if left_type == 'double' or right_type == 'double':
                return 'double'
            elif left_type == 'float' or right_type == 'float':
                return 'float'
            return 'int'
        elif op in ['==', '!=', '<', '>', '<=', '>=', '&&', '||']:
            return 'bool'
        return None
    elif isinstance(expression, Assignment):
        get_expression_type(expression.rvalue, current_scope)
        return None
    return None


def semantic_analyzer(ast):
    """
    Performs semantic analysis on the Abstract Syntax Tree (AST).

    Args:
        ast: The root node of the Abstract Syntax Tree.

    Returns:
        list: A list of semantic error messages found during the analysis.
    """
    errors = []# List to store semantic errors.
    global_scope = SymbolTable()  # Create the global scope symbol table.

    def visit(node, current_scope):
        """
        Recursively visits nodes of the AST to perform semantic checks.

        Args:
            node: The current node being visited.
            current_scope (SymbolTable): The symbol table for the current scope.
        """
        nonlocal errors

        if isinstance(node, Program):
            # Visit each declaration in the program.
            for declaration in node.declarations:
                visit(declaration, current_scope)
        elif isinstance(node, FunctionDefinition):
            # Add the function to the current scope.
            current_scope.set(node.name, {'type': node.return_type, 'kind': 'function', 'params': node.params})
            # Create a new scope for the function's body.
            function_scope = SymbolTable(current_scope)
            # Check if the 'main' function has parameters (which is not allowed).
            if node.name == 'main' and node.params:
                errors.append(f"Semantic Error: Function 'main' should not have parameters.")

            # Add function parameters to the function's scope.
            for param in node.params:
                function_scope.set(param.name, {'type': param.param_type, 'kind': 'variable'})

            has_return = False  # Flag to track if a non-void function has a return statement.

            def check_return(n):
                """
                Helper function to recursively check for return statements in a function body.
                """
                nonlocal has_return
                if isinstance(n, ReturnStatement) and n.value is not None:
                    has_return = True
                elif isinstance(n, Block):
                    if n.statements:
                        for stmt in n.statements:
                            check_return(stmt)
                elif isinstance(n, IfStatement):
                    check_return(n.then_block)
                    if n.else_block:
                        check_return(n.else_block)
                elif isinstance(n, (ForStatement, WhileStatement)):
                    check_return(n.body)

            # Check if a non-void function has a return statement.
            if node.return_type != 'void':
                check_return(node.body)
                if not has_return:
                    errors.append(f"Semantic Error: Non-void function '{node.name}' must return a value.")

            # Check for return statement with a value in a void 'main' function.
            if node.name == 'main' and node.return_type == 'void':
                def check_void_main_return(n):
                    """
                    Helper function to check for return statements with values in a void 'main' function.
                    """
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

            # Visit the function's body with the function's scope.
            visit(node.body, function_scope)

        elif isinstance(node, Block):
            # Create a new scope for the block, inheriting from the current scope.
            block_scope = SymbolTable(current_scope)
            if node.statements:
                # Visit each statement in the block.
                for statement in node.statements:
                    visit(statement, block_scope)
        elif isinstance(node, Declaration):
            # Check if the variable is already declared in the current scope.
            if current_scope.get(node.name):
                errors.append(f"Semantic Error: '{node.name}' already declared.")
            else:
                # Add the variable to the current scope.
                current_scope.set(node.name, {'type': node.data_type, 'kind': 'variable'})
                # Check type compatibility if there's an initializer.
                if node.initializer:
                    initializer_type = get_expression_type(node.initializer, current_scope)
                    if initializer_type:
                        try:
                            check_type_compatibility(node.data_type, initializer_type)
                        except SemanticError as e:
                            errors.append(
                                f"Semantic Error: Type mismatch in declaration of '{node.name}'. Expected '{node.data_type}', got '{initializer_type}'.")
        elif isinstance(node, Assignment):
            try:
                # Check if the left-hand side variable is declared.
                get_expression_type(node.lvalue, current_scope)
                var_info = current_scope.get(node.lvalue.name)
                if var_info:
                    # Check type compatibility between the variable and the assigned expression.
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
            # Perform type checking on the return value if it exists.
            if node.value:
                try:
                    get_expression_type(node.value, current_scope)
                except SemanticError as e:
                    errors.append(str(e))
        elif isinstance(node, IfStatement):
            # Visit the condition, then block, and else block (if it exists).
            visit(node.condition, current_scope)
            # Check if the condition is of boolean type.
            condition_type = get_expression_type(node.condition, current_scope)
            if condition_type != 'bool' and condition_type is not None:
                errors.append(f"Semantic Error: If condition must be boolean, got '{condition_type}'.")
            visit(node.then_block, current_scope)
            if node.else_block:
                visit(node.else_block, current_scope)
        elif isinstance(node, ForStatement):
            # Visit the initialization, condition, increment, and body of the for loop.
            if node.init:
                visit(node.init, current_scope)
            if node.condition:
                visit(node.condition, current_scope)
                # Check if the loop condition is of boolean type.
                condition_type = get_expression_type(node.condition, current_scope)
                if condition_type != 'bool' and condition_type is not None:
                    errors.append(f"Semantic Error: For loop condition must be boolean, got '{condition_type}'.")
            if node.increment:
                visit(node.increment, current_scope)
            visit(node.body, current_scope)
        elif isinstance(node, WhileStatement):
            # Visit the condition and body of the while loop.
            visit(node.condition, current_scope)
            # Check if the loop condition is of boolean type.
            condition_type = get_expression_type(node.condition, current_scope)
            if condition_type != 'bool' and condition_type is not None:
                errors.append(f"Semantic Error: While loop condition must be boolean, got '{condition_type}'.")
            visit(node.body, current_scope)
        elif isinstance(node, BinaryExpression):
            # Type checking for binary expressions is handled in get_expression_type.
            get_expression_type(node, current_scope)
        elif isinstance(node, CallExpression):
            # Check if the called function is declared.
            function_name = node.callee.name
            info = current_scope.get(function_name)
            if not info or info['kind'] != 'function':
                errors.append(f"Semantic Error: Function '{function_name}' not declared.")

    # Start the semantic analysis from the root of the AST (Program node) with the global scope.
    visit(ast, global_scope)
    print("Errors:", errors)
    return errors