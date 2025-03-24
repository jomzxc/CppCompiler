# syntax_tree.py

class Node:
    """
    Base class for all nodes in the Abstract Syntax Tree (AST).
    Each node can optionally store the line number and lexical position
    in the source code where the corresponding construct was found.
    """
    def __init__(self, lineno=None, lexpos=None):
        """
        Initializes a Node object.

        Args:
            lineno (int, optional): The line number in the source code. Defaults to None.
            lexpos (int, optional): The starting lexical position in the source code. Defaults to None.
        """
        self.lineno = lineno
        self.lexpos = lexpos

class Program(Node):
    """
    Represents the root of the AST, containing a list of top-level declarations.
    """
    def __init__(self, declarations):
        """
        Initializes a Program object.

        Args:
            declarations (list): A list of external declarations (e.g., FunctionDefinition, Declaration).
        """
        super().__init__()
        self.declarations = declarations

class FunctionDefinition(Node):
    """
    Represents the definition of a function.
    """
    def __init__(self, return_type, name, params, body):
        """
        Initializes a FunctionDefinition object.

        Args:
            return_type (str): The data type returned by the function (e.g., 'int', 'void').
            name (str): The name of the function.
            params (list): A list of Parameter objects representing the function's parameters.
            body (Block): A Block object representing the function's body.
        """
        super().__init__()
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class Parameter(Node):
    """
    Represents a parameter in a function definition.
    """
    def __init__(self, param_type, name):
        """
        Initializes a Parameter object.

        Args:
            param_type (str): The data type of the parameter (e.g., 'int', 'float').
            name (str): The name of the parameter.
        """
        super().__init__()
        self.param_type = param_type
        self.name = name

class Block(Node):
    """
    Represents a block of code enclosed in curly braces, containing a list of statements.
    """
    def __init__(self, statements):
        """
        Initializes a Block object.

        Args:
            statements (list): A list of Statement objects within the block.
        """
        super().__init__()
        self.statements = statements

class Declaration(Node):
    """
    Represents a variable declaration.
    """
    def __init__(self, data_type, name, initializer):
        """
        Initializes a Declaration object.

        Args:
            data_type (str): The data type of the variable (e.g., 'int', 'char').
            name (str): The name of the variable.
            initializer (Node, optional): An Expression node representing the initial value. Defaults to None.
        """
        super().__init__()
        self.data_type = data_type
        self.name = name
        self.initializer = initializer

class Assignment(Node):
    """
    Represents an assignment operation.
    """
    def __init__(self, lvalue, rvalue):
        """
        Initializes an Assignment object.

        Args:
            lvalue (Node): The left-hand side of the assignment (usually an Identifier).
            rvalue (Node): The right-hand side of the assignment (an Expression).
        """
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue

class ReturnStatement(Node):
    """
    Represents a return statement in a function.
    """
    def __init__(self, value):
        """
        Initializes a ReturnStatement object.

        Args:
            value (Node, optional): An Expression node representing the value to be returned. Defaults to None.
        """
        super().__init__()
        self.value = value

class IfStatement(Node):
    """
    Represents an if statement.
    """
    def __init__(self, condition, then_block, else_block):
        """
        Initializes an IfStatement object.

        Args:
            condition (Node): An Expression node representing the condition to be evaluated.
            then_block (Node): A Statement node (usually a Block) to be executed if the condition is true.
            else_block (Node, optional): A Statement node (usually a Block) to be executed if the condition is false. Defaults to None.
        """
        super().__init__()
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStatement(Node):
    """
    Represents a for loop.
    """
    def __init__(self, init, condition, increment, body):
        """
        Initializes a ForStatement object.

        Args:
            init (Node, optional): A Statement node representing the initialization part of the loop. Defaults to None.
            condition (Node, optional): An Expression node representing the loop condition. Defaults to None.
            increment (Node, optional): A Statement node representing the increment/decrement part of the loop. Defaults to None.
            body (Node): A Statement node (usually a Block) representing the loop body.
        """
        super().__init__()
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class WhileStatement(Node):
    """
    Represents a while loop.
    """
    def __init__(self, condition, body):
        """
        Initializes a WhileStatement object.

        Args:
            condition (Node): An Expression node representing the loop condition.
            body (Node): A Statement node (usually a Block) representing the loop body.
        """
        super().__init__()
        self.condition = condition
        self.body = body

class BinaryExpression(Node):
    """
    Represents a binary operation (e.g., +, -, ==).
    """
    def __init__(self, op, left, right):
        """
        Initializes a BinaryExpression object.

        Args:
            op (str): The operator of the binary expression (e.g., '+', '-', '==').
            left (Node): The left operand (an Expression node).
            right (Node): The right operand (an Expression node).
        """
        super().__init__()
        self.op = op
        self.left = left
        self.right = right

class Identifier(Node):
    """
    Represents an identifier (e.g., a variable name).
    """
    def __init__(self, name, lineno=None, lexpos=None):
        """
        Initializes an Identifier object.

        Args:
            name (str): The name of the identifier.
            lineno (int, optional): The line number in the source code. Defaults to None.
            lexpos (int, optional): The starting lexical position in the source code. Defaults to None.
        """
        super().__init__(lineno, lexpos)
        self.name = name

class Literal(Node):
    """
    Represents a literal value (e.g., 10, 3.14, 'a', true).
    """
    def __init__(self, type, value, lineno=None, lexpos=None):
        """
        Initializes a Literal object.

        Args:
            type (str): The data type of the literal (e.g., 'int', 'float', 'char', 'bool').
            value (str): The string representation of the literal value.
            lineno (int, optional): The line number in the source code. Defaults to None.
            lexpos (int, optional): The starting lexical position in the source code. Defaults to None.
        """
        super().__init__(lineno, lexpos)
        self.type = type
        self.value = value

class EmptyStatement(Node):
    """
    Represents an empty statement (just a semicolon).
    """
    def __init__(self):
        """
        Initializes an EmptyStatement object.
        """
        super().__init__()

class CallExpression(Node):
    """
    Represents a function call.
    """
    def __init__(self, callee, arguments):
        """
        Initializes a CallExpression object.

        Args:
            callee (Identifier): An Identifier node representing the function being called.
            arguments (list): A list of Expression nodes representing the arguments passed to the function.
        """
        super().__init__()
        self.callee = callee
        self.arguments = arguments